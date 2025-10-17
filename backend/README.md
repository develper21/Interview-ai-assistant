# AI Interview Assistant Backend

यह backend FastAPI का उपयोग करके बनाया गया है जो real-time audio streaming को Google Speech-to-Text और Google Gemini Pro के साथ integrate करता है।

## 🚀 Features

- **Real-time WebSocket Communication**: Frontend के साथ live audio streaming
- **Google Speech-to-Text Integration**: Audio को text में convert करने के लिए
- **Google Gemini Pro Integration**: AI-powered interview suggestions generate करने के लिए
- **Error Handling**: Robust error handling और connection management

## 📋 Prerequisites

- Python 3.10+
- Google Cloud Speech-to-Text API key
- Google Gemini Pro API key

## 🛠️ Installation

1. **Virtual Environment बनाएं:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# या
venv\Scripts\activate  # Windows
```

2. **Dependencies Install करें:**
```bash
pip install -r requirements.txt
```

3. **Environment Variables Setup करें:**

`.env` file में अपनी API keys डालें:
```bash
GOOGLE_API_KEY="your_gemini_api_key_here"
GOOGLE_APPLICATION_CREDENTIALS="./service_account.json"
```

## 🔑 API Keys Setup

### Google Gemini Pro API Key
1. [Google AI Studio](https://makersuite.google.com/app/apikey) पर जाएं
2. नया API key generate करें
3. `.env` file में `GOOGLE_API_KEY` के रूप में डालें

### Google Cloud Speech-to-Text Setup
1. [Google Cloud Console](https://console.cloud.google.com/) पर जाएं
2. नया project बनाएं या existing project select करें
3. Speech-to-Text API enable करें
4. Service Account बनाएं और JSON key download करें
5. JSON file को `service_account.json` के नाम से backend folder में रखें

## 🎯 Usage

### Backend Start करें:
```bash
uvicorn main:app --reload
```

Server `http://localhost:8000` पर start हो जाएगा।

### WebSocket Endpoint:
- WebSocket: `ws://localhost:8000/ws`

### Frontend के साथ Integration:
Frontend को WebSocket के माध्यम से backend से connect करना चाहिए। InterviewWidget component में पहले से ही यह integration मौजूद है।

## 📁 Project Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this file)
└── service_account.json # Google Cloud credentials (download this file)
```

## 🔧 Configuration

Backend को configure करने के लिए `.env` file में निम्नलिखित variables set करें:

```bash
# Google Gemini Pro API Key
GOOGLE_API_KEY="your_gemini_api_key_here"

# Google Cloud Service Account JSON file path
GOOGLE_APPLICATION_CREDENTIALS="./service_account.json"
```

## 🚨 Troubleshooting

### Common Issues:

1. **WebSocket Connection Failed**: Backend को पहले start करें
2. **Speech-to-Text Not Working**: Service account JSON file सही जगह पर है यह चेक करें
3. **Gemini API Error**: API key valid है यह चेक करें
4. **Audio Format Issues**: Browser में WebM Opus support चेक करें

### Logs देखने के लिए:
Backend console में logs दिखाई देंगे जो connection status और errors show करते हैं।

## 📝 API Endpoints

- **WebSocket**: `ws://localhost:8000/ws`
  - Real-time audio streaming के लिए
  - JSON messages receive/send करता है

## 🔄 Data Flow

1. Frontend microphone से audio capture करता है
2. Audio chunks को WebSocket के माध्यम से backend को भेजता है
3. Backend Google Speech-to-Text API का उपयोग करके audio को text में convert करता है
4. जब complete sentence मिलता है तो Gemini Pro को prompt भेजता है
5. AI suggestion generate होकर WebSocket के माध्यम से frontend को वापस भेजी जाती है

## 🧪 Testing

Backend को test करने के लिए:

1. Backend start करें
2. Browser में WebSocket connection test करें
3. Audio recording test करें
4. Real-time suggestions चेक करें

## 🤝 Contributing

इस project में contribute करने के लिए:

1. Feature branch बनाएं
2. Changes करें
3. Test करें
4. Pull request बनाएं

## 📄 License

यह project MIT license के तहत है।
