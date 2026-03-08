"""
Database module for Smart FAQ Chatbot System
This file handles all database operations using SQLite
"""

import sqlite3
from datetime import datetime

# Database file name
DATABASE = 'database.db'

def init_database():
    """
    Initialize the database with required tables
    This function creates the database structure if it doesn't exist
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create FAQ table (contains question-answer pairs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create unknown_questions table (questions chatbot doesn't know)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unknown_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_history table (all conversations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT NOT NULL,
            bot_answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")


def add_sample_faqs():
    """
    Add example FAQ entries to the database
    This helps demonstrate how the chatbot works
    """
    sample_faqs = [
        ("What is this chatbot?", "This is a Smart FAQ Chatbot System. I can answer frequently asked questions using simple rule-based logic."),
        ("How does this chatbot work?", "I search my FAQ database for matching questions. If found, I return the stored answer. If not found, I save your question for future learning."),
        ("Can I teach you new questions?", "Yes! An admin can add new Q&A pairs to my database through the admin feature, and I will learn them automatically."),
        ("What is your name?", "I am the Smart FAQ Chatbot! I'm here to help you find answers quickly."),
        ("How are you?", "I'm working perfectly! Thanks for asking. How can I help you today?"),
        ("What technologies do you use?", "I'm built with Python Flask (backend), SQLite (database), and HTML/CSS/JavaScript (frontend)."),
        ("Is this website secure?", "This is a demo chatbot for learning purposes. For production use, additional security measures should be implemented."),
        ("Can you do calculations?", "I can respond to predefined questions in my database, but I don't perform calculations. I use simple rule-based logic."),
    ]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Add each FAQ, skip if it already exists
    for question, answer in sample_faqs:
        try:
            cursor.execute(
                'INSERT INTO faq (question, answer) VALUES (?, ?)',
                (question, answer)
            )
        except sqlite3.IntegrityError:
            # Question already exists, skip it
            pass
    
    conn.commit()
    conn.close()
    print("✓ Sample FAQs added successfully!")


def search_faq(user_question):
    """
    Search for a matching question in the FAQ database
    Returns the answer if found, None if not found
    
    Now uses LIKE matching for more flexible search (partial matches work)
    
    Args:
        user_question (str): The question asked by the user
    
    Returns:
        str: The answer if found, None otherwise
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Convert user question to lowercase for case-insensitive search
    search_query = user_question.lower().strip()
    
    # First try: Exact match
    cursor.execute(
        'SELECT answer FROM faq WHERE LOWER(question) = ?',
        (search_query,)
    )
    
    result = cursor.fetchone()
    
    # If no exact match, try partial match (LIKE)
    if not result:
        # Search where the user question contains key words from FAQ
        cursor.execute(
            'SELECT answer FROM faq WHERE LOWER(question) LIKE ?',
            ('%' + search_query + '%',)
        )
        result = cursor.fetchone()
    
    # If still no match, try searching if FAQ contains words from user question
    if not result:
        cursor.execute(
            'SELECT answer FROM faq WHERE LOWER(?) LIKE \'%\' || LOWER(question) || \'%\'',
            (search_query,)
        )
        result = cursor.fetchone()
    
    conn.close()
    
    # Return answer if found, None otherwise
    return result[0] if result else None


def save_unknown_question(user_question):
    """
    Save a question that the chatbot doesn't know the answer to
    This helps identify gaps in the FAQ database
    
    Args:
        user_question (str): The question the user asked
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO unknown_questions (question) VALUES (?)',
            (user_question,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Question already exists in unknown_questions, no need to add again
        pass
    finally:
        conn.close()


def save_chat_history(question, answer):
    """
    Save the conversation to chat history
    Helps track all interactions with the chatbot
    
    Args:
        question (str): The user's question
        answer (str): The chatbot's response
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO chat_history (user_question, bot_answer) VALUES (?, ?)',
        (question, answer)
    )
    
    conn.commit()
    conn.close()


def add_faq_answer(question, answer):
    """
    Admin function: Add a new Q&A pair to the FAQ database
    This allows the chatbot to learn new answers over time
    
    Args:
        question (str): The question to add
        answer (str): The answer to add
    
    Returns:
        str: Success or error message
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO faq (question, answer) VALUES (?, ?)',
            (question, answer)
        )
        conn.commit()
        
        # Remove from unknown_questions if it exists there
        cursor.execute('DELETE FROM unknown_questions WHERE question = ?', (question,))
        conn.commit()
        
        conn.close()
        return "✓ Answer added successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return "✗ This question already exists in the FAQ database."


def get_unknown_questions():
    """
    Get all unknown questions that the chatbot couldn't answer
    Useful for admin to know what needs to be learned
    
    Returns:
        list: List of tuples (id, question, created_at)
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, question, created_at FROM unknown_questions ORDER BY created_at DESC')
    questions = cursor.fetchall()
    
    conn.close()
    return questions


def get_faq_list():
    """
    Get all FAQ entries from the database
    Useful for admin panel
    
    Returns:
        list: List of tuples (id, question, answer, created_at)
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, question, answer, created_at FROM faq ORDER BY created_at DESC')
    faqs = cursor.fetchall()
    
    conn.close()
    return faqs
