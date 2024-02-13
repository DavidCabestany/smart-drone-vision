const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json()); // for parsing application/json

// Endpoint to start the video stream
app.post('/api/start-stream', (req, res) => {
    const streamUrl = req.body.streamUrl || process.env.STREAM_URL;
    // Here you would call your Python script with the necessary arguments
    const pythonProcess = spawn('python', ['..\model\streamRSTP_for_tk2.py', streamUrl]);
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    res.json({ message: 'Stream started', pid: pythonProcess.pid });
});

// Endpoint to stop the video stream
app.post('/api/stop-stream', (req, res) => {
    const pid = req.body.pid;
    process.kill(pid);
    res.json({ message: 'Stream stopped' });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
