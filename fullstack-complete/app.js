async function upload() {

    const fileInput = document.getElementById("fileInput");
    const loading = document.getElementById("loading");
    const resultDiv = document.getElementById("result");

    if (fileInput.files.length === 0) {
        alert("Please upload a PDF!");
        return;
    }

    const file = fileInput.files[0];

    let formData = new FormData();
    formData.append("file", file);

    loading.classList.remove("hidden");
    resultDiv.innerHTML = "";

    try {

        const response = await fetch("http://127.0.0.1:8000/full-analysis/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        loading.classList.add("hidden");

        let nerHTML = data.ner.map(e =>
            `<li>${e.word} (${e.label})</li>`
        ).join("");

        let sentimentHTML = data.sentiment_raw.sentence_wise.map(s =>
            `<li>${s.sentence} → ${s.label} (${s.score.toFixed(2)})</li>`
        ).join("");

        let overall = data.sentiment_raw.overall;

        let overallHTML = `
            <p><b>Positive:</b> ${overall.positive}%</p>
            <p><b>Negative:</b> ${overall.negative}%</p>
            <p><b>Neutral:</b> ${overall.neutral}%</p>
        `;

        resultDiv.innerHTML = `
            <div class="card">
                <h2>📄 Markdown Output</h2>
                <p>${data.pdf_to_markdown.substring(0, 800)}...</p>
            </div>

            <div class="card">
                <h2>🏷 NER</h2>
                <ul>${nerHTML}</ul>
            </div>

            <div class="card">
                <h2>😊 Sentiment Analysis</h2>
                ${overallHTML}
                <ul>${sentimentHTML}</ul>
            </div>

            <div class="card">
                <h2>🌍 Language Extraction (Groq)</h2>
                <pre>${JSON.stringify(data.language_extraction, null, 2)}</pre>
            </div>
        `;

    } catch (error) {
        loading.classList.add("hidden");
        alert("Error connecting backend!");
        console.error(error);
    }
}