🚀 Social Media Agent

AI-powered content generator for captions, reels, hashtags & weekly plans — with image captioning support.

⭐ Overview

The Social Media Agent helps creators, influencers, and businesses instantly generate professional, trendy, high-performing social media content using Groq LLMs (LLaMA 3.3 series).

It supports both text-based and image-based caption generation — perfect for daily content creators.

✨ Features

🎭 Multi-Style Captions
Cinematic
Gen-Z
Luxury
Viral-SEO
Storytelling
🎬 Reels Script Generator (Hook, Visuals, VO, CTA)
🔥 Smart Hashtag Sets (High Reach, Medium, Low Competition)
🗓 7-Day Weekly Social Media Plan
📝 Caption Scoring (0–100)
🖼 Image → Caption (Vision Model)
🔐 User Login + Saved History

🛠️ Tech Stack
Backend: Python, Groq API
Frontend: Streamlit
Database: SQLite (user.db)
Storage: JSON for history
Models: LLaMA 3.3 series

📁 Project Structure
app.py
agent.py
ui.py
auth.py
config.py
history.json
user.db
requirements.txt
assets/
   └── architecture.png

⚙️ Setup & Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add .env
GROQ_API_KEY=your_key_here

3️⃣ Run
streamlit run app.py
