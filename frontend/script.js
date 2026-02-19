const summarizeBtn = document.getElementById("summarizeBtn");
const output = document.getElementById("output");

summarizeBtn.addEventListener("click", () => {
    const text = document.getElementById("textInput").value.trim();
    const pdfFile = document.getElementById("pdfInput").files[0];
    const mode = document.getElementById("mode").value;

    output.innerText = "⏳ Summarizing...";

    // ---------------- PDF FLOW ----------------
    if (pdfFile) {
        const formData = new FormData();
        formData.append("file", pdfFile);
        formData.append("mode", mode);

        fetch("http://127.0.0.1:5000/summarize-pdf", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                output.innerText = data.error;
            } else {
                renderSummary(data.summary, mode);
            }
        })
        .catch(err => {
            console.error(err);
            output.innerText = "❌ Error connecting to server (PDF)";
        });

        return;
    }

    // ---------------- TEXT FLOW ----------------
    if (!text) {
        output.innerText = "⚠️ Please enter text or upload a PDF.";
        return;
    }

    fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text, mode })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            output.innerText = data.error;
        } else {
            renderSummary(data.summary, mode);
        }
    })
    .catch(err => {
        console.error(err);
        output.innerText = "❌ Error connecting to server (Text)";
    });
});

// ---------------- BULLET RENDERING ----------------
function renderSummary(summary, mode) {
    if (mode === "bullet") {
        const lines = summary
            .split("\n")
            .map(l => l.trim())
            .filter(l => l.startsWith("*"));

        if (lines.length) {
            let html = "<ul>";
            lines.forEach(line => {
                html += `<li>${line.replace("*", "").trim()}</li>`;
            });
            html += "</ul>";
            output.innerHTML = html;
        } else {
            output.innerText = summary;
        }
    } else {
        output.innerText = summary;
    }
}
