let currentFilename = "";

function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData
  }).then(res => res.json()).then(data => {
    if (data.success) {
      currentFilename = data.filename;
      alert("Tải lên thành công!");
      document.getElementById('chatContainer').innerHTML = '';
    }
  });
}

function askQuestion() {
  const questionInput = document.getElementById('question');
  const question = questionInput.value.trim();
  if (!question || !currentFilename) return;

  renderMessage(question, "user");
  questionInput.value = "";

  fetch("/ask", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename: currentFilename, question: question })
  }).then(res => res.json()).then(data => {
    renderMessage(data.answer, "ai");
  });
}

function renderMessage(text, sender) {
  const container = document.getElementById('chatContainer');
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.innerHTML = `<div class="bubble">${text}</div>`;
  container.appendChild(msg);
  container.scrollTop = container.scrollHeight;
}

function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    askQuestion();
  }
}
