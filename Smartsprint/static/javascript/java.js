
const questionCards = document.querySelectorAll('.question-card');
const nextButtons = document.querySelectorAll('.next-btn');
const backButtons = document.querySelectorAll('.back-btn');

nextButtons.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        questionCards[index].classList.remove('active');
        questionCards[index + 1].classList.add('active');
    });
});

backButtons.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        questionCards[index + 1].classList.remove('active');
        questionCards[index].classList.add('active');
    });
});
