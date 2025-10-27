const form = document.getElementById("analyze-form");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const url = document.getElementById("urlInput").value;

  const resultCard = document.getElementById("result-card");
  const resultsDiv = document.getElementById("results");
  const loadingDiv = document.getElementById("loading");

  resultCard.style.display = "block";
  resultsDiv.style.display = "none";
  loadingDiv.style.display = "block";

  fetch("/app/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  })
  .then(response => response.json())
  .then(data => {
    console.log("Backend Response:", data);
    loadingDiv.style.display = "none";
    resultsDiv.style.display = "block";

    // Fill fields with backend data
    document.getElementById("title").textContent = data.title || "N/A";
    document.getElementById("summary").textContent = data.summary || "N/A";
    document.getElementById("bias_label").textContent = data.bias_label || "N/A";
    document.getElementById("credibility_score").textContent = data.credibility_score || "N/A";
    document.getElementById("fake_score").textContent = data.fake_score || "N/A";
  })
  .catch(err => {
    loadingDiv.style.display = "none";
    resultsDiv.style.display = "block";
    document.getElementById("summary").textContent = "Error fetching data: " + err.message;
    console.error("Error:", err);
  });
});
