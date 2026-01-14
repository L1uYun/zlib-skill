---
name: zlib
description: Use when user asks to download books from Z-Library, search Z-Library via Telegram bot, convert ebooks to PDF, or upload books to NotebookLM for analysis. Triggers on "download book", "zlib", "Z-Library", "get ebook", "upload to NotebookLM".
---

# Z-Library + NotebookLM Skill

Download books via Z-Library Telegram bot → Convert to PDF → Upload to NotebookLM for Q&A and content generation.

## Safety

Require explicit user confirmation for authorized personal use. Refuse mass downloading or credential abuse.

## Quick Reference

| Step | Command |
|------|---------|
| Download | `.venv/Scripts/python.exe scripts/zlib_client.py --title "书名"` |
| Convert | `.venv/Scripts/python.exe scripts/calibre_convert.py downloads/book.epub` |
| Create notebook | `.venv/Scripts/notebooklm.exe create "title"` |
| Upload PDF | `.venv/Scripts/notebooklm.exe source add "file.pdf"` |
| Ask | `.venv/Scripts/notebooklm.exe ask "question"` |
| Generate audio | `.venv/Scripts/notebooklm.exe generate audio` |

## Workflow

### 1. Download Book

```bash
.venv/Scripts/python.exe scripts/zlib_client.py --title "书名"
# With selection: --index 1
```

Downloads to `downloads/` directory.

### 2. Convert to PDF (if needed)

```bash
.venv/Scripts/python.exe scripts/calibre_convert.py downloads/book.epub
```

Requires Calibre installed on system.

### 3. Upload to NotebookLM

```bash
.venv/Scripts/notebooklm.exe create "Book Title"
.venv/Scripts/notebooklm.exe use <notebook-id>
.venv/Scripts/notebooklm.exe source add "downloads/book.pdf"
```

### 4. Use NotebookLM

```bash
.venv/Scripts/notebooklm.exe ask "What are the key points?"
.venv/Scripts/notebooklm.exe generate audio  # podcast
.venv/Scripts/notebooklm.exe generate slide-deck
```

## First-Time Setup

See [references/initialization.md](references/initialization.md) for complete setup guide.

**Quick check:**
- `.env` file with Telegram credentials
- `zlib.session` file (Telegram login)
- `~/.notebooklm/storage_state.json` (NotebookLM login)

## References

- **[initialization.md](references/initialization.md)** - First-time setup guide
- **[notebooklm-cli.md](references/notebooklm-cli.md)** - Full CLI reference

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/zlib_client.py` | Telegram bot interaction |
| `scripts/calibre_convert.py` | PDF conversion |
| `scripts/auth_step*.py` | Telegram authentication |

## Requirements

- Python 3.10+
- Telegram account with Z-Library bot access
- Calibre (for ebook conversion)
- Google account (for NotebookLM)
