echo "[*] Installing build tool - pdm..."
pip install pdm -q
echo "[✔] Installing build tool: done. "
echo "[*] Building and installing package..."
pdm install -q
# Also may via pip
# pip install -r requirements.txt
echo "[✔] Building and installing package: done."
