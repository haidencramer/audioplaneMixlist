const functions = require("firebase-functions");
const { spawn } = require("child_process");
const path = require("path");

exports.app = functions.https.onRequest((req, res) => {
  const backendPath = path.resolve(__dirname, "../backend");

  const uvicorn = spawn(
    "uvicorn",
    ["main:app", "--host", "127.0.0.1", "--port", "8000"],
    {
      cwd: backendPath,
      shell: true,
      env: { ...process.env },
    }
  );

  uvicorn.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
  });

  uvicorn.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  // Optional: either return early or wait for FastAPI to respond
  res.send("FastAPI server is starting...");
});
