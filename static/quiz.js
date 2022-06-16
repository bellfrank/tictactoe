// QUIZ QUESTIONS
const questions = [
    {
        question: "How many times does the average person laugh in a day?",
        options: ["0", "13", "20", "-5"],
        answer: "13"
    },
    {
        question: "What is 10 + 10?",
        options: ["8", "20", "28", "30"],
        answer: "20"
    },
    {
        question: "What is 11 + 11?",
        options: ["8", "22", "28", "30"],
        answer: "22"
    },
    {
        question: "What is Francisco's favorite animal?",
        options: ["otters", "penguins", "jellyfish"],
        answer: "otters"
    },
    {
        question: "What is 5 + 5?",
        options: ["1", "20", "10"],
        answer: "10"
    }
];

// Variables
let correct = 0;
let question_number = 0;
const total_questions = 4;
let interval = 0
timer_reset = false;


// Setting starting value of counter to 0, this will persist even if user closes browser
if (!localStorage.getItem('counter'))
    localStorage.setItem('counter', 0);

// Load current value of counter
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#counter').innerHTML = localStorage.getItem('counter');

});

function count() {
    let counter = localStorage.getItem('counter');
    counter++;

    //update counter
    document.querySelector('#counter').innerHTML = counter;
    localStorage.setItem('counter', counter);
}



// Loading Questions
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#quiz").style.display = "none";
    document.querySelector("#start").onclick = function (){
        this.style.display = "none";
        document.querySelector("#quiz").style.display = "block";
        interval = setInterval(count, 1000)
        load_question();
        
    }
});

function load_question() {

    if (question_number === total_questions) {
        document.querySelector("h2").innerHTML = "Game Over";
        document.querySelector('#options').innerHTML = `Final Score: ${correct}`;
        document.querySelector('#options').style.color = "green";
        
        clearInterval(interval);
        return;
    }

    document.querySelector("#question").innerHTML = questions[question_number].question;
    
    const options = document.querySelector("#options");
    options.innerHTML = "";

    for (const option of questions[question_number].options) {
        options.innerHTML += `<button class="option">${option}</button>`;
    }

    document.querySelectorAll(".option").forEach(option => {
        option.onclick = () => {

            if (option.textContent === questions[question_number].answer) {
                correct++;
            }
            question_number++;
            document.querySelector("#correct").innerHTML = `${correct} of ${question_number}`;
            load_question();
        }
    });
}


// RESET
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#reset').onclick = () => {
        location.reload();
        // Set values to 0
        correct = 0;
        question_number = 0;
        localStorage.setItem('counter', 0);

        // Reset timer

        if (localStorage.getItem())
        setInterval(count, 1000);

        
    }
});