// index.js
const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();
const port = 3000;
const apiUrl = 'http://3.38.221.183:8000';  // FastAPI 서버 URL

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

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
