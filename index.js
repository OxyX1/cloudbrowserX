const express = require('express');
const http = require('http');
const path = require('path');
const WebSocket = require('ws');
const puppeteer = require('puppeteer');
const { createCanvas } = require('canvas');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let browser; page;

async function start() {
    browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
    page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto('https://example.com');
}

wss.on('connection', async (ws) => {
    console.log('Client connected');
    if (!browser) await startBrowser();
    
    setInterval(async () => {
        const screenshot = await page.screenshot();
        ws.send(screenshot);
    }, 500);
    
    ws.on('message', async (msg) => {
        const { type, data } = JSON.parse(msg);
        if (type === 'navigate') {
            await page.goto(data);
        }
    });
});

server.listen(8080, () => { console.log('server running on port 8080'); });


const frontendHTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cloud Browser</title>
</head>
<body>
    <canvas id="screen" width="1280" height="720"></canvas>
    <input id="url" type="text" placeholder="Enter URL" />
    <button onclick="navigate()">Go</button>
    <script>
        const canvas = document.getElementById('screen');
        const ctx = canvas.getContext('2d');
        const socket = new WebSocket('ws://localhost:3000');

        socket.onmessage = (event) => {
            const img = new Image();
            img.src = URL.createObjectURL(new Blob([event.data]));
            img.onload = () => ctx.drawImage(img, 0, 0);
        };
        
        function navigate() {
            const url = document.getElementById('url').value;
            socket.send(JSON.stringify({ type: 'navigate', data: url }));
        }
    </script>
</body>
</html>`;

require('fs').writeFileSync('browser/client.html', frontendHTML);
