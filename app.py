"""
Smart FAQ Chatbot System - Flask Application
Main application file that runs the chatbot server
"""

from flask import Flask, render_template, request, jsonify
from database import (
    init_database,
    add_sample_faqs,
    search_faq,
    save_unknown_question,
    save_chat_history,
    add_faq_answer,
    get_unknown_questions,
    get_faq_list
)

# Create Flask application instance
app = Flask(__name__)

# Initialize database when app starts
init_database()
add_sample_faqs()


@app.route('/')
def index():
    """
    Home route - displays the chatbot interface
    Returns the main HTML page
    """
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat API endpoint - processes user messages
    This is where the magic happens!
    
    Expected JSON input:
        {
            "message": "user's question here"
        }
    
    Returns JSON with bot response
    """
    
    # Get the user's message from the request
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    # Check if message is empty
    if not user_message:
        return jsonify({
            'success': False,
            'error': 'Please enter a message'
        })
    
    # Search for answer in FAQ database
    answer = search_faq(user_message)
    
    # If answer found, use it
    if answer:
        bot_response = answer
        is_known = True
    else:
        # If no answer found, save question and send default message
        save_unknown_question(user_message)
        bot_response = "🤔 I don't know the answer to this yet. Your question has been saved and an admin will add an answer soon!"
        is_known = False
    
    # Save conversation to chat history
    save_chat_history(user_message, bot_response)
    
    # Return response to frontend in JSON format
    return jsonify({
        'success': True,
        'message': bot_response,
        'is_known': is_known
    })


@app.route('/api/admin/unknown-questions', methods=['GET'])
def get_unknown():
    """
    Admin API - Get all unknown questions
    Returns list of questions the chatbot couldn't answer
    """
    questions = get_unknown_questions()
    return jsonify({
        'success': True,
        'questions': questions
    })


@app.route('/api/admin/faq-list', methods=['GET'])
def get_faqs():
    """
    Admin API - Get all FAQ entries
    Returns the complete FAQ database
    """
    faqs = get_faq_list()
    return jsonify({
        'success': True,
        'faqs': faqs
    })


@app.route('/api/admin/add-answer', methods=['POST'])
def add_answer():
    """
    Admin API - Add new Q&A pair to database
    This allows admin to teach the chatbot new answers
    
    Expected JSON input:
        {
            "question": "question here",
            "answer": "answer here"
        }
    """
    
    data = request.get_json()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    
    # Validate input
    if not question or not answer:
        return jsonify({
            'success': False,
            'error': 'Question and answer cannot be empty'
        })
    
    # Add to FAQ database
    result = add_faq_answer(question, answer)
    
    return jsonify({
        'success': True,
        'message': result
    })


# Error handler for 404 (page not found)
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404


# Error handler for 500 (server error)
@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


# Main entry point
if __name__ == '__main__':
    """
    Run the Flask application
    Set debug=True for development (auto-reload on code changes)
    Running on 127.0.0.1:5000 (localhost:5000)
    """
    print("\n" + "="*60)
    print("🤖 Smart FAQ Chatbot System Starting...")
    print("="*60)
    print("📍 Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    # Start the Flask server
    app.run(debug=True, host='127.0.0.1', port=5000)
