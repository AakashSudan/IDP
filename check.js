const apiUrl = "http://127.0.0.1:8000/realtime/";

        async function checkRealTime(field, value) {
            try {
                // Create a FormData object for the real-time check
                const formData = new FormData();
                formData.append(field, value);
                
                const fileInput = document.getElementById("file");
                if (fileInput.files.length > 0) {
                    formData.append("file", fileInput.files[0]);
                }

                const response = await fetch(apiUrl, {
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();

                const resultsDiv = document.getElementById("results");
                const existingMessage = document.querySelector(`.result-${field}`);
                if (existingMessage) existingMessage.remove();

                // Display results for this field
                const statusClass = result.status.includes("Match") ? "match" : "mismatch";
                resultsDiv.innerHTML += `<p class="result-${field} ${statusClass}">${field}: ${result.message}</p>`;
            } catch (error) {
                console.error("Error during real-time check:", error);
            }
        }

        // Attach event listeners to form inputs
        document.querySelectorAll("#uploadForm input[data-field]").forEach(input => {
            input.addEventListener("input", (event) => {
                const field = event.target.dataset.field;
                const value = event.target.value;
                checkRealTime(field, value);
            });
        });

        // Handle form submission
        document.getElementById("uploadForm").addEventListener("submit", async function (e) {
            e.preventDefault();
            const formData = new FormData(this);

            const response = await fetch("http://127.0.0.1:8000/upload/", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";

            if (response.ok) {
                resultsDiv.innerHTML += `<h3>Extracted Text:</h3><pre>${result.extracted_text}</pre>`;
                resultsDiv.innerHTML += `<h3>Verification Results:</h3>`;
                result.results.forEach(res => {
                    const statusClass = res.status.includes("Match") ? "match" : "mismatch";
                    resultsDiv.innerHTML += `<p class="${statusClass}">${res.field}: ${res.value} (${res.status})</p>`;
                });
            } else {
                resultsDiv.innerHTML = `<p class="mismatch">Error: ${result.error}</p>`;
            }
        });