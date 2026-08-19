console.log("Portfolio JavaScript loaded successfully!");


const skillProgressBars =
    document.querySelectorAll(".skill-progress");


const skillObserver =
    new IntersectionObserver(
        function (entries, observer) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    const bar = entry.target;

                    const proficiency =
                        bar.dataset.proficiency;

                    bar.style.width =
                        `${proficiency}%`;

                    observer.unobserve(bar);

                }

            });

        },
        {
            threshold: 0.4
        }
    );


skillProgressBars.forEach(function (bar) {

    skillObserver.observe(bar);

});

/* =========================
   AI ASSISTANT UI
   ========================= */

const aiToggle = document.getElementById("ai-toggle");
const aiChat = document.getElementById("ai-chat");
const aiClose = document.getElementById("ai-close");


if (aiToggle && aiChat && aiClose) {

    aiToggle.addEventListener("click", function () {

        aiChat.style.display = "flex";

        aiToggle.style.display = "none";

    });


    aiClose.addEventListener("click", function () {

        aiChat.style.display = "none";

        aiToggle.style.display = "block";

    });

}

/* =========================
   VOICE INPUT
   ========================= */

const voiceButton = document.getElementById("voice-button");
const aiInput = document.getElementById("ai-input");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (voiceButton && aiInput && SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;


    voiceButton.addEventListener("click", function () {

        recognition.start();

        voiceButton.textContent = "🔴";

    });


    recognition.addEventListener(
        "result",
        function (event) {

            const transcript =
                event.results[0][0].transcript;

            aiInput.value = transcript;

        }
    );


    recognition.addEventListener(
        "end",
        function () {

            voiceButton.textContent = "🎤";

        }
    );


    recognition.addEventListener(
        "error",
        function () {

            voiceButton.textContent = "🎤";

        }
    );

}

/* =========================
   TEXT TO SPEECH
   ========================= */

function speakText(text) {

    if (!("speechSynthesis" in window)) {

        console.log(
            "Text-to-speech is not supported."
        );

        return;
    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(text);


    speech.lang = "en-US";

    speech.rate = 1;

    speech.pitch = 1;


    window.speechSynthesis.speak(speech);

}


/* =========================
   AI CHAT
   ========================= */


const aiSend = document.getElementById("ai-send");
const aiMessages = document.getElementById("ai-messages");


function addMessage(message, type) {

    const messageDiv =
        document.createElement("div");

    messageDiv.classList.add(
        "ai-message",
        type === "user"
            ? "user-message"
            : "bot-message"
    );

    const paragraph =
        document.createElement("p");

    paragraph.textContent = message;

    messageDiv.appendChild(paragraph);

    aiMessages.appendChild(messageDiv);

    aiMessages.scrollTop =
        aiMessages.scrollHeight;
}


async function sendAIMessage() {

    const question =
        aiInput.value.trim();

    if (!question) {
        return;
    }


    addMessage(question, "user");

    aiInput.value = "";


    const typingMessage =
        document.createElement("div");

    typingMessage.classList.add(
        "ai-message",
        "bot-message"
    );

   typingMessage.innerHTML = `
    <p class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
    </p>
`;

    aiMessages.appendChild(typingMessage);


    try {

        const formData =
            new FormData();

        formData.append(
            "question",
            question
        );


        const response =
            await fetch("/ai/chat/", {

                method: "POST",

                body: formData,

                headers: {
                    "X-CSRFToken":
                        getCookie("csrftoken")
                }

            });


        const data =
            await response.json();


        typingMessage.remove();


        if (data.answer) {

            addMessage(
                data.answer,
                "bot"
            );

            speakText(
                data.answer
            );

        } else {

            addMessage(
                data.error ||
                "Sorry, something went wrong.",
                "bot"
            );

        }

    }

    catch (error) {

        typingMessage.remove();

        addMessage(
            "Sorry, I couldn't connect to the AI service.",
            "bot"
        );

        console.error(error);

    }

}


function getCookie(name) {

    let cookieValue = null;

    if (document.cookie &&
        document.cookie !== "") {

        const cookies =
            document.cookie.split(";");

        for (
            let i = 0;
            i < cookies.length;
            i++
        ) {

            const cookie =
                cookies[i].trim();


            if (
                cookie.substring(
                    0,
                    name.length + 1
                ) ===
                (name + "=")
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;
            }
        }
    }

    return cookieValue;
}


if (aiSend) {

    aiSend.addEventListener(
        "click",
        sendAIMessage
    );

}


if (aiInput) {

    aiInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                sendAIMessage();

            }

        }
    );

}


/* =========================
   AI QUICK QUESTIONS
   ========================= */

const quickQuestions =
    document.querySelectorAll(
        ".quick-question"
    );


quickQuestions.forEach(function (button) {

    button.addEventListener(
        "click",
        function () {

            const question =
                button.dataset.question;

            aiInput.value = question;

            sendAIMessage();

        }
    );

});


/* =========================
   DARK / LIGHT MODE
   ========================= */

const themeToggle =
    document.getElementById("theme-toggle");


function applyTheme(theme) {

    if (theme === "light") {

        document.body.classList.add(
            "light-theme"
        );

        if (themeToggle) {
            themeToggle.textContent = "☀️";
        }

    } else {

        document.body.classList.remove(
            "light-theme"
        );

        if (themeToggle) {
            themeToggle.textContent = "🌙";
        }

    }
}


const savedTheme =
    localStorage.getItem("portfolio-theme");


if (savedTheme) {

    applyTheme(savedTheme);

} else {

    applyTheme("dark");

}


if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        function () {

            const isLight =
                document.body.classList.contains(
                    "light-theme"
                );

            const newTheme =
                isLight ? "dark" : "light";

            applyTheme(newTheme);

            localStorage.setItem(
                "portfolio-theme",
                newTheme
            );

        }
    );

}
