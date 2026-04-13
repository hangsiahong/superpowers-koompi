# Elite Superpowers (Koompi Edition)

This is a customized version of the [Superpowers](https://github.com/obra/superpowers) skill set, optimized for the **KConsole AI Gateway** and **Koompi** development workflow.

## 🚀 Key Features

- **Integrated tmux Workflow**: Automatically manage parallel agent panes and observability monitors.
- **Code Intelligence (LanceDB)**: Semantic search and "Project Memory" using Gemini Embeddings via KConsole.
- **Model Hot-Swapping**: Optimized to use GLM-5.1 for planning and Gemini-3-Flash for execution.
- **Isolated Workspace Support**: Native integration with Git Worktrees.

## 🛠️ Custom Skills

### 1. tmux-workflow
Manage your terminal workspace for parallel implementation.
- `bash scripts/tmux-manager.sh init "Project"`

### 2. code-intelligence
Semantic search across your entire codebase.
- `python scripts/indexer.py --index .`
- `python scripts/indexer.py --search "query"`

## 📦 Installation

1. Clone to your codex directory:
   ```bash
   git clone https://github.com/hangsiahong/superpowers-koompi.git ~/.codex/superpowers
   ```

2. Symlink to your skills:
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/superpowers/skills ~/.agents/skills/superpowers
   ```

3. Install dependencies:
   ```bash
   pip install lancedb pandas pyarrow requests
   ```

## 🧠 The Workflow

Refer to `~/.codex/AGENTS.md` for the full Elite operating procedure.
