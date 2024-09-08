let timeLeft = 60;
const counterElement = document.getElementById('counter');

// تابع شمارش معکوس
const countdown = setInterval(() => {
    if (timeLeft <= 0) {
        clearInterval(countdown);
        counterElement.innerHTML = `<a href="#">ارسال مجدد</a>`;
    } else {
        counterElement.innerHTML = timeLeft;
        timeLeft--;
    }
}, 1000);
