

Welcome to my AI-powered personal assistant, built using **Gradio**, **Gemini API**, and **Pushover** for real-time notifications. This assistant is designed to simulate a professional conversation with me — Akshaykarthick — about my **career**, **background**, **projects**, and **skills**.

---

## 🚀 Live Demo

🔗 [Launch the App](https://huggingface.co/spaces/AKS1432/personal-ai-agent)
<img width="1709" height="958" alt="image" src="https://github.com/user-attachments/assets/6e461822-3ad2-4215-8436-d2b10e644183" />




---

## 🧠 About This Project

This app uses **Google Gemini (via OpenAI-compatible endpoint)** to power a chatbot that acts as a virtual version of me. It's ideal for potential clients, employers, or collaborators who want to:

- Learn about my background and expertise  
- Discover my projects and experiences  
- Leave their email and get in touch  
- Ask career-related questions

---

## 💼 Features

- ✅ **Personalized context** from `summary.txt` and resume (`me/Akshaykarthick_s.pdf`)
- ✅ **Gradio ChatInterface** for a clean and interactive UI
- ✅ **Tool use detection** (e.g., record email or unknown question)
- ✅ **Real-time notifications** via **Pushover**
- ✅ **Environment-configured secrets** using `.env`

---
```
📁 project-root/
│   ├── app.py                   # Main Python app with Gradio interface
│   ├── README.md                # Project README (this file)
│   └── 📁 me/
│       ├── Akshaykarthick_s.pdf  # Your resume (used for chatbot context)
│       └── summary.txt           # Text summary of your background
├── .env                        # Environment variables (NOT to be pushed to Git)

```
---
```env
HF_TOKEN=hf_...
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_key  # optional for fallback
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_USER=your_pushover_user_key

