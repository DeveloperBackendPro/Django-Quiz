$(document).ready(function () {
    document.getElementById("current-year").innerHTML = new Date().getFullYear();
    document.getElementById("current-month").innerHTML = new Date().getMonth() + 1;
    document.getElementById("current-day").innerHTML = new Date().getDate();
});

function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;
}

setInterval(updateClock, 1000);
updateClock();