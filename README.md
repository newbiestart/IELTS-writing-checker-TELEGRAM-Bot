📄 README.md
# 📚 IELTS Writing Checker Bot  

A **Telegram bot** built with **Python (aiogram)** that evaluates IELTS Writing Task 1 and Task 2 essays using the **Gemini 2.0 Flash API**.  
The bot acts like a **real IELTS examiner**, providing detailed feedback and band score estimations.  

---

## ✨ Features
- 📝 **IELTS Writing Task 1 Evaluation**: Upload a graph/chart image and essay; get a full analysis and score.  
- 📝 **IELTS Writing Task 2 Evaluation**: Enter a topic and essay; receive detailed feedback and band score.  
- 🔐 **Mandatory Channel Subscription**: Users must join a specific Telegram channel before accessing the bot’s features.  
- 🔑 **Secure Credentials**: Tokens and API keys stored in `.env`.  
- 📱 **User-Friendly Menu**: Simple keyboard buttons for easy navigation.

---

## 🚀 Tech Stack
- **Language**: Python 3.10+  
- **Telegram Bot Framework**: [aiogram](https://docs.aiogram.dev/)  
- **AI API**: [Gemini 2.0 Flash](https://ai.google.dev/gemini-api)  
- **Environment Management**: python-dotenv  
- **HTTP Requests**: requests  

---

## 📂 Project Structure


- **bot/**
- **├── main.py # Main bot logic**
- **├── config.py # Config loader**
- **├── .env # Environment variables (not shared)**
- **└── requirements.txt # Project dependencies**


---

## 🔑 Setup Instructions

### 1️⃣ Clone the Repository

- ** git clone https://github.com/yourusername/ielts-writing-bot.git **
- ** cd ielts-writing-bot **

##  ️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

##  3️⃣ Install Dependencies
pip install -r requirements.txt

##  4️⃣ Create .env File

Create a .env file in the root directory and add your credentials:

- BOT_TOKEN=your_telegram_bot_token
- GEMINI_API_KEY=your_gemini_api_key
- CHANNEL_USERNAME=@IELTS_checker

## 5️⃣ Run the Bot
python main.py

---

## 🤖 How to Use

Start the bot with /start.

Press IELTS check to access evaluation options.

Choose Task 1 or Task 2:

For Task 1: Upload a chart/graph image and your essay.

For Task 2: Send a topic and your essay.

The bot will analyze and score your writing using Gemini AI.

If you're not subscribed to the Telegram channel, you'll be prompted to join

---

## 🛠️ Requirements

Python 3.10+

A valid Telegram bot token (get from BotFather
)

A Gemini API key (get from Google AI Studio
)

---

## 📌 Roadmap

 Add conversation history storage (SQLite/Firestore)

 Support for multiple channels or groups

 Add inline feedback improvements

 Deploy to a server (Heroku, Render, or VPS)

---

## 🤝 Contributing

Contributions are welcome!
If you’d like to add features or fix bugs:

Fork the repository

Create a new branch (git checkout -b feature/YourFeature)

Commit changes (git commit -m "Added some feature")

Push to the branch (git push origin feature/YourFeature)

Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.

---

## 👨‍💻 Author

Azamatjon
Passionate about technology, AI, and education.

## Telegram: @IELTS_checker
