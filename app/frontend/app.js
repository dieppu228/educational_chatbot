// ══════════════════════════════════════════════════════════
// EduBot — Frontend (connected to FastAPI backend)
// ══════════════════════════════════════════════════════════

const API_URL = "/api/chat";

const $ = (s) => document.querySelector(s);
const chatInput = $("#chatInput");
const sendBtn = $("#sendBtn");
const chatBody = $("#chatBody");
const messagesEl = $("#messages");
const bookSelect = $("#bookSelect");
const gradeSelect = $("#gradeSelect");
const chatBookInfo = $("#chatBookInfo");

let isTyping = false;
let userId = getOrCreateUserId();
let pendingHitl = null;

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
    sendBtn.disabled = pendingHitl || !chatInput.value.trim();
  });
  bookSelect?.addEventListener("change", updateScopeLabel);
  gradeSelect?.addEventListener("change", updateScopeLabel);
  updateScopeLabel();

  document.querySelectorAll(".quick-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      chatInput.value = btn.dataset.prompt;
      sendBtn.disabled = false;
      chatInput.focus();
    });
  });

  $("#newChatBtn").addEventListener("click", () => {
    userId = createUserId();
    localStorage.setItem("edubot_user_id", userId);
    pendingHitl = null;
    setChatLocked(false);
    const userIdEl = $(".user-id");
    if (userIdEl) userIdEl.textContent = userId;
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
  if (!text || isTyping || pendingHitl) return;

  addUserMessage(text);
  chatInput.value = "";
  sendBtn.disabled = true;
  isTyping = true;

  const typingEl = showTyping();
  const book = bookSelect?.value || "auto";
  const grade = gradeSelect?.value || "auto";

  try {
    const data = await sendChatPayload({ message: text, book, grade, user_id: userId });
    removeEl(typingEl);
    handleBotResponse(data);
  } catch (err) {
    removeEl(typingEl);
    addBotMessage("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.<br><small style='color:#999'>" + esc(err.message) + "</small>");
  }

  isTyping = false;
}

async function sendChatPayload(payload) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

function handleBotResponse(data) {
  const files = data.export ? [{
    name: data.export.filename || "slide_bai_giang.pptx",
    type: "PPTX",
    ext: "pptx",
    url: data.export.download_url,
  }] : [];
  addBotMessage(formatMarkdown(data.content || ""), files);
  if (data.debug) {
    console.log("Pipeline Debug:", data.debug);
  }
  if (data.hitl?.type === "outline_review") {
    pendingHitl = data.hitl;
    setChatLocked(true);
    renderOutlineReview(data.hitl);
  } else {
    pendingHitl = null;
    setChatLocked(false);
  }
}

function setChatLocked(locked) {
  chatInput.disabled = locked;
  chatInput.placeholder = locked ? "Đang chờ duyệt dàn ý..." : "Hỏi bài, yêu cầu soạn giáo án, tạo slide...";
  sendBtn.disabled = locked || !chatInput.value.trim();
  document.querySelectorAll(".quick-btn").forEach((btn) => { btn.disabled = locked; });
}

function renderOutlineReview(hitl) {
  removeEl($("#hitlPanel"));
  const outline = hitl.outline || {};
  const slides = Array.isArray(outline.slides) ? outline.slides : [];
  const slideHtml = slides.map((slide, idx) => `
    <div class="hitl-slide" data-slide-index="${idx}">
      <div class="hitl-slide-head">
        <span>${idx + 1}</span>
        <select class="hitl-type" disabled>
          ${["title", "content", "exercise", "summary", "image"].map((type) =>
            `<option value="${type}" ${slide.slide_type === type ? "selected" : ""}>${type}</option>`
          ).join("")}
        </select>
      </div>
      <input class="hitl-title" value="${escAttr(slide.title || "")}" disabled>
      <input class="hitl-objective" value="${escAttr(slide.objective || "")}" disabled>
      <textarea class="hitl-keypoints" disabled>${esc((slide.key_points || []).join("\n"))}</textarea>
      <input class="hitl-sources" value="${escAttr((slide.source_chunk_ids || []).join(", "))}" disabled>
    </div>
  `).join("");

  const panel = `
    <div class="message bot" id="hitlPanel">
      <div class="msg-avatar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
      </div>
      <div class="msg-content hitl-content">
        <div class="hitl-card">
          <div class="hitl-header">
            <div class="hitl-title-label">Duyệt dàn ý</div>
            <input class="hitl-lesson" value="${escAttr(outline.lesson_title || "")}" disabled>
          </div>
          <div class="hitl-slides">${slideHtml}</div>
          <div class="hitl-actions">
            <button class="hitl-btn primary" data-hitl-action="approve">Duyệt</button>
            <button class="hitl-btn" data-hitl-action="edit">Cần chỉnh sửa</button>
            <button class="hitl-btn primary hidden" data-hitl-action="submit-edit">Gửi chỉnh sửa</button>
          </div>
        </div>
      </div>
    </div>`;

  messagesEl.insertAdjacentHTML("beforeend", panel);
  const el = $("#hitlPanel");
  el.querySelector('[data-hitl-action="approve"]').addEventListener("click", approveOutline);
  el.querySelector('[data-hitl-action="edit"]').addEventListener("click", enableOutlineEdit);
  el.querySelector('[data-hitl-action="submit-edit"]').addEventListener("click", submitEditedOutline);
  scrollBottom();
}

function enableOutlineEdit() {
  const panel = $("#hitlPanel");
  if (!panel) return;
  panel.querySelectorAll("input, textarea, select").forEach((el) => { el.disabled = false; });
  panel.querySelector('[data-hitl-action="edit"]').classList.add("hidden");
  panel.querySelector('[data-hitl-action="submit-edit"]').classList.remove("hidden");
}

async function approveOutline() {
  await sendHitlDecision({
    message: "Duyệt dàn ý",
    hitl_type: "outline_review",
    hitl_approved: true,
  });
}

async function submitEditedOutline() {
  await sendHitlDecision({
    message: "Gửi dàn ý đã chỉnh sửa",
    hitl_type: "outline_review",
    hitl_approved: false,
    edited_outline: collectEditedOutline(),
  });
}

async function sendHitlDecision(extraPayload) {
  if (!pendingHitl || isTyping) return;
  isTyping = true;
  addUserMessage(extraPayload.hitl_approved ? "Duyệt dàn ý" : "Gửi dàn ý đã chỉnh sửa");
  const typingEl = showTyping();
  disableHitlButtons(true);
  const book = bookSelect?.value || "auto";
  const grade = gradeSelect?.value || "auto";
  try {
    const data = await sendChatPayload({ ...extraPayload, book, grade, user_id: userId });
    removeEl(typingEl);
    removeEl($("#hitlPanel"));
    handleBotResponse(data);
  } catch (err) {
    removeEl(typingEl);
    addBotMessage("Xin lỗi, đã có lỗi xảy ra khi duyệt dàn ý.<br><small style='color:#999'>" + esc(err.message) + "</small>");
    disableHitlButtons(false);
  }
  isTyping = false;
}

function disableHitlButtons(disabled) {
  document.querySelectorAll(".hitl-btn").forEach((btn) => { btn.disabled = disabled; });
}

function collectEditedOutline() {
  const panel = $("#hitlPanel");
  const originalSlides = pendingHitl?.outline?.slides || [];
  const slides = Array.from(panel.querySelectorAll(".hitl-slide")).map((row, idx) => {
    const original = originalSlides[idx] || {};
    return {
      ...original,
      slide_type: row.querySelector(".hitl-type").value,
      title: row.querySelector(".hitl-title").value.trim(),
      objective: row.querySelector(".hitl-objective").value.trim(),
      key_points: row.querySelector(".hitl-keypoints").value.split("\n").map((s) => s.trim()).filter(Boolean),
      source_chunk_ids: row.querySelector(".hitl-sources").value.split(",").map((s) => s.trim()).filter(Boolean),
    };
  });
  return {
    ...(pendingHitl?.outline || {}),
    lesson_title: panel.querySelector(".hitl-lesson").value.trim(),
    slides,
  };
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
          <div class="file-name">${esc(f.name)}</div>
          <div class="file-meta">${esc(f.type)} • ${esc(f.ext)}</div>
        </div>
        <a class="file-download" href="${escAttr(f.url || "#")}" download="${escAttr(f.name)}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
          Tải
        </a>
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
function createUserId() { return "user_" + Math.random().toString(36).slice(2, 10); }
function getOrCreateUserId() {
  const stored = localStorage.getItem("edubot_user_id");
  if (stored) return stored;
  const next = createUserId();
  localStorage.setItem("edubot_user_id", next);
  return next;
}
function updateScopeLabel() {
  if (!chatBookInfo) return;
  const bookLabels = { auto: "Tự động", CD: "Cánh Diều", KNTT: "Kết nối tri thức" };
  const gradeLabels = { auto: "Tự động", 10: "Lớp 10", 11: "Lớp 11", 12: "Lớp 12" };
  const book = bookLabels[bookSelect?.value || "auto"] || "Tự động";
  const grade = gradeLabels[gradeSelect?.value || "auto"] || "Tự động";
  chatBookInfo.textContent = `${book} - ${grade}`;
}
function esc(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
function escAttr(s) { return esc(s).replace(/"/g, "&quot;"); }
function scrollBottom() { chatBody.scrollTop = chatBody.scrollHeight; }
function removeEl(el) { if (el?.parentNode) el.parentNode.removeChild(el); }
