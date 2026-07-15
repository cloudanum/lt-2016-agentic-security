#!/bin/bash
# Launches a local Jupyter Lab for the Agentic Security course (no login prompt).
# Foolproof: safe to press repeatedly. Never starts a second session.
# Uses port 8889 so it does not collide with any other Jupyter on 8888.

PORT=8889
COURSE_DIR="/home/student/agentic-security"
OPEN_URL="http://localhost:${PORT}/lab/tree/code"
LOG="${COURSE_DIR}/.jupyter-lab.log"
LOCK="${COURSE_DIR}/.jupyter-lab.lock"
JUPYTER="/home/student/anaconda3/bin/jupyter"

is_up() {
  curl -s -o /dev/null --max-time 2 "http://localhost:${PORT}/api"
}

# Serialize concurrent launches (e.g. fast double-clicks): only one
# instance runs this block at a time, the rest wait then see it's up.
exec 9>"$LOCK"
flock 9

if ! is_up; then
  nohup "$JUPYTER" lab \
    --no-browser \
    --port="$PORT" \
    --notebook-dir="$COURSE_DIR" \
    --ServerApp.token='' \
    --ServerApp.password='' \
    --ServerApp.disable_check_xsrf=True \
    >"$LOG" 2>&1 &

  for _ in $(seq 1 40); do
    is_up && break
    sleep 0.5
  done
fi

flock -u 9

if is_up; then
  xdg-open "$OPEN_URL"
else
  command -v zenity >/dev/null \
    && zenity --error --text="Jupyter Lab failed to start. See ${LOG}" \
    || notify-send "Jupyter Lab failed to start" "See ${LOG}" 2>/dev/null \
    || echo "Jupyter Lab failed to start. See ${LOG}"
fi
