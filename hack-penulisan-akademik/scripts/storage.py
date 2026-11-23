"""I/O dasar workspace dan berkas bukti; hanya menggunakan pustaka standar Python."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ThesisError(Exception):
    """Kesalahan domain yang perlu disampaikan tanpa disembunyikan kepada pengguna."""


def timestamp() -> str:
    """Mengembalikan waktu UTC ISO 8601 untuk jejak perubahan."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path, default: Any = None) -> Any:
    """Membaca JSON dan memberi konteks jika dokumen salah format."""
    if not path.exists():
        if default is not None:
            return default
        raise ThesisError(f"Berkas tidak ditemukan: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (ValueError, OSError) as exc:
        raise ThesisError(f"Gagal membaca JSON {path}: {exc}") from exc


def write_json(path: Path, content: Any) -> None:
    """Menyimpan JSON secara atomik agar berkas tidak terpotong jika proses terhenti."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = ""
    try:
        with tempfile.NamedTemporaryFile("w", dir=path.parent, suffix=".tmp", encoding="utf-8", delete=False) as handle:
            json.dump(content, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temporary_name = handle.name
        os.replace(temporary_name, path)
    except OSError as exc:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)
        raise ThesisError(f"Gagal menyimpan {path}: {exc}") from exc


def read_text(path: Path) -> str:
    """Membaca UTF-8 dengan penanganan kesalahan eksplisit."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ThesisError(f"Gagal membaca {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    """Menghitung hash SHA-256 tanpa memuat seluruh file ke memori."""
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ThesisError(f"Tidak dapat menghitung hash {path}: {exc}") from exc
    return digest.hexdigest()


def next_id(items: list[dict[str, Any]], prefix: str) -> str:
    """Menghasilkan ID monoton di registry tanpa menggunakan nilai acak."""
    numbers = [int(str(item.get("id", "")).split("-")[-1]) for item in items
               if str(item.get("id", "")).startswith(prefix + "-")
               and str(item.get("id", "")).split("-")[-1].isdigit()]
    return f"{prefix}-{max(numbers, default=0)+1:03d}"


def import_attachment(workspace: Path, source: Path, category: str, item_id: str) -> tuple[str, str]:
    """Menyalin bukti ke folder workspace yang dikelola, lalu mengembalikan (lokasi, hash)."""
    if not source.is_file():
        raise ThesisError(f"Bukti tidak ditemukan: {source}")
    if source.is_symlink():
        raise ThesisError("Symlink tidak diterima sebagai bukti untuk menghindari ambiguitas target.")
    target_dir = workspace / "attachments" / category / item_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    relative = target.relative_to(workspace).as_posix()
    return relative, sha256_file(target)


def local_attachment(workspace: Path, relative_path: str) -> Path:
    """Memvalidasi bahwa path registry menunjuk file di dalam workspace, tanpa traversal."""
    candidate = (workspace / relative_path).resolve()
    root = workspace.resolve()
    if not candidate.is_relative_to(root):
        raise ThesisError(f"Path melewati batas workspace: {relative_path}")
    return candidate


def append_decision(workspace: Path, note: str, actor: str) -> None:
    """Menambahkan keputusan penelitian ke log JSON Lines (tanpa mengubah log sebelumnya)."""
    log_path = workspace / "logs" / "decisions.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": timestamp(), "actor": actor, "decision": note}, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise ThesisError(f"Gagal mencatat keputusan: {exc}") from exc
