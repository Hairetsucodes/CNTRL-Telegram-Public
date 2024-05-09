cd home/azureuser/TeleMe
git pull origin main

# Activate virtual environment and install requirements
source venv/bin/activate
pip install -r requirements.txt

# Update supervisor configuration and restart the process
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart tele-me
