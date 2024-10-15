
// Toggle mobile dropdown visibility
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const mobileDropdown = document.getElementById('mobileDropdown');
const mobileDropdownBtn = document.querySelector('.mobile-dropdown-btn');
const mobileDropdownContent = document.querySelector('.mobile-dropdown-content');

mobileMenuBtn.addEventListener('click', function() {
    mobileDropdown.classList.toggle('show');
});

// Toggle service dropdown on mobile
mobileDropdownBtn.addEventListener('click', function() {
    mobileDropdownContent.classList.toggle('show');
});

// This will update the year dynamically
const yearSpan = document.getElementById("year");
const currentYear = new Date().getFullYear();
yearSpan.textContent = currentYear;
    

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

function formatMessage(message) {
    // Format bold and italic text using asterisks
    message = message.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>'); // Bold Italics
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold
    message = message.replace(/\*(.*?)\*/g, '$1'); // Italics
    
    // Replace new lines (\n) with <br> for proper line breaks
    message = message.replace(/\n/g, '<br>');

    // Replace bullet points (- or *) with list items (<li> tags)
    message = message.replace(/^[-*] (.*?)(\n|$)/gm, '<li>$1</li>');

    // Wrap the list items in <ul> tags to create a proper list
    message = message.replace(/(<li>.*?<\/li>)/g, '<ul>$1</ul>');

    //message = message.replace(/\*/g, '');

    return message;
}
        

let isUserAtBottom = true; // Tracks whether the user is at the bottom of the chat

// Check if the user is at the bottom of the chat box
function checkScrollPosition() {
    const chatHeight = chatBox.scrollHeight;
    const visibleHeight = chatBox.clientHeight;
    const scrollPosition = chatBox.scrollTop;

    // If the user is within 20px from the bottom, consider them at the bottom
    isUserAtBottom = chatHeight - (visibleHeight + scrollPosition) < 20;
}

// Auto-scroll only if the user is at the bottom
function autoScroll() {
    if (isUserAtBottom) {
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }
}

// Listen for scroll events to detect when the user scrolls up or down
chatBox.addEventListener('scroll', checkScrollPosition);

// Modified typeMessage function to respect user's scroll
function typeMessage(messageDiv, message) {
    const formattedMessage = formatMessage(message); // Format the message
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = formattedMessage;

    const elements = Array.from(tempDiv.childNodes); // Get all child nodes (text and elements)

    let currentElementIndex = 0;
    let typingIndex = 0;

    const typingSpeed = 10; // Typing speed

    function typeCharacter() {
        if (currentElementIndex < elements.length) {
            const currentNode = elements[currentElementIndex];

            if (currentNode.nodeType === Node.TEXT_NODE) {
                // If it's a text node, type character by character
                if (typingIndex < currentNode.textContent.length) {
                    messageDiv.innerHTML += currentNode.textContent.charAt(typingIndex);
                    typingIndex++;
                    setTimeout(typeCharacter, typingSpeed);
                    autoScroll(); // Only auto-scroll if the user is at the bottom
                } else {
                    // Move to the next node when done with this one
                    currentElementIndex++;
                    typingIndex = 0;
                    typeCharacter(); // Continue typing the next node
                }
            } else if (currentNode.nodeType === Node.ELEMENT_NODE) {
                // If it's an HTML element, add it directly and move on
                messageDiv.appendChild(currentNode.cloneNode(true)); // Append the HTML element
                currentElementIndex++;
                typeCharacter(); // Continue typing the next node
                autoScroll(); // Only auto-scroll if the user is at the bottom
            }
        }
    }

    typeCharacter(); // Start typing
}

function appendMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom

    if (sender === 'bot') {
        const cleanedMessage = message.trim();
        typeMessage(messageDiv, formatMessage(cleanedMessage)); // Use typing effect for bot
    } else {
        messageDiv.innerHTML = formatMessage(message); // Display user message directly
    }
}

async function sendMessage() {
    const message = userInput.value.trim(); // Trim whitespace from input
    if (!message) return; // Ignore empty messages

    appendMessage("user", message); // Append user message to chat
    userInput.value = ""; // Clear input box immediately
    resetTextareaHeight(); // Reset the height of textarea

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
    });

    const data = await response.json();
    appendMessage("bot", data.response); // Append bot message with typing effect
}


// Attach event listeners
sendButton.addEventListener("click", sendMessage);

// Adjust height on input (remove resizing on normal typing)
userInput.addEventListener("input", (event) => {
    // Do nothing on normal typing
});

// Handle Shift + Enter and regular Enter behavior
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault(); // Prevent default behavior of adding a newline
        addNewLine(); // Add a new line and expand the textarea
    } else if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Prevent default behavior of adding a newline
        sendMessage(); // Send the message when Enter is pressed without Shift
        resetTextareaHeight(); // Reset textarea height after sending a message
    }
});

// Function to add a new line and expand the textarea when Shift + Enter is pressed
function addNewLine() {
    const currentValue = userInput.value;
    const cursorPos = userInput.selectionStart; // Get the current cursor position

    // Insert a new line at the current cursor position
    userInput.value = currentValue.slice(0, cursorPos) + "\n" + currentValue.slice(cursorPos);
    userInput.selectionStart = userInput.selectionEnd = cursorPos + 1; // Move the cursor to the new line

    // Adjust the textarea height manually after inserting the new line
    autoResizeTextarea(); // Now we handle the auto-resizing only after Shift + Enter
}

// Function to manually resize the textarea based on its scrollHeight
function autoResizeTextarea() {
    userInput.style.height = 'auto'; // Reset height before recalculating
    userInput.style.height = `${Math.min(userInput.scrollHeight, 120)}px`; // Max height limit (120px or whatever you want)
}

// Reset textarea height to initial height (1 row) after sending a message
function resetTextareaHeight() {
    userInput.style.height = 'auto'; // Reset to auto before calculating
    userInput.style.height = '28px'; // Reset to initial height (adjust this as needed)
}
