let timeLeft = 10;
const counterElement = document.getElementById('counter');

// تابع شمارش معکوس
const countdown = setInterval(() => {
    if (timeLeft <= 0) {
        clearInterval(countdown);
        counterElement.innerHTML = "کد منقضی شده است";
    } else {
        counterElement.innerHTML = timeLeft;
        timeLeft--;
    }
}, 1000);
