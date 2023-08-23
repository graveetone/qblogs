const daysOfWeek = [
    "Неділя",
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
]

const today = new Date();
const dayName = daysOfWeek[today.getDay()];
const day = today.getDate()
const month = today.getMonth() + 1;
const year = today.getFullYear();

const hour = today.getHours();
const minutes = today.getMinutes();
const forblinkedColonHTML = "<span id='forblink'>:</span>"

const date  = `${day}.${month}.${year}`
const time = `${hour}${forblinkedColonHTML}${minutes}`

let dateTime = `${dayName}, ${date} ${time}`
document.getElementById("datetime").innerHTML = dateTime;