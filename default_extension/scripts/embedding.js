console.log("here");

async function sendEmbedding(url) {
    console.log("Url: ", url);
    const rawResponse = await fetch('http://127.0.0.1:5000/embedding', {
        method: 'POST',
        mode: "no-cors",
        credentials: "same-origin",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    });
}


chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
    console.log(message);
    var url = "https://www.theguardian.com/uk";
    chrome.tabs.create({ url: "hi" });
    sendResponse({ farewell: "goodbye" });
});
