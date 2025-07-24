const questionInput = document.getElementById("questionInput");
const answerBox = document.getElementById("answerContent");

function submitQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  answerBox.innerHTML = ""; // Clear old answer/chart

  fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  })
    .then((res) => {
      if (!res.ok) throw new Error("Server error");
      return res.json();
    })
    .then(async (data) => {
      console.log("Backend response:", data);

      // Type the raw answer
      await typeText(answerBox, JSON.stringify(data.answer, null, 2));

      // Render chart only if valid tabular with 2+ keys
      if (
        Array.isArray(data.answer) &&
        data.answer.length > 0 &&
        Object.keys(data.answer[0]).length >= 2 &&
        isTabular(data.answer)
      ) {
        renderChart(data.answer);
      } else {
        answerBox.innerHTML += `<p><i>Chart rendering coming soon!</i></p>`;
      }
    })
    .catch((err) => {
      console.error("Fetch failed:", err);
      answerBox.innerHTML = "<span style='color:red'>Error: Failed to fetch</span>";
    });
}

// Typing effect
async function typeText(container, text) {
  const delay = 10;
  for (let i = 0; i < text.length; i++) {
    container.innerHTML += text.charAt(i);
    await new Promise((resolve) => setTimeout(resolve, delay));
  }
}

// Plotly bar chart
function renderChart(data) {
  const keys = Object.keys(data[0]);
  const xKey = keys[0];
  const yKey = keys[1];

  const trace = {
    x: data.map((row) => row[xKey]),
    y: data.map((row) => row[yKey]),
    type: "bar",
    marker: { color: "purple" }
  };

  const layout = {
    title: `${yKey} by ${xKey}`,
    xaxis: { title: xKey },
    yaxis: { title: yKey },
    margin: { t: 40 }
  };

  const chartDiv = document.createElement("div");
  answerBox.appendChild(chartDiv);
  Plotly.newPlot(chartDiv, [trace], layout);
}

// Tabular checker
function isTabular(data) {
  if (!Array.isArray(data)) return false;
  if (data.length === 0) return false;
  const keys = Object.keys(data[0]);
  return data.every(
    (item) =>
      typeof item === "object" &&
      Object.keys(item).length === keys.length &&
      keys.every((k) => k in item)
  );
}
