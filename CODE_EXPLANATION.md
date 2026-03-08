# 📖 Code Explanation for Beginners

This guide explains the key code sections in simple terms.

---

## 🎯 How the Chatbot Works - Step by Step

```
┌─────────────────────────────────────────────────────────────┐
│ USER TYPES QUESTION IN BROWSER                              │
│ "What is this chatbot?"                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ JavaScript (script.js) CATCHES THE TEXT                      │
│ - Gets text from input field                                │
│ - Calls sendMessage() function                              │
│ - Displays message as blue chat bubble                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ fetch() SENDS REQUEST TO FLASK SERVER                        │
│ POST /api/chat                                              │
│ Message: "What is this chatbot?"                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ FLASK (app.py) RECEIVES REQUEST                              │
│ - @app.route('/api/chat') function triggered                │
│ - Gets user message: "What is this chatbot?"                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ DATABASE (database.py) SEARCHES FAQ                          │
│ search_faq("What is this chatbot?")                         │
│ - Converts to lowercase                                     │
│ - Looks in faq table                                        │
│ - FOUND! Returns answer                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ FLASK SAVES CONVERSATION                                    │
│ save_chat_history(question, answer)                         │
│ - Saves to chat_history table                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ FLASK RETURNS RESPONSE AS JSON                               │
│ {                                                           │
│   "success": true,                                          │
│   "message": "This is a Smart FAQ Chatbot..."               │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ JavaScript RECEIVES RESPONSE                                │
│ - Parses JSON data                                          │
│ - Displays message as gray chat bubble                      │
│ - Auto-scrolls to bottom                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ USER SEES RESPONSE IN CHAT                                   │
│ "This is a Smart FAQ Chatbot System..."                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 app.py (Flask Application)

### Key Function: `@app.route('/api/chat', methods=['POST'])`

This is the **main chatbot logic**:

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    # 1. Get the user's message from the request
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    # 2. Check if message is empty
    if not user_message:
        return jsonify({'success': False, 'error': 'Please enter a message'})
    
    # 3. Search FAQ database
    answer = search_faq(user_message)
    
    # 4. If found, use it; if not, create default message
    if answer:
        bot_response = answer
        is_known = True
    else:
        save_unknown_question(user_message)
        bot_response = "I don't know this yet..."
        is_known = False
    
    # 5. Save conversation
    save_chat_history(user_message, bot_response)
    
    # 6. Send response back
    return jsonify({'success': True, 'message': bot_response, 'is_known': is_known})
```

**Translation:** 
1. Get message from user
2. Check if empty
3. Search database for answer
4. **If answer exists → use it, else → mark as unknown**
5. Save conversation
6. Send response back to frontend

---

## 💾 database.py (Database Logic)

### Key Function: `search_faq(user_question)`

This **searches** the FAQ database:

```python
def search_faq(user_question):
    # 1. Open database connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 2. Convert to lowercase (ignore case differences)
    search_query = user_question.lower().strip()
    
    # 3. Execute SQL query
    cursor.execute(
        'SELECT answer FROM faq WHERE LOWER(question) = ?',
        (search_query,)
    )
    
    # 4. Get result
    result = cursor.fetchone()
    conn.close()
    
    # 5. Return answer if found, None if not
    return result[0] if result else None
```

**Translation:**
1. Connect to database
2. Make question lowercase
3. **Search for exact match in faq table**
4. Get the answer
5. Return answer or None

---

### Key Function: `save_unknown_question(user_question)`

This **saves questions the chatbot doesn't know**:

```python
def save_unknown_question(user_question):
    # 1. Open database connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 2. Insert question into unknown_questions table
    try:
        cursor.execute(
            'INSERT INTO unknown_questions (question) VALUES (?)',
            (user_question,)
        )
        conn.commit()  # Save to database
    except sqlite3.IntegrityError:
        # If question already exists, skip it
        pass
    finally:
        conn.close()
```

**Translation:**
1. Connect to database
2. **Insert question into unknown_questions table**
3. Save changes
4. If it already exists, ignore it
5. Close connection

---

### Key Function: `add_faq_answer(question, answer)`

This is **admin function to teach the chatbot**:

```python
def add_faq_answer(question, answer):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 1. Insert new Q&A pair
        cursor.execute(
            'INSERT INTO faq (question, answer) VALUES (?, ?)',
            (question, answer)
        )
        conn.commit()
        
        # 2. Remove from unknown_questions (if it's there)
        cursor.execute(
            'DELETE FROM unknown_questions WHERE question = ?',
            (question,)
        )
        conn.commit()
        
        conn.close()
        return "✓ Answer added successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return "✗ This question already exists"
```

**Translation:**
1. Connect to database
2. **Add new Q&A pair to faq table**
3. Remove from unknown_questions
4. Return success message

---

## 🎨 script.js (Frontend Logic)

### Key Function: `sendMessage()`

This **handles when user clicks Send**:

```javascript
function sendMessage() {
    // 1. Get text from input field
    const message = messageInput.value.trim();
    
    // 2. Check if empty
    if (!message) {
        showStatus('Please type a question first!', 'error');
        return;
    }
    
    // 3. Add user message as blue bubble
    addMessageToChat(message, 'user');
    
    // 4. Clear input field
    messageInput.value = '';
    
    // 5. Show "Thinking..." status
    showStatus('Thinking...', 'info');
    
    // 6. Send to server
    sendToServer(message);
}
```

**Translation:**
1. Get message from input
2. Check if empty
3. **Show message as blue bubble**
4. Clear input field
5. Show "Thinking..." message
6. Send to Flask server

---

### Key Function: `sendToServer(message)`

This **communicates with Flask**:

```javascript
function sendToServer(message) {
    // 1. Create data object
    const data = { message: message };
    
    // 2. Send POST request to Flask
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())  // Convert to JSON
    .then(data => {
        // 3. If successful, show bot response
        if (data.success) {
            addMessageToChat(data.message, 'bot');
            showStatus('', '');
        } else {
            showStatus('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showStatus('Failed to connect!', 'error');
    })
    .finally(() => {
        // 4. Re-enable send button
        sendBtn.disabled = false;
        messageInput.focus();
    });
}
```

**Translation:**
1. Create data object
2. **Send POST request to `/api/chat`**
3. Wait for response
4. Show bot response as gray bubble
5. If error, show error message
6. Re-enable send button

---

### Key Function: `addMessageToChat(message, sender)`

This **creates chat bubbles**:

```javascript
function addMessageToChat(message, sender) {
    // 1. Create message container
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // 2. Create message text
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = message;
    
    // 3. Create timestamp
    const timeDiv = document.createElement('div');
    timeDiv.classList.add('message-time');
    timeDiv.textContent = 'Just now';
    
    // 4. Add content and time to message
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    // 5. Add message to chat box
    chatBox.appendChild(messageDiv);
    
    // 6. Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
```

**Translation:**
1. Create a new `<div>` for message
2. **Add appropriate CSS class** (blue for user, gray for bot)
3. Add message text
4. Add timestamp
5. Add to chat box
6. Scroll to bottom

---

## 📋 index.html (Structure)

The HTML is simple:

```html
<!-- Chat box where messages appear -->
<div class="chat-box" id="chatBox">
    <!-- Messages added here by JavaScript -->
</div>

<!-- Input section -->
<input id="messageInput" placeholder="Type your question...">
<button id="sendBtn">Send</button>

<!-- Admin panel -->
<input id="adminQuestion" placeholder="Enter question">
<textarea id="adminAnswer" placeholder="Enter answer"></textarea>
<button id="addAnswerBtn">Add to FAQ</button>
```

**Translation:**
- **Chat box** = Place where messages appear
- **Input + Button** = Where user types questions
- **Admin section** = Where admin adds Q&A pairs

---

## 🎨 style.css (Styling)

Key CSS classes:

```css
/* User messages (right side, blue) */
.user-message .message-content {
    background: #667eea;
    color: white;
    border-radius: 15px 15px 0px 15px;
}

/* Bot messages (left side, gray) */
.bot-message .message-content {
    background: #e9ecef;
    color: #333;
    border-radius: 15px 15px 15px 0px;
}

/* Send button styling */
.send-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 25px;
    cursor: pointer;
}

/* Chat box scrollbar */
.chat-box::-webkit-scrollbar {
    width: 8px;
}
```

**Translation:**
- User messages → **Blue, right-aligned**
- Bot messages → **Gray, left-aligned**
- Button → **Purple gradient**
- Scrollbar → **Thin, styled**

---

## 🔄 Complete Flow Example

### User asks: "What is this chatbot?"

**Step 1 - Frontend (JavaScript)**
```javascript
// User clicks Send button
sendMessage()
// Gets: "What is this chatbot?"
addMessageToChat("What is this chatbot?", 'user')
// Shows as blue bubble on right
sendToServer("What is this chatbot?")
// Sends to Flask
```

**Step 2 - Backend (Flask)**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = "What is this chatbot?"
    answer = search_faq(user_message)  # Search database
    # Found answer!
    save_chat_history(user_message, answer)
    return jsonify({'success': True, 'message': answer})
```

**Step 3 - Database (SQLite)**
```sql
-- search_faq() executes:
SELECT answer FROM faq 
WHERE LOWER(question) = 'what is this chatbot?'
-- Returns: "This is a Smart FAQ Chatbot System..."

-- save_chat_history() executes:
INSERT INTO chat_history (user_question, bot_answer, created_at)
VALUES ('What is this chatbot?', 'This is...', CURRENT_TIMESTAMP)
-- Saved!
```

**Step 4 - Frontend (JavaScript receives)**
```javascript
// Response arrives
data.message = "This is a Smart FAQ Chatbot System..."

// Show as bot message
addMessageToChat("This is a Smart FAQ Chatbot System...", 'bot')
// Shows as gray bubble on left
```

---

## 🎯 Important Concepts

### 1. **Async/Await (fetch)**
```javascript
fetch('/api/chat', {...})
.then(response => response.json())
.then(data => {
    // Handle response
})
```
Translation: Send request, wait for response, then handle it.

### 2. **JSON (Communication Format)**
```javascript
// JavaScript sends:
{ "message": "What is this chatbot?" }

// Flask receives and sends back:
{ "success": true, "message": "This is a Smart FAQ..." }
```
Translation: Data format that both frontend and backend understand.

### 3. **Database Query**
```python
cursor.execute(
    'SELECT answer FROM faq WHERE LOWER(question) = ?',
    (search_query,)
)
```
Translation: Find answer where question matches (case-insensitive).

### 4. **REST API Endpoint**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
```
Translation: Flask listens for POST requests at `/api/chat` and runs this function.

---

## ✅ Summary

1. **User types question** → JavaScript catches it
2. **JavaScript sends to Flask** → Via fetch() API
3. **Flask searches database** → Using search_faq()
4. **Flask saves conversation** → Using save_chat_history()
5. **Flask returns response** → As JSON
6. **JavaScript displays response** → As chat bubble
7. **All saved to database** → For history and learning

**Simple, Beginner-Friendly, No AI/ML!** 🎉

---

## 💡 Try This Exercise

**Modify the bot response message:**

1. Find this line in `app.py`:
```python
bot_response = "🤔 I don't know the answer to this yet..."
```

2. Change it to:
```python
bot_response = "❌ Sorry, I don't have an answer for that. Check the admin panel!"
```

3. Save the file
4. Restart Flask (Ctrl + C, then `python app.py`)
5. Ask an unknown question → See new message!

This shows how easy it is to modify the chatbot! 🚀

