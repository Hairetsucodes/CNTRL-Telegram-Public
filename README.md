



# INSTALL GUIDE
1. Make sure /venv exists in the root directory: `python3.10 -m venv venv`
2. Activate venv: `source venv/bin/activate`
3. Install pip packages: `pip install -r requirements.txt`
4. Make .env file and update accordingly: `cp .env.example .env`
5. Install supervisord: `sudo apt-get install supervisor`
6. Make sure supervisord is running: `sudo service supervisor status`
7. Make sure supervisord is enabled on system startup: `sudo systemctl enable supervisor`
8. Copy server supervisord config file to supervisord config path: `sudo cp supervisor/conf.d/tele-me.conf /etc/supervisor/conf.d/tele-me.conf`
9. Restart supervisord: `sudo service supervisor restart`

##Development

```bash
# Run the application
python main.py
```

## Production

```bash
# Prepare supervisor configuration for persistent process
sudo cp supervisor/conf/supervisor.conf /etc/supervisor/conf.d/tele-me.conf

```