# notebooklm-py 命令参考

基于 [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) 项目。运行 `notebooklm --help` 查看完整选项。

## Session

| Command | Description |
|---------|-------------|
| `notebooklm login` | Login via browser |
| `notebooklm status` | Show current context |
| `notebooklm list` | List notebooks |
| `notebooklm use <id>` | Set current notebook |

## Notebook

| Command | Description |
|---------|-------------|
| `notebooklm create "title"` | Create notebook |
| `notebooklm delete <id>` | Delete notebook |
| `notebooklm rename "title"` | Rename current |

## Sources

| Command | Description |
|---------|-------------|
| `notebooklm source add "file.pdf"` | Add file |
| `notebooklm source list` | List sources |
| `notebooklm source wait <id>` | Wait for processing |

## Chat

| Command | Description |
|---------|-------------|
| `notebooklm ask "question"` | Ask question |
| `notebooklm history` | View history |

## Generate

| Command | Description |
|---------|-------------|
| `notebooklm generate audio` | Podcast |
| `notebooklm generate slide-deck` | Slides |
| `notebooklm generate video` | Video |
| `notebooklm generate infographic` | Infographic |
| `notebooklm generate quiz` | Quiz |
| `notebooklm generate mind-map` | Mind map |

## Tips

- Use `--json` for machine-readable output
- Use `--help` on any command for details
- Auth stored in `~/.notebooklm/storage_state.json`
