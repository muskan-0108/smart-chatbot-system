/*
   Smart FAQ Chatbot - JavaScript Frontend
   This file handles all the interactive features of the chatbot
*/

// Get DOM elements (these are the HTML elements we'll interact with)
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const chatBox = document.getElementById('chatBox');
const statusMessage = document.getElementById('statusMessage');

// Admin panel elements
const adminQuestion = document.getElementById('adminQuestion');
const adminAnswer = document.getElementById('adminAnswer');
const addAnswerBtn = document.getElementById('addAnswerBtn');
const unknownList = document.getElementById('unknownList');

// Debug: Check if elements are found
console.log("🔍 DOM Elements loaded:");
console.log("  messageInput:", messageInput ? "✅ Found" : "❌ NOT FOUND");
console.log("  sendBtn:", sendBtn ? "✅ Found" : "❌ NOT FOUND");
console.log("  chatBox:", chatBox ? "✅ Found" : "❌ NOT FOUND");
console.log("  statusMessage:", statusMessage ? "✅ Found" : "❌ NOT FOUND");


/* ===== CHAT FUNCTIONALITY ===== */

/**
 * Send a message to the chatbot
 * This function is called when user clicks Send button or presses Enter
 */
function sendMessage() {
    const message = messageInput.value.trim();
    
    console.log("🔵 sendMessage() called, message:", message);
    
    // Check if message is empty
    if (!message) {
        console.log("⚠️ Message is empty");
        showStatus('Please type a question first!', 'error');
        return;
    }
    
    console.log("📝 Adding user message to chat");
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input field
    messageInput.value = '';
    
    // Disable send button while processing
    sendBtn.disabled = true;
    showStatus('Thinking...', 'info');
    
    // Send message to server
    sendToServer(message);
}

/**
 * Send message to Flask backend
 * Makes a request to /api/chat endpoint
 */
function sendToServer(message) {
    // Create data to send
    const data = {
        message: message
    };
    
    console.log("📤 Sending message to server:", message);
    
    // Send POST request to Flask server
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log("📥 Response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("💬 Bot response received:", data);
        // Handle successful response
        if (data.success) {
            // Add bot response to chat
            console.log("✅ Adding bot message to chat:", data.message);
            addMessageToChat(data.message, 'bot');
            showStatus('', '');  // Clear status
        } else {
            // Show error if request failed
            console.log("❌ Error from server:", data.error);
            showStatus('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        // Handle network error
        console.error('❌ Network error:', error);
        showStatus('Failed to connect to server!', 'error');
    })
    .finally(() => {
        // Always re-enable send button
        sendBtn.disabled = false;
        messageInput.focus();  // Focus back on input
    });
}

/**
 * Add a message to the chat display
 * Creates a chat bubble and adds it to the chat box
 */
function addMessageToChat(message, sender) {
    console.log(`➕ Adding ${sender} message:`, message);
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = message;
    
    // Create timestamp
    const timeDiv = document.createElement('div');
    timeDiv.classList.add('message-time');
    timeDiv.textContent = 'Just now';
    
    // Add content and time to message
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    // Add message to chat box
    chatBox.appendChild(messageDiv);
    
    console.log("✨ Message added from", sender, "- Total messages now:", chatBox.children.length);
    
    // Force scroll to bottom immediately
    setTimeout(() => {
        // Scroll to the absolute bottom
        chatBox.scrollTop = chatBox.scrollHeight + 1000;
        console.log("📌 ChatBox scrollHeight:", chatBox.scrollHeight, "| Scrolled to:", chatBox.scrollTop);
    }, 50);
}

/**
 * Show status message below input
 * Used for showing errors, loading states, or success messages
 */
function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = 'status-message';
    if (type) {
        statusMessage.classList.add(type);
    }
}


/* ===== ADMIN PANEL FUNCTIONALITY ===== */

/**
 * Add a new Q&A pair to the FAQ database
 * Called when admin clicks "Add to FAQ" button
 */
function addNewAnswer() {
    const question = adminQuestion.value.trim();
    const answer = adminAnswer.value.trim();
    
    // Validate inputs
    if (!question || !answer) {
        alert('Please fill in both question and answer fields!');
        return;
    }
    
    // Create data to send
    const data = {
        question: question,
        answer: answer
    };
    
    // Send POST request to admin API
    fetch('/api/admin/add-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Clear form on success
            adminQuestion.value = '';
            adminAnswer.value = '';
            alert(data.message);
            
            // Refresh unknown questions list
            loadUnknownQuestions();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add answer!');
    });
}

/**
 * Load and display unknown questions from the database
 * Shows questions that the chatbot couldn't answer
 */
function loadUnknownQuestions() {
    // Send GET request to get unknown questions
    fetch('/api/admin/unknown-questions')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const questions = data.questions;
            
            // Clear the list
            unknownList.innerHTML = '';
            
            // Check if there are any unknown questions
            if (questions.length === 0) {
                unknownList.innerHTML = '<p>✓ No unknown questions! All questions have answers.</p>';
            } else {
                // Add each question to the list
                questions.forEach(item => {
                    const questionDiv = document.createElement('div');
                    questionDiv.classList.add('admin-list-item');
                    
                    // Format the question with id and date
                    const questionText = item[1];  // item[1] is the question
                    const dateText = new Date(item[2]).toLocaleString();  // item[2] is created_at
                    
                    questionDiv.innerHTML = `
                        <strong>Q:</strong> ${questionText}<br>
                        <small style="color: #999;">Asked: ${dateText}</small>
                    `;
                    
                    unknownList.appendChild(questionDiv);
                });
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        unknownList.innerHTML = '<p>Error loading unknown questions</p>';
    });
}


/* ===== EVENT LISTENERS ===== */

// Send message when clicking Send button
sendBtn.addEventListener('click', sendMessage);

// Send message when pressing Enter key
messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Add answer when clicking admin button
addAnswerBtn.addEventListener('click', addNewAnswer);

// Load unknown questions when page loads
window.addEventListener('load', function() {
    loadUnknownQuestions();
    
    // Refresh unknown questions every 5 seconds
    setInterval(loadUnknownQuestions, 5000);
});

// Focus on input when page loads
window.addEventListener('load', function() {
    messageInput.focus();
});
