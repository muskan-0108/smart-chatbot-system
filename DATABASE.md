# 📊 Database Documentation

## Overview

The chatbot uses **SQLite** database with 3 main tables:

```
smart_chatbot/
└── database.db  ← Created automatically when app runs
```

---

## 📋 Table Schema

### 1. **faq** (Frequently Asked Questions)

Stores all Q&A pairs that the chatbot knows.

```
Column Name  | Type          | Description
-------------|---------------|---------------------------
id           | INTEGER (PK)  | Unique ID (auto-increment)
question     | TEXT (UNIQUE) | User's question
answer       | TEXT          | Chatbot's response
created_at   | TIMESTAMP     | When added to database
```

**Example Data:**
```
1 | "What is this chatbot?" | "This is a Smart FAQ Chatbot System..." | 2024-03-07 10:00:00
2 | "How does it work?" | "I search my FAQ database..." | 2024-03-07 10:00:00
```

---

### 2. **unknown_questions** (Questions Without Answers)

Stores questions the chatbot couldn't answer (for admin to review).

```
Column Name  | Type          | Description
-------------|---------------|---------------------------
id           | INTEGER (PK)  | Unique ID (auto-increment)
question     | TEXT (UNIQUE) | Question user asked
created_at   | TIMESTAMP     | When question was asked
```

**Example Data:**
```
1 | "Tell me a joke" | 2024-03-07 10:15:30
2 | "Can you code?" | 2024-03-07 10:20:15
```

---

### 3. **chat_history** (All Conversations)

Stores every conversation between user and chatbot.

```
Column Name      | Type          | Description
-----------------|---------------|---------------------------
id               | INTEGER (PK)  | Unique ID (auto-increment)
user_question    | TEXT          | What user asked
bot_answer       | TEXT          | What chatbot responded
created_at       | TIMESTAMP     | When conversation happened
```

**Example Data:**
```
1 | "What is this chatbot?" | "This is a Smart FAQ..." | 2024-03-07 10:00:00
2 | "Tell me a joke" | "I don't know this yet..." | 2024-03-07 10:15:30
```

---

## 🔄 How Data Flows

```
User asks "What is this chatbot?"
           ↓
JavaScript sends to Flask
           ↓
Flask searches faq table
           ↓
Found in database!
   Answer: "This is a Smart FAQ..."
           ↓
Question + Answer saved to chat_history
           ↓
Response sent to user
```

```
User asks "Tell me a joke"
           ↓
JavaScript sends to Flask
           ↓
Flask searches faq table
           ↓
NOT found in database!
   Answer: "I don't know this yet..."
           ↓
Question saved to unknown_questions
Question + Answer saved to chat_history
           ↓
Response sent to user
           ↓
Admin sees "Tell me a joke" in unknown questions
Admin adds answer: "Why did the chicken cross the road?"
Question moved from unknown_questions to faq
           ↓
Next time user asks → Answer returned from faq!
```

---

## 💻 Sample SQL Queries

If you want to inspect the database directly:

### View all FAQs
```sql
SELECT * FROM faq;
```

### View all unknown questions
```sql
SELECT * FROM unknown_questions;
```

### View all conversations
```sql
SELECT * FROM chat_history;
```

### Count total conversations
```sql
SELECT COUNT(*) as total_conversations FROM chat_history;
```

### Find questions asked in last 24 hours
```sql
SELECT * FROM chat_history 
WHERE created_at > datetime('now', '-1 day');
```

### Most frequently asked questions
```sql
SELECT user_question, COUNT(*) as count 
FROM chat_history 
GROUP BY user_question 
ORDER BY count DESC;
```

---

## 🎯 Sample FAQ Data

The chatbot comes with 8 pre-loaded FAQs:

1. **"What is this chatbot?"**
   - *Answer:* "This is a Smart FAQ Chatbot System. I can answer frequently asked questions using simple rule-based logic."

2. **"How does this chatbot work?"**
   - *Answer:* "I search my FAQ database for matching questions. If found, I return the stored answer. If not found, I save your question for future learning."

3. **"Can I teach you new questions?"**
   - *Answer:* "Yes! An admin can add new Q&A pairs to my database through the admin feature, and I will learn them automatically."

4. **"What is your name?"**
   - *Answer:* "I am the Smart FAQ Chatbot! I'm here to help you find answers quickly."

5. **"How are you?"**
   - *Answer:* "I'm working perfectly! Thanks for asking. How can I help you today?"

6. **"What technologies do you use?"**
   - *Answer:* "I'm built with Python Flask (backend), SQLite (database), and HTML/CSS/JavaScript (frontend)."

7. **"Is this website secure?"**
   - *Answer:* "This is a demo chatbot for learning purposes. For production use, additional security measures should be implemented."

8. **"Can you do calculations?"**
   - *Answer:* "I can respond to predefined questions in my database, but I don't perform calculations. I use simple rule-based logic."

---

## 🗄️ Database Functions in Code

### **database.py** Functions

#### 1. `init_database()`
Creates all 3 tables when app starts.
```python
init_database()  # Automatically called in app.py
```

#### 2. `add_sample_faqs()`
Populates the database with example questions.
```python
add_sample_faqs()  # Automatically called in app.py
```

#### 3. `search_faq(user_question)`
Searches the faq table for a matching question.
```python
answer = search_faq("What is this chatbot?")
# Returns: "This is a Smart FAQ Chatbot System..."
```

#### 4. `save_unknown_question(user_question)`
Saves unknown questions for admin review.
```python
save_unknown_question("Tell me a joke")
# Saved to unknown_questions table
```

#### 5. `save_chat_history(question, answer)`
Records every conversation automatically.
```python
save_chat_history("What is this chatbot?", "This is...")
# Saved to chat_history table
```

#### 6. `add_faq_answer(question, answer)`
Admin function to add new Q&A pairs.
```python
add_faq_answer("Tell me a joke", "Why did the chicken...")
# Added to faq table, removed from unknown_questions
```

#### 7. `get_unknown_questions()`
Gets list of questions without answers.
```python
questions = get_unknown_questions()
# Returns: list of unknown questions
```

#### 8. `get_faq_list()`
Gets all FAQ entries (for admin panel).
```python
faqs = get_faq_list()
# Returns: list of all Q&A pairs
```

---

## 🎯 How Search Works

The chatbot uses **exact matching** with case-insensitive search:

```python
# User asks: "what is this chatbot?"
# Stored in db: "What is this chatbot?"

# Search converts both to lowercase:
search_query = "what is this chatbot?"
db_question = "what is this chatbot?"

# They match → Answer returned!
```

---

## 🚀 Extending the Database

### Add a new table (example):
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER (1-5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
```

### Add a new column to existing table:
```python
cursor.execute('''
    ALTER TABLE faq ADD COLUMN category TEXT DEFAULT 'General'
''')
```

---

## 📈 Database Growth Expectations

After regular use:

| Table | Grows? | Example |
|-------|--------|---------|
| faq | Slowly (admin adds) | +5-10 per week |
| unknown_questions | Varies | Depends on user questions |
| chat_history | Fast | +100-1000 per day |

**To clean old chat history:**
```sql
DELETE FROM chat_history WHERE created_at < datetime('now', '-30 days');
```

---

## ✅ Database Integrity

### UNIQUE constraints prevent duplicates:
- **faq.question** - Same question can only exist once
- **unknown_questions.question** - Same unknown question saved only once

### AUTO-INCREMENT ensures unique IDs:
```python
# When inserting:
INSERT INTO faq (question, answer) VALUES (...)
# id field auto-increments: 1, 2, 3, 4, ...
```

---

## 🐛 Database Troubleshooting

### Check if database exists:
```powershell
# In project directory
dir  # Look for database.db
```

### Reset database (if corrupted):
1. Stop Flask app (Ctrl + C)
2. Delete `database.db`
3. Run app again → Database recreated
4. All sample FAQs re-loaded

### View database file size:
```powershell
(Get-Item database.db).Length  # Size in bytes
```

---

That's everything about the database! It's simple but powerful! 🚀
