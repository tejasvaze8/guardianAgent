var cursor_x = -1;
var cursor_y = -1;

function trackMouse(event) {
 cursor_x = event.pageY;
 cursor_y = event.pageX;
}

document.onmousemove = trackMouse;

async function getGeneratedText() {
    const url = "http://127.0.0.1:5000/generate";
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    return data.generation;
}

function createCard(text, x, y) {
    console.log(text);
    const card = document.createElement("div");

    card.style.width = "300px";
    card.style.height = "auto";
    card.style.backgroundColor = "white";
    card.style.textAlign = "center";
    card.style.zIndex = "99999";

    card.style.color = "#aaa";
    card.style.background = "$fafafa";
    card.style.boxShadow = "0 5px 50px 1px";
    card.style.borderRadius = "0.4em";

    card.style.position = "absolute";
    card.style.top = `${x}px`;
    card.style.left = `${y}px`;

    const cardText = document.createElement("p");
    cardText.innerText = text;
    cardText.style.paddingTop = "50px";
    cardText.style.paddingBottom = "50px";
    cardText.style.paddingRight = "20px";
    cardText.style.paddingLeft = "20px";
    cardText.style.color = "black";

    card.appendChild(cardText);

    document.body.appendChild(card);
}

function createSelectionCard(x, y) {
    const card = document.createElement("div");

    card.style.height = "auto";
    card.style.backgroundColor = "white";
    card.style.textAlign = "center";
    card.style.zIndex = "99999";
    card.className = "selection-card";

    card.style.color = "#ddd";
    card.style.background = "$fafafa";
    card.style.boxShadow = "0px 5px 10px 0px";
    card.style.borderRadius = "0.4em";

    card.style.position = "absolute";
    card.style.top = `${x - 80}px`;
    card.style.left = `${y}px`;

    const cardText = document.createElement("p");
    cardText.innerText = "This is a test card.";
    cardText.style.paddingTop = "10px";
    cardText.style.paddingBottom = "10px";
    cardText.style.paddingRight = "10px";
    cardText.style.paddingLeft = "10px";
    cardText.style.color = "black";

    card.appendChild(cardText);

    document.body.appendChild(card);
}

function removeAllSelectionCards() {
    var elements = document.getElementsByClassName("selection-card");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}

function debounce(fn, delay) {
  let timer = null;
  return function () {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
};

document.addEventListener("selectionchange", debounce(function (event) {
    let selection = document.getSelection ? document.getSelection().toString() :  document.selection.createRange().toString();
    removeAllSelectionCards();
    if (selection && /\S/.test(selection)) {
        console.log(selection, cursor_x, cursor_y);
        createSelectionCard(cursor_x, cursor_y);
    }
}, 250));

getGeneratedText().then((text) => {
    console.log(text);
    createCard(text, 30, 30);
});
