🤖 AI Interview Assistant

An AI-powered interview assistant built with Next.js, Python, and Gemini Pro 🚀. It listens to interview questions in real-time and provides on-screen suggestions to help you ace any job interview. Features secure authentication with Supabase and a modern, responsive UI.

✨ Key Features

Real-Time AI Suggestions: Get live AI suggestions during your interviews.

User Authentication: Secure login/signup using Supabase.

Modern UI/UX: Clean, responsive, dark-mode first design.

Session Management: Manage and track your interview sessions.

Custom API Key: Save your own Gemini API key.

🛠️ Tech Stack

Frontend: Next.js, TypeScript, Tailwind CSS

Backend: Python, FastAPI, WebSockets

Database & Auth: Supabase

AI: Google Gemini Pro

Speech-to-Text: Google Cloud Speech-to-Text

🚀 Getting Started

Prerequisites

Node.js (v18+)

Python (v3.10+)

npm or yarn

Installation

Clone the repository:

git clone [https://github.com/your-username/ai-interview-assistant.git](https://github.com/your-username/ai-interview-assistant.git)
cd ai-interview-assistant


Setup Frontend:

npm install
# Create .env.local and add Supabase keys


Setup Backend:

cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Create .env and add API keys


Run the application:

Start the backend server: uvicorn main:app --reload

Start the frontend server: npm run dev