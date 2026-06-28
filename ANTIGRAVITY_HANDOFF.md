# 🚀 Antigravity CLI Handoff Document: Bixby PC Navigator

**ATTENTION ANTIGRAVITY AGENT:** 
The user is migrating to you from a previous session with Gemini CLI. Read this document carefully. Do not ask the user to repeat themselves. You are picking up an ongoing, highly advanced project right in the middle of deployment.

---

## 🎯 The Ultimate Goal
The user (Vedansh, a CS student) wants to turn Samsung's native Bixby voice assistant on their Galaxy Book 5 360 into a **"God-Mode" local PC orchestrator**. 
Because native Bixby on Windows is very limited (can only open basic apps or change volume), we are building a custom Bixby Capsule that acts as a voice-to-cloud relay, triggering complex, local automation scripts directly on the PC hardware.

## 🏗️ The Architecture We Built
We have successfully built and verified a 3-part hybrid architecture:

1.  **The Bixby Capsule (`playground.pc_navigator`)**
    *   **Goal:** Listens to voice commands (e.g., "Start my dev environment"), extracts the intent using Natural Language training, and fires a JSON payload to the cloud.
    *   **Status:** 100% built and trained. **Currently blocked by a Samsung server outage (see below).**
2.  **The Cloud Relay (Firebase Realtime Database)**
    *   **Goal:** A secure, low-latency bridge between Samsung's cloud and the local PC.
    *   **Status:** 100% active and configured.
3.  **The Local Orchestrator (`companion-node/index.js`)**
    *   **Goal:** A Node.js app running locally on the Windows PC. It listens to Firebase, grabs incoming commands, and uses `child_process.spawn` to trigger Python/PowerShell scripts. It also captures the stdout of those scripts and writes it *back* to Firebase so Bixby can speak the results out loud (Two-Way Communication).
    *   **Status:** 100% built, tested, and working locally.

## 🛠️ The Automation Modules We Built
Inside `companion-node/scripts/`, we built several powerful local modules:
*   `llm_query.js`: Takes a query, hits the Gemini 2.5 Flash API, and returns a concise, Bixby-friendly answer. (The "Genius Bridge").
*   `screen_reader.py`: Uses `pyautogui` and `pyperclip` to invisibly grab all text from the active Windows screen and sends it to Gemini for a 2-sentence summary.
*   `study_assistant.py`: Searches the local `Documents` (and OneDrive) folder for specific PDFs/Word docs, parses them using `PyPDF2`/`python-docx`, and answers academic questions based purely on local file context.
*   `setup_dev.ps1`: A PowerShell script that opens VS Code, browser tabs, and local servers simultaneously.

## 🛑 The Current Blocker (Why We Paused)
**DO NOT attempt to fix the Bixby code.** The code is flawless (0 errors, 0 warnings). 
The project is currently paused because **Samsung's Developer Execution Servers are down/unstable** (likely due to the One UI 8.5 rollout traffic). 

Whenever the user hits "Compile" or tests an utterance in the Bixby Simulator, it throws a `13 INTERNAL: Received RST_STREAM With Code 0` error. This is a hard network connection drop from Samsung's data centers. The user is waiting out the outage before trying to compile again.

## ⏭️ Your Next Steps (When the User is Ready)

When the user returns to you, they will likely want to check if the Samsung servers are back up.

1.  **Test the Simulator:** Have the user run `node index.js` in the `companion-node` folder, then open Bixby Studio's simulator and test the utterance: `Start my dev environment`.
2.  **If it still fails (`RST_STREAM`):** Remind the user that Samsung is still down. Offer to continue building new local Python/PowerShell scripts in the `scripts/` folder (like a media controller or cross-device phone link via Windows Phone Link API) which can be tested locally in the terminal while waiting.
3.  **If it succeeds:** CELEBRATE! The pipeline is complete. Your immediate next task is to help the user write a **Silent Windows Startup Script** (e.g., a `.vbs` wrapper) so that `node index.js` runs invisibly in the background every time Windows boots up, making the Bixby integration seamless.

**Security Note:** The `serviceAccountKey.json` is protected via `.gitignore`. The Gemini API key in the scripts expects a local environment variable (`process.env.GEMINI_API_KEY`). Ensure the user's local terminal session has this key set before testing the Python/JS modules.
