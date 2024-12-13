# Restoring repository to default:
echo "[*] Restoring local repo..."
git restore .
if [ $? -eq 0 ]; then
    echo "[✔] Restoring local repo: Done!"
else
    echo "[✘] Restoring local repo: Error. Try manual."
fi

# Updating repository:
echo "[*] Updating local repo..."
git pull
if [ $? -eq 0 ]; then
    echo "[✔] Updating local repo: Done!"
else
    echo "[✘] Updating local repo: Error. Try manual."
fi
