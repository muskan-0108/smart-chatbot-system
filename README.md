# 🤖 Smart FAQ Chatbot System - Complete Setup Guide

## Project Overview

This is a **beginner-friendly, full-stack chatbot project** that uses simple rule-based logic to answer frequently asked questions. Perfect for your resume!

### Key Features:
✅ **Chat Interface** - Ask questions, get instant answers  
✅ **FAQ Database** - Stores questions and answers  
✅ **Self-Learning** - Records unknown questions for admin to answer  
✅ **Chat History** - Saves all conversations  
✅ **Admin Panel** - Add new Q&A pairs manually  
✅ **No AI/ML** - Simple, beginner-friendly logic  
✅ **No External Database** - Uses SQLite (included with Python)

---

## 📁 Project Structure

```
smart_chatbot/
│
├── app.py                    # Flask application (main server)
├── database.py               # Database operations
├── requirements.txt          # Python dependencies
│
├── templates/
│   └── index.html           # Chat UI (HTML)
│
├── static/
│   ├── style.css            # Styling (CSS)
│   └── script.js            # Frontend logic (JavaScript)
│
└── database.db              # SQLite database (created automatically)
```

---

## 🚀 Step-by-Step Setup Instructions (Windows)

### **STEP 1: Open VS Code and Terminal**

1. Open **VS Code**
2. Open the terminal: `Ctrl + ~` (or go to Terminal → New Terminal)
3. The terminal should open in your current workspace directory

### **STEP 2: Navigate to Project Directory**

If you created the project at `C:/smart_chatbot`, run:

```powershell
cd C:\smart_chatbot
```

To verify you're in the right place, run:
```powershell
dir
```

You should see these files:
- app.py
- database.py
- requirements.txt
- templates/ (folder)
- static/ (folder)

### **STEP 3: Create Virtual Environment**

A virtual environment keeps dependencies isolated and clean.

**Run this command:**
```powershell
python -m venv venv
```

This creates a `venv` folder with Python installed.

**⏳ Wait 30-60 seconds for it to complete!**

### **STEP 4: Activate Virtual Environment**

Your command prompt will now show `(venv)` prefix if successful.

**Run this command:**
```powershell
.\venv\Scripts\activate
```

**After running, you should see:**
```
(venv) C:\smart_chatbot>
```

> **Note:** Every time you open a new terminal, you must activate the venv again!

### **STEP 5: Install Python Dependencies**

Now install Flask (the web framework).

**Run this command:**
```powershell
pip install -r requirements.txt
```

**What it installs:**
- Flask (web framework)
- Werkzeug (Flask dependency)

**You should see output like:**
```
Successfully installed Flask-2.3.3 Werkzeug-2.3.7
```

**⏳ This takes 1-2 minutes depending on your internet speed**

### **STEP 6: Run the Flask Application**

Everything is ready! Start the server:

**Run this command:**
```powershell
python app.py
```

**You should see output like:**
```
============================================================
🤖 Smart FAQ Chatbot System Starting...
============================================================
📍 Open your browser and go to: http://localhost:5000
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🌐 STEP 7: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://localhost:5000**
3. You should see the chatbot interface!

---

## 💬 Testing the Chatbot

### Try These Questions:

1. **"What is this chatbot?"**
   - ✅ Should return the stored answer

2. **"How does it work?"**
   - ✅ Should return the stored answer

3. **"Tell me a joke"**
   - ❌ Not in database → Will save to "unknown questions"

4. **Scroll down to Admin Panel** → Add answer for "Tell me a joke"

After adding an answer, ask "Tell me a joke" again → Now it will respond!

---

## 🛑 Stopping the Server

When you want to stop the chatbot:

**Press in the terminal:**
```
Ctrl + C
```

You should see:
```
Shutting down...
```

---

## 🔄 How to Run Again (Next Time)

If you close VS Code and want to run the chatbot again:

1. Open VS Code in the `smart_chatbot` folder
2. Open terminal: `Ctrl + ~`
3. **Activate venv:**
   ```powershell
   .\venv\Scripts\activate
   ```
4. **Run the app:**
   ```powershell
   python app.py
   ```
5. **Open browser:** http://localhost:5000

---

## 🐛 Troubleshooting

### ❌ Error: "python is not recognized"

**Solution:** Python is not installed on your system.
- Download from: https://www.python.org/downloads/
- When installing, **CHECK** "Add Python to PATH"
- Then try again

### ❌ Error: "Cannot activate virtual environment"

**Solution:** You're using wrong command. For Windows PowerShell:
```powershell
.\venv\Scripts\activate
```

For Command Prompt (cmd):
```cmd
venv\Scripts\activate.bat
```

### ❌ Error: "Module 'flask' not found"

**Solution:** Virtual environment not activated OR pip install failed.
- Make sure you see `(venv)` in your command prompt
- Run: `pip install -r requirements.txt` again

### ❌ Error: "Port 5000 is already in use"

**Solution:** Another application is using port 5000.
- Close other Flask apps running
- Or kill the process:
  ```powershell
  Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process
  ```

### ❌ Browser shows "Connection refused"

**Solution:** Flask server is not running.
- Check terminal shows: `Running on http://127.0.0.1:5000`
- If not, run: `python app.py`

### ❌ Database errors or questions not saving

**Solution:** Delete `database.db` and restart:
1. Stop Flask (Ctrl + C)
2. Delete `database.db` from the project folder
3. Run: `python app.py`
4. Database will be recreated with sample FAQs

---

## 📚 Understanding the Code

### **app.py** (Main Application)
- Handles web requests
- Manages chat API
- Connects to database

### **database.py** (Database Logic)
- Creates tables
- Searches FAQ
- Saves conversations
- Allows admin to add answers

### **index.html** (Chat Interface)
- HTML structure
- Chat bubbles
- Admin panel

### **style.css** (Styling)
- Colors and layout
- Responsive design
- Beautiful gradients

### **script.js** (Frontend Logic)
- Handles button clicks
- Sends messages to server
- Displays chat bubbles
- Loads unknown questions

---

## 🎯 How It Works (Simplified)

```
User Types Question
        ↓
JavaScript catches it (script.js)
        ↓
Sends to Flask server (/api/chat)
        ↓
Flask searches database (database.py)
        ↓
Found? → Return answer
Not found? → Save to unknown_questions table
        ↓
JavaScript displays response
        ↓
Question saved to chat_history
```

---

## 📊 Database Schema

### **faq table**
```
id        | question              | answer
---------|----------------------|--------
1        | What is this chatbot  | This is...
2        | How does it work      | I search...
```

### **unknown_questions table**
```
id | question           | created_at
---|------------------|----------
1  | Tell me a joke    | 2024-03-07...
```

### **chat_history table**
```
id | user_question | bot_answer | created_at
---|---------------|-----------|----------
1  | What is...    | This is.. | 2024-03-07...
```

---

## 🎓 Learning Outcomes

By completing this project, you understand:

✅ **Flask Basics** - Creating web servers
✅ **REST APIs** - How frontend talks to backend
✅ **SQLite Database** - Storing and querying data
✅ **HTML/CSS/JavaScript** - Building UIs
✅ **Frontend-Backend Communication** - fetch API, JSON
✅ **Virtual Environments** - Python dependency management

---

## 💡 Project Ideas to Extend

1. **Add search filtering** - Search FAQs by keyword
2. **User authentication** - Login system for admins
3. **Statistics** - Show most asked questions
4. **Export data** - Download chat history as CSV
5. **Multiple languages** - Support different languages
6. **Fuzzy matching** - Find similar questions (e.g., "What is this bot?" matches "What is this chatbot?")

---

## 🎯 For Your Resume

When adding this to your resume, mention:

**Smart FAQ Chatbot System**
- Developed a rule-based chatbot using Flask and SQLite
- Built responsive web UI with HTML, CSS, and JavaScript
- Implemented self-learning functionality by saving unknown questions
- Created admin panel for managing FAQ database
- 100% beginner-friendly, no ML/AI libraries

**Tech Stack:** Python, Flask, SQLite, HTML5, CSS3, JavaScript

---

## 📝 License

This project is free to use for learning and resume purposes!

---

## ❓ Need Help?

If you have questions:

1. **Check the code comments** - Every function has explanations
2. **Check this troubleshooting guide** - Most issues are covered
3. **Review the file comments** - Each file explains what it does

**Happy Coding!** 🚀

