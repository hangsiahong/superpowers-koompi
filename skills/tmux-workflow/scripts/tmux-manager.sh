#!/bin/bash

# tmux-manager.sh - Integrated Worktree & Path management

SESSION_NAME=${2:-"codex-superpowers"}
WORKTREE_PATH=$3

check_tmux() {
    if ! command -v tmux &> /dev/null; then
        echo "Error: tmux is not installed."
        exit 1
    fi
}

init_session() {
    check_tmux
    local target_dir=$WORKTREE_PATH
    
    # If no worktree path provided, try to find a matching local directory
    if [ -z "$target_dir" ]; then
        target_dir=$(readlink -f "$SESSION_NAME" 2>/dev/null)
    fi

    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "Session $SESSION_NAME already exists."
    else
        if [ -d "$target_dir" ]; then
            echo "Initializing session $SESSION_NAME in $target_dir"
            tmux new-session -d -s "$SESSION_NAME" -n "Orchestrator" -c "$target_dir"
        else
            tmux new-session -d -s "$SESSION_NAME" -n "Orchestrator"
        fi
        
        sleep 0.1
        tmux split-window -h -t "$SESSION_NAME" -c "#{pane_current_path}"
        tmux send-keys -t "$SESSION_NAME" "echo 'Observability Monitor'" C-m
        tmux select-pane -t "$SESSION_NAME:0.0"
    fi
}

add_worker() {
    local worker_name=$1
    check_tmux
    tmux split-window -v -t "$SESSION_NAME" -c "#{pane_current_path}"
    tmux send-keys -t "$SESSION_NAME" "echo 'Worker: $worker_name'" C-m
    tmux select-layout -t "$SESSION_NAME" tiled
}

case "$1" in
    init)
        init_session
        ;;
    add-worker)
        add_worker "$3"
        ;;
    *)
        echo "Usage: $0 {init|add-worker} [session_name] [optional_path]"
        exit 1
esac
