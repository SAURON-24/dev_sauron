const express = require('express');
const axios = require('axios');
const path = require('path');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const port = 3000;
const apiUrl = 'http://3.38.221.183:8000';  // FastAPI 서버 URL

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// 정적 파일 제공 설정
app.use(express.static('public'));

app.get('/detected-objects', async (req, res) => {
    try {
        const response = await axios.get(`${apiUrl}/detected-objects`);
        console.log('Fetched detected objects:', response.data); // 로그 추가
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching detected objects:', error.message); // 에러 로그 추가
        res.status(500).send('Error fetching detected objects');
    }
});

app.post('/clear-detected-objects', async (req, res) => {
    try {
        const response = await axios.post(`${apiUrl}/clear-detected-objects`);
        console.log('Cleared detected objects:', response.data); // 로그 추가
        res.json(response.data);
    } catch (error) {
        console.error('Error clearing detected objects:', error.message); // 에러 로그 추가
        res.status(500).send('Error clearing detected objects');
    }
});

app.post('/start-payment', async (req, res) => {
    try {
        const response = await axios.post(`${apiUrl}/start-payment`);
        console.log('Started payment process:', response.data); // 로그 추가
        res.json(response.data);
    } catch (error) {
        console.error('Error starting payment process:', error.message); // 에러 로그 추가
        res.status(500).send('Error starting payment process');
    }
});

app.post('/confirm-payment', async (req, res) => {
    try {
        const response = await axios.post(`${apiUrl}/confirm-payment`);
        console.log('Payment confirmed:', response.data); // 로그 추가
        res.json(response.data);
    } catch (error) {
        console.error('Error confirming payment:', error.message); // 에러 로그 추가
        res.status(500).send('Error confirming payment');
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', (message) => {
        console.log('Received message:', message);
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});