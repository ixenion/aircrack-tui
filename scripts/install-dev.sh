# Install package with additional python libs to run autotests.

echo "[*] Installing build tool - pdm..."
pip install pdm -q
echo "[✔] Installing build tool: done. "
echo "[*] Building and installing package (dev mode)..."
pdm install -d -q
# Also may via pip
# pip install -r requirements-dev.txt
echo "[✔] Building and installing package (dev mode): done."
