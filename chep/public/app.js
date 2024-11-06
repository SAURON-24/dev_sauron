const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();
const port = 3000;
const apiUrl = 'http://3.38.221.183:8000/nfc';  // FastAPI 서버 URL

app.use(express.static('public'));

app.get('/tags', async (req, res) => {
  try {
    const response = await axios.get(apiUrl);
    res.json(response.data);
  } catch (error) {
    res.status(500).send('Error fetching tags');
  }
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
