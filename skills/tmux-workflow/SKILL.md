---
name: tmux-workflow
description: Use when running multiple parallel agents, monitoring long-running background tasks, or requiring a multi-pane observability dashboard for parallel implementation plans.
---

# tmux Workflow

## Overview
A tmux-based Command Center for managing parallel agent execution and background observability.

## When to Use
- Implementing plans with 2+ parallel sub-agents (via dispatching-parallel-agents)
- Monitoring logs and tests simultaneously while coding
- Managing long-running background tasks (dev servers, scrapers)

## Core Pattern: The Command Center
- **Pane 0 (Main)**: Orchestrator / Brainstorming
- **Pane 1 (Monitor)**: Logs / Live Output
- **Pane 2+ (Workers)**: Parallel sub-agent execution contexts

## Usage

### 1. Initialize Dashboard
```bash
bash scripts/tmux-manager.sh init "ProjectName"
```

### 2. Add Worker Pane
```bash
bash scripts/tmux-manager.sh add-worker "Worker Name"
```

### 3. Split for Monitoring
```bash
bash scripts/tmux-manager.sh split-log "tail -f dev.log"
```

## Implementation Details
The `tmux-manager.sh` script handles session naming, pane splitting, and layout optimization (usually tiled or main-vertical).
