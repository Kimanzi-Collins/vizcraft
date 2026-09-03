#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const generatePy = path.join(__dirname, '..', 'generate.py');
const args = [generatePy, ...process.argv.slice(2)];

const py = spawn('python', args, { stdio: 'inherit' });

py.on('error', (err) => {
  if (err.code === 'ENOENT') {
    // Try python3 if python is not found
    const py3 = spawn('python3', args, { stdio: 'inherit' });
    py3.on('error', (e) => {
      console.error('Error: Python 3 is required to run VizCraft.');
      process.exit(1);
    });
    py3.on('close', (code) => process.exit(code));
  } else {
    console.error(`Failed to start VizCraft: ${err.message}`);
    process.exit(1);
  }
});

py.on('close', (code) => {
  process.exit(code);
});
