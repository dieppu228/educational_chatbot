import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowUp,
  BookOpen,
  Bot,
  Check,
  ChevronDown,
  Download,
  FileDown,
  GraduationCap,
  Menu,
  MessageSquarePlus,
  MonitorPlay,
  Pencil,
  Sparkles,
  UserRound,
  X,
} from "lucide-react";

const API_URL = "/api/chat";
const STREAM_API_URL = "/api/chat/stream";

const BOOKS = [
  { value: "auto", label: "Tự động" },
  { value: "CD", label: "Cánh Diều" },
  { value: "KNTT", label: "Kết nối tri thức" },
];

const GRADES = [
  { value: "auto", label: "Tự động" },
  { value: "10", label: "Lớp 10" },
  { value: "11", label: "Lớp 11" },
  { value: "12", label: "Lớp 12" },
];

const QUICK_ACTIONS = [
  { label: "Tạo bài tập", prompt: "Tạo 5 câu trắc nghiệm cho bài này", icon: GraduationCap },
  { label: "Soạn giáo án", prompt: "Soạn giáo án chi tiết cho bài này", icon: FileDown },
  { label: "Tạo slide", prompt: "Tạo slide bài giảng cho bài này", icon: MonitorPlay },
];

function createUserId() {
  return `user_${Math.random().toString(36).slice(2, 10)}`;
}

function getOrCreateUserId() {
  const stored = localStorage.getItem("edubot_user_id");
  if (stored) return stored;
  const id = createUserId();
  localStorage.setItem("edubot_user_id", id);
  return id;
}

function timeNow() {
  return new Intl.DateTimeFormat("vi-VN", { hour: "2-digit", minute: "2-digit" }).format(new Date());
}

function createWelcomeMessage() {
  return {
    id: crypto.randomUUID(),
    role: "assistant",
    content: "Xin chào! Mình là EduBot. Bạn có thể hỏi kiến thức Tin học, tạo bài tập, slide hoặc giáo án theo đúng bộ sách và khối lớp.",
    time: timeNow(),
  };
}

async function sendChat(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function sendChatStream(payload, onEvent) {
  const response = await fetch(STREAM_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  if (!response.body) {
    onEvent(await response.json());
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed) onEvent(JSON.parse(trimmed));
    }
  }

  buffer += decoder.decode();
  const trimmed = buffer.trim();
  if (trimmed) onEvent(JSON.parse(trimmed));
}

function ScopeSelect({ icon: Icon, label, value, options, onChange }) {
  return (
    <label className="scope-field">
      <span className="scope-label"><Icon size={15} />{label}</span>
      <span className="select-shell">
        <select value={value} onChange={(event) => onChange(event.target.value)}>
          {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
        </select>
        <ChevronDown size={15} />
      </span>
    </label>
  );
}

function Avatar({ role, active = false }) {
  const isBot = role === "assistant";
  return (
    <span className={`avatar ${isBot ? "bot-avatar" : "user-avatar"} ${active ? "active" : ""}`}>
      {isBot ? <Bot size={19} /> : <UserRound size={18} />}
      {isBot && <span className="avatar-presence" />}
    </span>
  );
}

function InlineText({ text }) {
  const parts = String(text).split(/(\*\*.*?\*\*|`.*?`)/g);
  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) return <strong key={index}>{part.slice(2, -2)}</strong>;
    if (part.startsWith("`") && part.endsWith("`")) return <code key={index}>{part.slice(1, -1)}</code>;
    return <span key={index}>{part}</span>;
  });
}

function RichText({ text }) {
  return String(text || "").split("\n").map((line, index) => (
    <span className="text-line" key={`${index}-${line.slice(0, 12)}`}>
      <InlineText text={line} />
    </span>
  ));
}

function ExportCard({ file }) {
  if (!file) return null;
  return (
    <div className="export-card">
      <span className="export-icon"><FileDown size={20} /></span>
      <span className="export-copy">
        <strong>{file.filename || "tai_lieu.pptx"}</strong>
        <small>Tệp PowerPoint</small>
      </span>
      <a href={file.download_url} download={file.filename} title="Tải tệp"><Download size={17} /></a>
    </div>
  );
}

function Message({ message }) {
  return (
    <article className={`message ${message.role}`}>
      <Avatar role={message.role} />
      <div className="message-content">
        <div className="message-bubble"><RichText text={message.content} /></div>
        <ExportCard file={message.export} />
        <time>{message.time}</time>
      </div>
    </article>
  );
}

function TypingMessage({ status }) {
  return (
    <article className="message assistant">
      <Avatar role="assistant" active />
      <div className="message-content">
        <div className="message-bubble typing">
          <span /><span /><span />
          {status && <strong>{status}</strong>}
        </div>
      </div>
    </article>
  );
}

function OutlineReview({ hitl, busy, onApprove, onSubmit }) {
  const [editing, setEditing] = useState(false);
  const [outline, setOutline] = useState(hitl.outline || {});
  const slides = Array.isArray(outline.slides) ? outline.slides : [];

  const updateSlide = (index, field, value) => {
    setOutline((current) => ({
      ...current,
      slides: current.slides.map((slide, slideIndex) => slideIndex === index ? { ...slide, [field]: value } : slide),
    }));
  };

  return (
    <section className="outline-review">
      <div className="outline-heading">
        <div><span>Dàn ý cần duyệt</span><strong>{outline.lesson_title || "Dàn ý bài học"}</strong></div>
        <span className="outline-count">{slides.length} phần</span>
      </div>
      <div className="outline-list">
        {slides.map((slide, index) => (
          <div className="outline-item" key={slide.slide_id || index}>
            <span className="outline-index">{String(index + 1).padStart(2, "0")}</span>
            <div className="outline-fields">
              <input disabled={!editing} value={slide.title || ""} onChange={(event) => updateSlide(index, "title", event.target.value)} />
              <textarea disabled={!editing} value={(slide.key_points || []).join("\n")} onChange={(event) => updateSlide(index, "key_points", event.target.value.split("\n").filter(Boolean))} />
            </div>
          </div>
        ))}
      </div>
      <div className="outline-actions">
        {!editing && <button className="secondary-button" onClick={() => setEditing(true)} disabled={busy}><Pencil size={16} />Chỉnh sửa</button>}
        {editing && <button className="secondary-button" onClick={() => onSubmit(outline)} disabled={busy}><Check size={16} />Gửi chỉnh sửa</button>}
        <button className="primary-button" onClick={onApprove} disabled={busy}><Check size={16} />Duyệt dàn ý</button>
      </div>
    </section>
  );
}

export default function App() {
  const [userId, setUserId] = useState(getOrCreateUserId);
  const [book, setBook] = useState("auto");
  const [grade, setGrade] = useState("auto");
  const [messages, setMessages] = useState([createWelcomeMessage()]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [pendingHitl, setPendingHitl] = useState(null);
  const [latestExport, setLatestExport] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentStatus, setCurrentStatus] = useState("");
  const messageEndRef = useRef(null);

  useEffect(() => messageEndRef.current?.scrollIntoView({ behavior: "smooth" }), [messages, busy, pendingHitl, currentStatus]);

  const scopeText = useMemo(() => {
    const bookLabel = BOOKS.find((item) => item.value === book)?.label;
    const gradeLabel = GRADES.find((item) => item.value === grade)?.label;
    return `${bookLabel} · ${gradeLabel}`;
  }, [book, grade]);

  const addMessage = (role, content, extra = {}) => {
    setMessages((current) => [...current, { id: crypto.randomUUID(), role, content, time: timeNow(), ...extra }]);
  };

  const handleResponse = (data) => {
    addMessage("assistant", data.content || "Mình chưa nhận được nội dung phản hồi.", { export: data.export });
    if (data.export) setLatestExport(data.export);
    setPendingHitl(data.hitl?.type === "outline_review" ? data.hitl : null);
    if (data.debug) console.info("Pipeline Debug", data.debug);
  };

  const submitPayload = async (payload) => {
    setBusy(true);
    setCurrentStatus("Đang xử lý yêu cầu...");
    try {
      await sendChatStream({ ...payload, book, grade, user_id: userId }, (event) => {
        if (event.type === "status") {
          setCurrentStatus(event.text);
          return;
        }
        if (event.type === "final") {
          handleResponse(event);
        }
      });
    } catch (error) {
      addMessage("assistant", `Không thể kết nối tới hệ thống. ${error.message}`);
    } finally {
      setCurrentStatus("");
      setBusy(false);
    }
  };

  const handleSend = async (prompt = input) => {
    const text = prompt.trim();
    if (!text || busy || pendingHitl) return;
    addMessage("user", text);
    setInput("");
    await submitPayload({ message: text });
  };

  const handleHitl = async (approved, editedOutline) => {
    addMessage("user", approved ? "Duyệt dàn ý" : "Gửi dàn ý đã chỉnh sửa");
    await submitPayload({
      message: approved ? "Duyệt dàn ý" : "Gửi dàn ý đã chỉnh sửa",
      hitl_type: "outline_review",
      hitl_approved: approved,
      edited_outline: editedOutline,
    });
  };

  const resetChat = () => {
    const nextUserId = createUserId();
    localStorage.setItem("edubot_user_id", nextUserId);
    setUserId(nextUserId);
    setMessages([createWelcomeMessage()]);
    setPendingHitl(null);
    setLatestExport(null);
    setInput("");
    setSidebarOpen(false);
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="brand-row">
          <span className="brand-mark"><Sparkles size={21} /></span>
          <div><strong>EduBot</strong><span>Trợ lý học tập AI</span></div>
          <button className="mobile-close" onClick={() => setSidebarOpen(false)} title="Đóng"><X size={20} /></button>
        </div>

        <button className="new-chat" onClick={resetChat}><MessageSquarePlus size={18} />Cuộc trò chuyện mới</button>

        <div className="scope-panel">
          <div className="panel-title"><span>Phạm vi học liệu</span><small>Tùy chọn</small></div>
          <ScopeSelect icon={BookOpen} label="Bộ sách" value={book} options={BOOKS} onChange={setBook} />
          <ScopeSelect icon={GraduationCap} label="Khối lớp" value={grade} options={GRADES} onChange={setGrade} />
          <p>Để tự động, hệ thống sẽ nhận diện phạm vi trực tiếp từ câu hỏi.</p>
        </div>

        <div className="sidebar-spacer" />
        <div className="profile-row">
          <Avatar role="user" />
          <div><strong>Người dùng</strong><span>{userId}</span></div>
          <span className="online-dot" title="Đang hoạt động" />
        </div>
      </aside>

      {sidebarOpen && <button className="sidebar-backdrop" onClick={() => setSidebarOpen(false)} aria-label="Đóng menu" />}

      <main className="workspace">
        <header className="workspace-header">
          <button className="mobile-menu" onClick={() => setSidebarOpen(true)} title="Mở menu"><Menu size={20} /></button>
          <div><h1>Không gian học tập</h1><span><span className="status-dot" />{scopeText}</span></div>
          {latestExport ? (
            <a className="header-download" href={latestExport.download_url} download={latestExport.filename}><Download size={17} /><span>Tải tài liệu</span></a>
          ) : <span className="header-badge"><Sparkles size={15} />AI sẵn sàng</span>}
        </header>

        <section className="chat-scroll">
          <div className="chat-column">
            <div className="assistant-intro"><span><Bot size={17} /></span><div><strong>EduBot</strong><small>Sẵn sàng hỗ trợ theo SGK Tin học THPT</small></div></div>
            {messages.map((message) => <Message key={message.id} message={message} />)}
            {pendingHitl && (
              <OutlineReview
                hitl={pendingHitl}
                busy={busy}
                onApprove={() => handleHitl(true)}
                onSubmit={(outline) => handleHitl(false, outline)}
              />
            )}
            {busy && <TypingMessage status={currentStatus} />}
            <div ref={messageEndRef} />
          </div>
        </section>

        <footer className="composer-area">
          <div className="quick-actions">
            {QUICK_ACTIONS.map(({ label, prompt, icon: Icon }) => (
              <button key={label} onClick={() => setInput(prompt)} disabled={busy || pendingHitl}><Icon size={15} />{label}</button>
            ))}
          </div>
          <div className={`composer ${pendingHitl ? "locked" : ""}`}>
            <textarea
              rows="1"
              value={input}
              disabled={busy || Boolean(pendingHitl)}
              placeholder={pendingHitl ? "Duyệt dàn ý để tiếp tục" : "Hỏi kiến thức, tạo bài tập, slide hoặc giáo án..."}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  handleSend();
                }
              }}
            />
            <button className="send-button" onClick={() => handleSend()} disabled={!input.trim() || busy || Boolean(pendingHitl)} title="Gửi"><ArrowUp size={19} /></button>
          </div>
          <p>EduBot có thể mắc lỗi. Hãy đối chiếu thông tin quan trọng với tài liệu học tập.</p>
        </footer>
      </main>
    </div>
  );
}
