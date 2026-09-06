#!/bin/sh
# PostToolUse-hook: koerer tests efter hver Edit eller Write.
# Exit 2 sender stderr tilbage til agenten. Vaerktoejet er allerede koert, saa det blokerer ikke (se hooks-reference).
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
if python3 -m pytest -q --no-header -p no:cacheprovider >/tmp/fragtvaegt-hook.log 2>&1; then
  exit 0
fi
echo "Tests fejler efter din aendring. Ret det, foer du gaar videre:" >&2
tail -15 /tmp/fragtvaegt-hook.log >&2
exit 2
