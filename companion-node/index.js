const admin = require('firebase-admin');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Path to the service account key (you must generate this from Firebase Console)
const serviceAccountPath = path.join(__dirname, 'serviceAccountKey.json');

if (!fs.existsSync(serviceAccountPath)) {
  console.error("ERROR: serviceAccountKey.json is missing!");
  console.error("Please download it from Firebase Console -> Project Settings -> Service Accounts -> Generate New Private Key");
  console.error(`And place it in: ${__dirname}`);
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

// Initialize Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  // REPLACE THIS with your actual Firebase Database URL
  databaseURL: process.env.FIREBASE_DB_URL || "https://YOUR-PROJECT-ID.firebaseio.com" 
});

const db = admin.database();
const commandsRef = db.ref('commands');

console.log('Advanced Bixby PC Navigator Companion App is running...');
console.log('Listening for commands from Firebase...\n');

// Listen for new child added to /commands
commandsRef.on('child_added', (snapshot) => {
  const commandId = snapshot.key;
  const commandData = snapshot.val();
  
  if (!commandData) return;

  console.log(`[${new Date().toLocaleTimeString()}] Received new command (${commandId}):`);
  console.log(commandData);

  // Determine what to execute based on the payload
  const { complexTask, targetScript, parameters } = commandData;

  let scriptToRun = null;
  let args = [];

  // Map high level complex tasks to specific scripts, or use targetScript directly if provided
  if (targetScript) {
    scriptToRun = targetScript;
  } else if (complexTask) {
    switch (complexTask.toLowerCase()) {
      case 'dev environment':
        scriptToRun = 'setup_dev.ps1';
        break;
      case 'log analysis':
        scriptToRun = 'log_analysis.ps1';
        break;
      case 'server backup':
        scriptToRun = 'backup.ps1';
        break;
      case 'system health':
        scriptToRun = 'health_check.py';
        break;
      default:
        console.log(`Unknown Complex Task: ${complexTask}`);
    }
  }

  if (parameters) {
    args.push(parameters); // Assuming single string parameter for simplicity. Adjust as needed.
  }

  if (scriptToRun) {
    executeScript(scriptToRun, args, commandId);
  } else {
    console.log("No valid script identified for this command.\n");
    // Optionally remove the unhandled command
    commandsRef.child(commandId).remove();
  }
});

function executeScript(scriptName, args, commandId) {
  const scriptsDir = path.join(__dirname, 'scripts');
  const scriptPath = path.join(scriptsDir, scriptName);

  if (!fs.existsSync(scriptPath)) {
    console.error(`Script not found: ${scriptPath}`);
    // Clean up
    commandsRef.child(commandId).remove();
    return;
  }

  console.log(`Executing: ${scriptPath} with args: ${args}`);

  let processObj;
  
  // Determine runner based on extension
  const ext = path.extname(scriptName).toLowerCase();
  if (ext === '.ps1') {
    // Run PowerShell script bypassing execution policy for this process
    processObj = spawn('powershell.exe', ['-ExecutionPolicy', 'Bypass', '-File', scriptPath, ...args]);
  } else if (ext === '.py') {
    processObj = spawn('python', [scriptPath, ...args]);
  } else if (ext === '.js') {
    processObj = spawn('node', [scriptPath, ...args]);
  } else if (ext === '.bat' || ext === '.cmd') {
      processObj = spawn('cmd.exe', ['/c', scriptPath, ...args]);
  } else {
    console.error(`Unsupported script extension: ${ext}`);
    commandsRef.child(commandId).remove();
    return;
  }

  let scriptOutput = "";

  processObj.stdout.on('data', (data) => {
    console.log(`STDOUT: ${data}`);
    scriptOutput += data.toString();
  });

  processObj.stderr.on('data', (data) => {
    console.error(`STDERR: ${data}`);
  });

  processObj.on('close', (code) => {
    console.log(`Script finished with exit code ${code}\n`);
    
    // Send response back to Firebase
    db.ref(`responses/${commandId}`).set({
      result: scriptOutput.trim() || "Task completed.",
      timestamp: admin.database.ServerValue.TIMESTAMP
    }).then(() => {
      console.log(`Response sent to cloud for command ${commandId}.`);
      return commandsRef.child(commandId).remove();
    }).then(() => {
      console.log(`Command ${commandId} removed from queue.`);
    }).catch((err) => {
      console.error(`Failed to handle completion: ${err}`);
    });
  });
}
