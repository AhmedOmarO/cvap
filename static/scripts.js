/* filepath: /Users/ahmed.omar/Documents/Github/cvap/templates/scripts.js */
let stopTypingFlag = false;

// Load FAQs dynamically
async function loadFAQs() {
    let faqContainer = document.getElementById('faqContainer');
    faqContainer.innerHTML = ""; 

    try {
        let response = await fetch('/get_faqs');
        let data = await response.json();
        
        data.faqs.forEach((question) => {
            let button = document.createElement('button');
            button.classList.add("faq-button");
            button.textContent = question;
            button.onclick = () => sendMessage(question);
            faqContainer.appendChild(button);
        });
    } catch (error) {
        console.error("Error loading FAQs:", error);
        faqContainer.innerHTML = "Failed to load FAQs.";
    }
}

function clearChat() {
    let chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = '<p class="typing" id="typingEffect"> <b> Hello! How can I assist you? </b> </p> ';
}

function stopChat() {
    stopTypingFlag = true;
    console.log("Stop typing flag set to true");

}

// Send user message & get bot response
function sendMessage(message = null) {
    let userInput = document.getElementById('userInput');
    let messageText = message ? message : userInput.value.trim();
    if (messageText === "") return;

    appendMessage(messageText, "user-message");

    fetch('/get_response', {
        method: 'POST',
        body: JSON.stringify({ message: messageText }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        typeMessage(data.response, "bot-message");
    });

    if (!message) {
        userInput.value = "";
    }
}


// Type message with HTML support
function typeMessage(text, className) {
    let chatContainer = document.getElementById('chatContainer');
    let messageDiv = document.createElement('div');
    messageDiv.classList.add("message", className);
    // messageDiv.classList.add("typing", className);
    // stopTypingFlag = false; // Reset the stop flag

    chatContainer.appendChild(messageDiv);

    // Split text into sentences
    let sentences = text.split(/(?<=[.!?])|<\/div>/).filter(Boolean);

    
    // log the sentences
    sentences = sentences.filter(s => s.trim()); // Remove empty strings


    // loop through the sentences and type them sequentially


     function typeSentence() {
        

        
                
        for (let i = 0; i < sentences.length; i++) {
            

            // create a new p element for each sentence
            const sentenceElement = document.createElement("p"); // Each sentence in a new line
            sentenceElement.style.margin = "0"; // Remove default margin
            sentenceElement.style.padding = "0"; // Remove default padding
            sentenceElement.innerHTML = sentences[i]; // Set the sentence text
            sentenceElement.classList.add("typing"); // Add typing animation
            // append the sentence to the chat container after a delay
            setTimeout(() => {
                chatContainer.appendChild(sentenceElement);
                        }, 2000 * i );
            console.log(stopTypingFlag)
            // chatContainer.appendChild(sentenceElement);
            chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll

            // remove the typing animation after the sentence is typed
            setTimeout(() => {
                sentenceElement.classList.remove("typing");
            }, 2000 * i + 2000);

        }

        
    }

    typeSentence();
}

// append message without delay 
function appendMessage(text, className) {
    let chatContainer = document.getElementById('chatContainer');

    let messageDiv = document.createElement('div');
    messageDiv.classList.add("message", className);
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll
}

// Handle "Enter" key press to send message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

// Load FAQs on page load
loadFAQs();



// function typeMessage(text, className) {
//     let chatContainer = document.getElementById('chatContainer');
//     let messageDiv = document.createElement('div');
//     messageDiv.classList.add("message", className);
//     chatContainer.appendChild(messageDiv);

//     // Split text into sentences while keeping HTML intact
//     let sentences = text.match(/([^.!?]+[.!?]*|<[^>]+>)/g); // Keep punctuation and HTML tags together
//     sentences = sentences ? sentences.filter(s => s.trim()) : [];

//     let currentIndex = 0;

//     function typeSentence(sentence, index) {
//         let tempDiv = document.createElement("div");
//         tempDiv.innerHTML = sentence;
//         let sentenceText = tempDiv.innerText; // Extract plain text without breaking HTML
//         let htmlParts = sentence.split(/(<[^>]+>)/g).filter(part => part.trim() !== "");

//         let i = 0;
//         function typeCharacter() {
//             if (i < htmlParts.length) {
//                 if (htmlParts[i].startsWith("<")) {
//                     messageDiv.innerHTML += htmlParts[i]; // Instantly insert HTML tag
//                 } else {
//                     let charArray = htmlParts[i].split("");
//                     let j = 0;
//                     let charInterval = setInterval(() => {
//                         if (j < charArray.length) {
//                             messageDiv.innerHTML += charArray[j];
//                             j++;
//                             chatContainer.scrollTop = chatContainer.scrollHeight;
//                         } else {
//                             clearInterval(charInterval);
//                             i++;
//                             typeCharacter(); // Move to next part
//                         }
//                     }, 10); // Adjust speed
//                     return;
//                 }
//                 i++;
//                 typeCharacter();
//             } else {
//                 if (index < sentences.length - 1) {
//                     setTimeout(() => typeSentence(sentences[index + 1], index + 1), 500);
//                 }
//             }
//         }

//         typeCharacter();
//     }

//     if (sentences.length > 0) {
//         typeSentence(sentences[0], 0);
//     }
// }
