"""
Session Store — JSON Persistence for EduBot Sessions.

Lưu/tải sessions ra file JSON.
Mỗi session = 1 file riêng: data/sessions/{session_id}.json
Index file: data/sessions/_index.json

Sau này migrate sang DB: chỉ thay implementation, interface giữ nguyên.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict
from src.llm.memory import Session

logger = logging.getLogger("chatbot.session_store")


class SessionStore:
    """
    JSON-based session persistence.

    Storage layout:
        data/sessions/
        ├── _index.json          # Session metadata index
        ├── abc-123.json         # Individual session files
        ├── def-456.json
        └── ...
    """

    def __init__(self, storage_path: str = "data/sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._index_file = self.storage_path / "_index.json"

        # Ensure index file exists
        if not self._index_file.exists():
            self._write_index([])

    # ── Save ────────────────────────────────────────────────

    def save_session(self, session: Session) -> None:
        """Save a single session to its own JSON file."""
        file_path = self.storage_path / f"{session.session_id}.json"

        try:
            data = session.to_dict()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Update index
            self._update_index(session)
            logger.debug(f"Session saved: {session.session_id} -> {file_path}")

        except Exception as e:
            logger.error(f"Failed to save session {session.session_id}: {e}")
            raise

    def save_all(self, sessions: List[Session]) -> None:
        """Batch save multiple sessions."""
        for session in sessions:
            self.save_session(session)

    def auto_save(self, session: Session) -> None:
        """
        Auto-save a session (called after important interactions).
        Same as save_session but with error swallowing for non-critical saves.
        """
        try:
            self.save_session(session)
        except Exception as e:
            logger.warning(f"Auto-save failed for session {session.session_id}: {e}")

    # ── Load ────────────────────────────────────────────────

    def load_session(self, session_id: str) -> Optional[Session]:
        """Load a single session from its JSON file."""
        file_path = self.storage_path / f"{session_id}.json"

        if not file_path.exists():
            logger.warning(f"Session file not found: {file_path}")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            session = Session.from_dict(data)
            logger.debug(f"Session loaded: {session_id}")
            return session

        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {e}")
            return None

    def load_all(self) -> List[Session]:
        """Load all sessions from storage."""
        sessions = []
        index = self._read_index()

        for entry in index:
            session = self.load_session(entry["session_id"])
            if session:
                sessions.append(session)

        logger.info(f"Loaded {len(sessions)} sessions from {self.storage_path}")
        return sessions

    # ── Query ───────────────────────────────────────────────

    def list_sessions(self) -> List[Dict]:
        """
        List all sessions (metadata only, without loading full content).

        Returns:
            List of dicts: [{"session_id": ..., "topic": ..., "intent": ..., "created_at": ..., "updated_at": ...}]
        """
        return self._read_index()

    def get_latest_session_id(self) -> Optional[str]:
        """Get the most recently updated session ID."""
        index = self._read_index()
        if not index:
            return None

        # Sort by updated_at descending
        sorted_index = sorted(index, key=lambda x: x.get("updated_at", ""), reverse=True)
        return sorted_index[0]["session_id"]

    def find_sessions_by_topic(self, topic: str) -> List[Dict]:
        """Find sessions matching a topic (simple substring match)."""
        index = self._read_index()
        return [entry for entry in index if topic.lower() in entry.get("topic", "").lower()]

    def session_exists(self, session_id: str) -> bool:
        """Check if a session file exists."""
        return (self.storage_path / f"{session_id}.json").exists()

    # ── Delete ──────────────────────────────────────────────

    def delete_session(self, session_id: str) -> bool:
        """Delete a session file and remove from index."""
        file_path = self.storage_path / f"{session_id}.json"

        try:
            if file_path.exists():
                file_path.unlink()

            # Remove from index
            index = self._read_index()
            index = [e for e in index if e["session_id"] != session_id]
            self._write_index(index)

            logger.info(f"Session deleted: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False

    # ── Index Management ────────────────────────────────────

    def _read_index(self) -> List[Dict]:
        """Read the session index file."""
        try:
            if self._index_file.exists():
                with open(self._index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read index: {e}")
        return []

    def _write_index(self, index: List[Dict]) -> None:
        """Write the session index file."""
        try:
            with open(self._index_file, "w", encoding="utf-8") as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to write index: {e}")

    def _update_index(self, session: Session) -> None:
        """Update or add a session entry in the index."""
        index = self._read_index()

        entry = {
            "session_id": session.session_id,
            "topic": session.topic,
            "intent": session.intent,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }

        # Update existing or append new
        updated = False
        for i, e in enumerate(index):
            if e["session_id"] == session.session_id:
                index[i] = entry
                updated = True
                break

        if not updated:
            index.append(entry)

        self._write_index(index)


__all__ = ["SessionStore"]
