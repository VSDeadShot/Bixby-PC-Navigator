import os
import glob
import sys
import json
import urllib.request

try:
    import PyPDF2
    import docx
except ImportError:
    print("Missing dependencies. Run: pip install PyPDF2 python-docx")
    sys.exit(1)

api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        return f"Error reading PDF: {e}"
    return text

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading Word document: {e}"

def find_file(search_term, search_dir):
    search_term = search_term.lower()
    found_files = []
    
    # Windows 11 often puts Documents inside OneDrive
    onedrive_dir = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Documents')
    dirs_to_search = [search_dir]
    if os.path.exists(onedrive_dir):
        dirs_to_search.append(onedrive_dir)

    for directory in dirs_to_search:
        for root, _, files in os.walk(directory):
            for file in files:
                if (file.endswith('.pdf') or file.endswith('.docx')) and search_term in file.lower():
                    found_files.append(os.path.join(root, file))
    
    if not found_files:
        return None
        
    # Return the most recently modified file that matches
    found_files.sort(key=os.path.getmtime, reverse=True)
    return found_files[0]

def ask_gemini(document_text, question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Truncate text to avoid overloading the API
    truncated_text = document_text[:30000]
    
    prompt = f"You are Bixby, an AI assistant. Use the following document text to answer the user's question concisely in 2-3 sentences. \n\nDocument Text:\n{truncated_text}\n\nQuestion: {question}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        return "I had trouble analyzing the document."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python study_assistant.py <filename_search_term> <question>")
        sys.exit(1)
        
    file_query = sys.argv[1]
    question = sys.argv[2]
    
    # Default search directory is the user's Documents folder
    documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')
    
    target_file = find_file(file_query, documents_dir)
    
    if not target_file:
        print(f"I couldn't find any PDF or Word documents matching '{file_query}' in your Documents folder.")
        sys.exit(0)
        
    print(f"Analyzing {os.path.basename(target_file)}...")
    
    if target_file.endswith('.pdf'):
        doc_text = extract_text_from_pdf(target_file)
    elif target_file.endswith('.docx'):
        doc_text = extract_text_from_docx(target_file)
    else:
        print("Unsupported file type.")
        sys.exit(0)
        
    if "Error reading" in doc_text:
        print(doc_text)
        sys.exit(0)
        
    answer = ask_gemini(doc_text, question)
    
    # Print a clear separator so the orchestrator can easily grab the final answer
    print("\n--- BIXBY RESPONSE ---")
    print(answer)