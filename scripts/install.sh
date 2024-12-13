pdm_version="2.16.1"

echo "[*] Installing build tool - pdm..."
pip install pdm==$pdm_version -q
echo "[✔] Installing build tool: done. "
echo "[*] Building and installing package..."
pdm install -q
# Also may via pip
# pip install -r requirements.txt
echo "[✔] Building and installing package: done."
