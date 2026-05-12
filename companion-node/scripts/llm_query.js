// llm_query.js
// This script takes a question as an argument, asks Google's Gemini API, and prints the response.

const apiKey = process.env.GEMINI_API_KEY || "YOUR_GEMINI_API_KEY_HERE"; // Set this in your environment variables
const question = process.argv[2];

if (!question) {
  console.log("Error: Please provide a question as an argument.");
  process.exit(1);
}

async function askGemini() {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  
  const payload = {
    contents: [{
      parts: [{ text: "You are Bixby, a helpful AI PC assistant. Please answer this question concisely in 2 or 3 sentences so it can be read out loud easily: " + question }]
    }]
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (data.error) {
      console.log("Error from Gemini API:", data.error.message);
    } else {
      const answer = data.candidates[0].content.parts[0].text;
      // Just log the raw answer. Our index.js orchestrator captures this stdout and sends it to Bixby!
      console.log(answer.trim());
    }
  } catch (error) {
    console.log("Failed to connect to the LLM:", error.message);
  }
}

askGemini();
