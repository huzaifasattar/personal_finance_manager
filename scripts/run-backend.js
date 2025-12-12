#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const backendDir = path.join(__dirname, '..', 'backend');
const isWindows = os.platform() === 'win32';

// Determine Python executable path
let pythonPath;
if (isWindows) {
  pythonPath = path.join(backendDir, 'venv', 'Scripts', 'python.exe');
} else {
  pythonPath = path.join(backendDir, 'venv', 'bin', 'python');
}

// Check if venv exists
const venvExists = fs.existsSync(pythonPath);

if (!venvExists) {
  console.error('❌ Virtual environment not found!');
  console.error('Please run: yarn setup:backend');
  console.error('Or manually: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt');
  process.exit(1);
}

// Get command from arguments (default to 'runserver')
const command = process.argv[2] || 'runserver';
const args = command === 'runserver' 
  ? ['manage.py', 'runserver'] 
  : process.argv.slice(2);

// Spawn the Python process
const pythonProcess = spawn(pythonPath, args, {
  cwd: backendDir,
  stdio: 'inherit',
  shell: false
});

pythonProcess.on('error', (error) => {
  console.error(`❌ Error starting Django server: ${error.message}`);
  process.exit(1);
});

pythonProcess.on('exit', (code) => {
  if (code !== 0 && code !== null) {
    console.error(`❌ Django server exited with code ${code}`);
    process.exit(code);
  }
});

// Handle process termination
process.on('SIGINT', () => {
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});

