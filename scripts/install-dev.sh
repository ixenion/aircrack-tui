# Install package with additional python libs to run autotests.

pdm_version="2.16.1"

echo "[*] Installing build tool - pdm..."
pip install pdm==$pdm_version -q

echo "[✔] Installing build tool: done. "
echo "[*] Building and installing package (dev mode)..."
pdm install -d -q
# Also may via pip
# pip install -r requirements-dev.txt
echo "[✔] Building and installing package (dev mode): done."
