let selectedFile = null;

// Drag & Drop
const dropArea = document.getElementById("dropArea");

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.background = "rgba(255,255,255,0.3)";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.background = "rgba(255,255,255,0.1)";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    selectedFile = e.dataTransfer.files[0];
    document.getElementById("fileName").textContent = selectedFile.name;
});

// File input
document.getElementById("fileInput").addEventListener("change", (e) => {
    selectedFile = e.target.files[0];
    document.getElementById("fileName").textContent = selectedFile.name;
});

// Upload
async function uploadFile() {
    if (!selectedFile) {
        alert("Upload a file!");
        return;
    }

    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    loader.classList.remove("hidden");
    resultDiv.innerHTML = "";

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        loader.classList.add("hidden");

        // Sentiment class
        let sentimentClass = data.sentiment.sentiment.toLowerCase();

        let html = `
        <div class="card ${sentimentClass}">
            <h3>📊 Sentiment</h3>
            <p>${data.sentiment.sentiment} (Score: ${data.sentiment.polarity})</p>
        </div>

        <div class="card">
            <h3>🧠 Named Entities</h3>
            <ul>
                ${data.ner.map(e => `<li>${e.text} (${e.label})</li>`).join("")}
            </ul>
        </div>

        <div class="card">
            <h3>💰 Financial Data</h3>
            <pre>${JSON.stringify(data.finance, null, 2)}</pre>
        </div>
        `;

        resultDiv.innerHTML = html;

    } catch (error) {
        loader.classList.add("hidden");
        alert("Error occurred!");
        console.error(error);
    }
}
