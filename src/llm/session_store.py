import json
import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Dict
from src.llm.memory import Session

logger = logging.getLogger("chatbot.session_store")


class SessionStore:

    def __init__(self, storage_path: str = "data/sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._index_file = self.storage_path / "_index.json"

        # Ensure index file exists
        if not self._index_file.exists():
            self._write_index([])

    # ── Save ────────────────────────────────────────────────

    def save_session(self, session: Session) -> None:
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
        for session in sessions:
            self.save_session(session)

    def auto_save(self, session: Session) -> None:
        try:
            self.save_session(session)
        except Exception as e:
            logger.warning(f"Auto-save failed for session {session.session_id}: {e}")

    # ── Load ────────────────────────────────────────────────

    def load_session(self, session_id: str) -> Optional[Session]:
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
        return self._read_index()

    def get_latest_session_id(self) -> Optional[str]:
        index = self._read_index()
        if not index:
            return None

        # Sort by updated_at descending
        sorted_index = sorted(index, key=lambda x: x.get("updated_at", ""), reverse=True)
        return sorted_index[0]["session_id"]

    def find_sessions_by_topic(self, topic: str) -> List[Dict]:
        index = self._read_index()
        return [entry for entry in index if topic.lower() in entry.get("topic", "").lower()]

    def session_exists(self, session_id: str) -> bool:
        return (self.storage_path / f"{session_id}.json").exists()

    # ── Delete ──────────────────────────────────────────────

    def delete_session(self, session_id: str) -> bool:
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
        try:
            if self._index_file.exists():
                with open(self._index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read index: {e}")
        return []

    def _write_index(self, index: List[Dict]) -> None:
        try:
            with open(self._index_file, "w", encoding="utf-8") as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to write index: {e}")

    def _update_index(self, session: Session) -> None:
        index = self._read_index()

        entry = {
            "session_id": session.session_id,
            "user_id": session.user_id,
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

    # ── Async Methods ───────────────────────────────────────

    async def save_session_async(self, session: Session) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_session, session)

    async def load_session_async(self, session_id: str) -> Optional[Session]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_session, session_id)

    async def auto_save_async(self, session: Session) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.auto_save, session)


__all__ = ["SessionStore"]
