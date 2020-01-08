// Select people
let people = document.querySelectorAll(".guest-number");

people.forEach(function (guest) {
  guest.addEventListener("click", addGuest);
});

function addGuest() {
  people.forEach(function (guest) {
    guest.classList.remove("selected");
    guest.classList.add("guest-number");
  });
  this.classList.add("selected");
  guestNumber = this.getAttribute("value");
}

// Select date
let date = document.querySelector(".calendar-html");

// Select time
let items = document.querySelectorAll(".item");

console.log(items)

items.forEach(function (item) {
  item.addEventListener("click", addTime)
});
function addTime() {
  items.forEach(function (item) {
    item.classList.remove("selected");
    item.classList.add("item")
  });
  this.classList.add("selected");
  hour = this.getAttribute("value")
}

let button = document.querySelector("#button-res");
button.addEventListener("click", function () {
  console.log(guestNumber);
  console.log(hour);
  console.log(date.value);
});
