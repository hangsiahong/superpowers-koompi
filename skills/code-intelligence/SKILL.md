---
name: code-intelligence
description: Use when working on large, multi-service codebases where semantic search and global project context are needed to find relevant code or explain architecture.
---

# Code Intelligence (LanceDB)

## Overview
A semantic search and retrieval system powered by LanceDB and KConsole Gemini Embeddings. It allows you to search your codebase by "meaning" rather than just keywords.

## When to Use
- You need to find code but don't know the exact filenames or variable names.
- Working across multiple microservices where dependencies are unclear.
- "Remembering" architecture patterns from different parts of the project.

## Usage

### 1. Index your Project
Run this in a background tmux pane to build the initial memory:
\`\`\`bash
python scripts/indexer.py --index ./your-project
\`\`\`

### 2. Semantic Search
Ask for a concept, not a keyword:
\`\`\`bash
python scripts/indexer.py --search "How is the user authentication handled?"
\`\`\`

## Best Practices
- **Exclude noise**: The indexer automatically ignores hidden files and common build artifacts.
- **Refresh**: Re-index after major refactors or adding new services.
- **Combined with tmux**: Keep a "Monitor" pane open to run the indexer in the background.

## Implementation
The system uses \`text-embedding-004\` via KConsole AI Gateway and stores vectors in a local LanceDB instance (\`.lancedb\`).
