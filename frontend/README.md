🤖 AI Interview Assistant - Frontend

Yeh project AI Interview Assistant ka official frontend hai. Isse Next.js 14 (App Router), TypeScript, aur Tailwind CSS ka use karke banaya gaya hai.
✨ Key Features (Mukhya Visheshtayein)

    Real-Time AI Suggestions: Live interview ke dauran AI se real-time mein suggestions prapt karein.

    User Authentication: Supabase ka use karke secure login aur signup functionality.

    Modern UI/UX: Clean, responsive, aur dark-mode first design jo har device par accha dikhe.

    Session Management: Apne interview sessions ko manage aur track karein.

    Custom API Key: Users apni khud ki Gemini API key save kar sakte hain.

🛠️ Tech Stack (Istemal Ki Gayi Technologies)

    Framework: Next.js 14

    Language: TypeScript

    Styling: Tailwind CSS

    UI Components: Shadcn UI

    Backend Service: Supabase (Auth & Database)

    Icons: Lucide React

🚀 Getting Started (Shuru Kaise Karein)

Is project ko apne local machine par chalane ke liye neeche diye gaye steps follow karein.
Prerequisites (Zaroori Cheezein)

    Node.js (v18 ya usse upar)

    npm ya yarn

Installation (Kaise Install Karein)

    Repository ko Clone karein:

    git clone [https://github.com/your-username/ai-interview-assistant.git](https://github.com/your-username/ai-interview-assistant.git)
    cd ai-interview-assistant

    Dependencies Install karein:

    npm install
    # ya
    yarn install

    Environment Variables Set karein:
    Project ke root mein .env.local naam ki ek file banayein aur usmein .env.example file se content copy karein.

    .env.local

    NEXT_PUBLIC_SUPABASE_URL="Aapke_Supabase_Project_Ka_URL"
    NEXT_PUBLIC_SUPABASE_ANON_KEY="Aapke_Supabase_Project_Ki_Anon_Key"

    Aapko yeh keys aapke Supabase project ki settings mein mil jayengi.

    Development Server Chalu karein:

    npm run dev

    Ab browser mein http://localhost:3000 open karein.

📁 Folder Structure (Folder Ka Dhaancha)

.
├── app/              # Saare routes aur pages (App Router)
│   ├── (auth)/       # Login/Signup pages ka group
│   └── (app)/        # Dashboard/Protected pages ka group
├── components/       # Saare reusable React components
│   ├── features/     # Bade features jaise AuthForm, InterviewWidget
│   ├── shared/       # Navbar, Footer jaise shared components
│   └── ui/           # Basic UI elements (Button, Card, Input)
├── lib/              # Helper functions aur external clients (Supabase, utils)
└── ...

🤝 How to Contribute (Yogdaan Kaise Dein)

Contributions ka swagat hai! Agar aap is project mein yogdaan dena chahte hain, toh please ek Pull Request banayein.

    Project ko Fork karein.

    Ek nayi Feature Branch banayein (git checkout -b feature/AmazingFeature).

    Apne changes Commit karein (git commit -m 'Add some AmazingFeature').

    Branch ko Push karein (git push origin feature/AmazingFeature).

    Ek Pull Request open karein.

📜 License

Yeh project MIT License ke antargat license प्राप्त hai.