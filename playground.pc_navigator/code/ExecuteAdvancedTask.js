import http from 'http';
import console from 'console';

export default function executeAdvancedTask(input) {
  console.log("Input received:", input);
  
  const complexTask = input ? input.complexTask : "None";
  const targetScript = input ? input.targetScript : "None";
  const parameters = input ? input.parameters : "None";

  // Replace with your actual Firebase Realtime Database URL
  const firebaseUrl = "https://bixby-pc-navigator-default-rtdb.firebaseio.com/commands.json";
  
  let payload = {
    "complexTask": String(complexTask),
    "targetScript": String(targetScript),
    "parameters": String(parameters)
  };

  try {
    console.log("Sending payload to Firebase:", payload);
    const response = http.postUrl(firebaseUrl, payload, { passAsJson: true, format: 'json', returnHeaders: true });
    console.log("Firebase response status:", response.status);
    
    return {
      success: true,
      message: "Command sent to PC successfully."
    };
  } catch (e) {
    console.error("HTTP error:", e);
    return {
      success: false,
      message: "Failed to send command to PC."
    };
  }
}