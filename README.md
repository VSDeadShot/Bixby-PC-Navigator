# Bixby PC Navigator - AI Local Companion

Bixby PC Navigator is an advanced, two-way bridge that transforms Samsung's Bixby voice assistant into a powerful, locally executing AI orchestrator for your Windows PC. 

By bypassing the limitations of native Bixby desktop controls, this project connects a custom Bixby Developer Studio capsule to a local Node.js server via a secure Firebase Realtime Database relay. This allows Bixby to execute complex Python and PowerShell scripts, interact with your active screen, and analyze local documents using the Google Gemini 2.5 LLM.

## 🚀 Key Features

* **Cloud-to-Local Bridge:** Instantly relays voice commands from any Bixby-enabled device (Galaxy Book, Phone, Watch) directly to your local PC's command line.
* **Two-Way Communication:** The Node.js orchestrator captures terminal output and sends it back to the cloud, allowing Bixby to speak the results out loud.
* **Genius LLM Bridge:** Ask complex coding or academic questions via voice; the local `llm_query.js` script fetches answers from Google's Gemini 2.5 Flash model and Bixby reads them back.
* **Context-Aware Screen Reader:** A Python automation script (`screen_reader.py`) that captures the text of your active window and uses AI to summarize it in a Bixby-friendly format.
* **Local Study Assistant:** A Python document parser (`study_assistant.py`) that instantly searches your local Documents folder for PDFs or Word files, reads them, and answers your specific questions about the text.

## 🛠️ Prerequisites

1. **Bixby Developer Studio:** To compile and publish the voice capsule.
2. **Node.js (v16+)**: To run the local orchestrator (`index.js`).
3. **Python 3.10+**: To execute the local AI automation scripts.
4. **Firebase Account**: A free Firebase Realtime Database to act as the secure cloud relay.
5. **Google AI Studio Key**: A free API key to power the local Gemini 2.5 models.

## 📦 Installation & Setup

### 1. Set up the Cloud Relay (Firebase)
1. Create a Firebase project and a Realtime Database.
2. Generate a Private Key from **Project Settings -> Service Accounts**.
3. Save the downloaded file as `serviceAccountKey.json` inside the `companion-node/` directory. *(Note: This file is ignored by git for security).*

### 2. Set up the Local Environment
Clone the repository and install the Node.js and Python dependencies.

```bash
git clone <your-repo-url>
cd bixby-workspace/companion-node

# Install Node Orchestrator dependencies
npm install firebase-admin

# Install Python Automation dependencies
pip install pyautogui pyperclip PyPDF2 python-docx
```

### 3. Configure the AI Keys
For security, the Gemini API key is loaded via environment variables. Set this in your Windows terminal before running the scripts:

**PowerShell:**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Orchestrator
Start the local Node.js server to begin listening for Bixby commands:
```bash
node index.js
```

## 🧠 Bixby Capsule Structure
The `playground.pc_navigator` folder contains the Bixby Developer Studio code. 
* **Models:** Defines `ComplexTask` (Enum), `TargetScript`, and `TaskResult`.
* **Actions:** `ExecuteAdvancedTask.js` uses `http.postUrl` to send the JSON payload to the Firebase database.
* **Training:** Natural language utterances are mapped to the `ExecuteAdvancedTask` goal via the Bixby GUI.

*(Note: Ensure you update the `firebaseUrl` variable inside `code/ExecuteAdvancedTask.js` with your specific database URL).*
