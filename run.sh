#!/usr/bin/env bash
set -euo pipefail

exec > >(tee -a run.log) 2>&1

# ---- Load user environment
[ -f ~/.profile ] && source ~/.profile
[ -f ~/.bashrc ] && source ~/.bashrc

# ---- Add custom binary path
export PATH="$PATH:$HOME/EMs/EMsoftBuild/Release/Bin"

cd "$(dirname "$0")"

# ---- System dependencies
DEPS=(
  python3
  python3-pip
  libxkbcommon-x11-0
  libxcb-xinerama0
  libxcb-cursor0
  qtwayland5
  intel-opencl-icd
  ocl-icd-libopencl1
)

echo "=== Checking for system dependencies ==="
missing=()
for pkg in "${DEPS[@]}"; do
  if dpkg -s "$pkg" >/dev/null 2>&1; then
    echo "OK  - $pkg already installed"
  else
    echo "Missing - $pkg"
    missing+=("$pkg")
  fi
done

if [ ${#missing[@]} -gt 0 ]; then
  echo "Installing: ${missing[*]}"
  sudo apt-get update -y
  sudo apt-get install -y "${missing[@]}"
else
  echo "=== All dependencies satisfied ==="
fi

# ---- Create virtual environment if it does not exist
if [ ! -x ".venv/bin/python" ]; then
  echo "[INFO] Creating virtual env at .venv ..."
  python3 -m venv .venv
fi

# ---- Activate virtual environment
# shellcheck disable=SC1091
source .venv/bin/activate

# ---- Ensure pip/setuptools/wheel up to date
python3 -m pip install --upgrade pip setuptools wheel

# ---- Install dependencies if requirements.txt has changed
if [ -f "requirements.txt" ]; then
  NEED_INSTALL=1
  HASH_FILE=".venv/.requirements.sha256"

  if command -v sha256sum >/dev/null 2>&1; then
    CURR_HASH="$(sha256sum requirements.txt | awk '{print $1}')"
    if [ -f "$HASH_FILE" ] && [ "$(cat "$HASH_FILE")" = "$CURR_HASH" ]; then
      NEED_INSTALL=0
    fi
  fi

  if [ "$NEED_INSTALL" -eq 1 ]; then
    echo "[INFO] Installing dependencies from requirements.txt ..."
    python3 -m pip install -r requirements.txt
    [ -n "${CURR_HASH-}" ] && echo "$CURR_HASH" > "$HASH_FILE"
  else
    echo "[INFO] No changes in requirements.txt"
  fi
else
  echo "[WARN] requirements.txt not found"
fi

exec python3 src/emsoft_gui/gui_main.py "$@"
