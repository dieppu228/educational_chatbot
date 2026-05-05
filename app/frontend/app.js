// ══════════════════════════════════════════════════════════
// EduBot — Frontend (connected to FastAPI backend)
// ══════════════════════════════════════════════════════════

const API_URL = "/api/chat";

const $ = (s) => document.querySelector(s);
const chatInput = $("#chatInput");
const sendBtn = $("#sendBtn");
const chatBody = $("#chatBody");
const messagesEl = $("#messages");

let isTyping = false;
const userId = "user_" + Math.random().toString(36).slice(2, 8);

document.addEventListener("DOMContentLoaded", () => {
  // Show user ID
  const userIdEl = $(".user-id");
  if (userIdEl) userIdEl.textContent = userId;

  loadWelcome();
  setupEvents();
});

function setupEvents() {
  sendBtn.addEventListener("click", handleSend);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  });
  chatInput.addEventListener("input", () => {
    sendBtn.disabled = !chatInput.value.trim();
  });

  document.querySelectorAll(".quick-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      chatInput.value = btn.dataset.prompt;
      sendBtn.disabled = false;
      chatInput.focus();
    });
  });

  $("#newChatBtn").addEventListener("click", () => {
    messagesEl.innerHTML = "";
    loadWelcome();
  });
}

function loadWelcome() {
  addBotMessage(
    "Xin chào! Tôi là <strong>EduBot</strong> — trợ lý soạn giáo án và slide bài giảng Tin Học THPT. Hãy cho tôi biết bạn cần gì nhé!"
  );
}

// ── Send Message ──
async function handleSend() {
  const text = chatInput.value.trim();
  if (!text || isTyping) return;

  addUserMessage(text);
  chatInput.value = "";
  sendBtn.disabled = true;
  isTyping = true;

  const typingEl = showTyping();
  const book = $("#bookSelect")?.value || "auto";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, book, user_id: userId }),
    });

    removeEl(typingEl);

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    addBotMessage(formatMarkdown(data.content));

    // Show debug info in console
    if (data.debug) {
      console.log("Pipeline Debug:", data.debug);
    }
  } catch (err) {
    removeEl(typingEl);
    addBotMessage("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.<br><small style='color:#999'>" + esc(err.message) + "</small>");
  }

  isTyping = false;
}

// ── Messages ──
function addUserMessage(text) {
  const html = `
    <div class="message user">
      <div class="msg-avatar">GV</div>
      <div class="msg-content">
        <div class="msg-bubble">${esc(text)}</div>
        <div class="msg-time">${now()}</div>
      </div>
    </div>`;
  messagesEl.insertAdjacentHTML("beforeend", html);
  scrollBottom();
}

function addBotMessage(html, files) {
  let filesHtml = "";
  if (files && files.length) {
    filesHtml = files.map((f) => `
      <div class="file-card">
        <div class="file-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg>
        </div>
        <div class="file-info">
          <div class="file-name">${f.name}</div>
          <div class="file-meta">${f.type} • ${f.ext}</div>
        </div>
        <button class="file-download">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
          Tải
        </button>
      </div>`).join("");
  }

  const msg = `
    <div class="message bot">
      <div class="msg-avatar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
      </div>
      <div class="msg-content">
        <div class="msg-bubble">${html}</div>
        ${filesHtml}
        <div class="msg-time">${now()}</div>
      </div>
    </div>`;
  messagesEl.insertAdjacentHTML("beforeend", msg);
  scrollBottom();
}

function showTyping() {
  const div = document.createElement("div");
  div.className = "message bot";
  div.innerHTML = `
    <div class="msg-avatar">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
    </div>
    <div class="msg-content">
      <div class="msg-bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();
  return div;
}

// ── Markdown-lite ──
function formatMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
}

// ── Utils ──
function now() {
  const d = new Date();
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}
function esc(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
function scrollBottom() { chatBody.scrollTop = chatBody.scrollHeight; }
function removeEl(el) { if (el?.parentNode) el.parentNode.removeChild(el); }
