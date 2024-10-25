const micButton = document.getElementById('micButton');
const outputText = document.getElementById('outputText');
let isRecording = false;
let recognition;

// Check if the browser supports SpeechRecognition
if ('webkitSpeechRecognition' in window) {
    // Initialize speech recognition
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'fa-FA';  // Persian language

    // Handle speech recognition results
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        outputText.value = transcript;  // Populate the textarea with the result
    };

    // Handle errors during recognition
    recognition.onerror = function (event) {
        console.error("Error occurred in recognition: " + event.error);
    };

    // Stop recognition when it ends
    recognition.onend = function () {
        if (isRecording) {
            micButton.style.backgroundColor = 'transparent';  
            isRecording = false;
        }
    };

    // Handle button click to start/stop recognition
    micButton.addEventListener('click', () => {
        if (!isRecording) {
            recognition.start();  // Start speech recognition
            micButton.style.backgroundColor = '#63e6bf9a'; 
            isRecording = true;
        } else {
            recognition.stop();  // Stop speech recognition
        }
    });
} else {
    // If browser does not support speech recognition
    alert("Your browser doesn't support speech recognition.");
}
