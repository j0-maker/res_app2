// Select people
let people = document.querySelectorAll(".guest-number");

people.forEach(function (guest) {
  guest.addEventListener("click", addGuest);
});

function addGuest() {
  people.forEach(function (guest) {
    guest.style.background = "#3b5998";
  });
  this.style.background = "rgb(37, 168, 185)";
  guestNumber = this.getAttribute("value");
}

// Select date
let date = document.querySelector(".calendar-html");

// Select time
let items = document.querySelectorAll(".item");

items.forEach(function (item) {
  item.addEventListener("click", addTime);
});
function addTime() {
  items.forEach(function (item) {
    item.style.background = "#3b5998";
  });
  this.style.background = "rgb(37, 168, 185)";
  hour = this.getAttribute("value");
}

let button = document.querySelector("#button-res");
button.addEventListener("click", function () {
  console.log(guestNumber);
  console.log(hour);
  console.log(date.value);
});
