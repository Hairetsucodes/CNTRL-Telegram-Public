



# INSTALL GUIDE 
1. Make sure /venv exists in the root directory: 
```bash
python3.10 -m venv venv
```
2. Activate venv: 
```bash
source venv/bin/activate
```
3. Install pip packages: 
```bash
pip install -r requirements.txt
```
4. Make .env file and update accordingly: 
```bash
cp .env.example .env
```


## Development

```bash
# Run the application
python main.py
```

## Production
5. Install supervisord: 
```bash 
sudo apt install supervisor
```
6. Make sure supervisord is running: 
```bash 
sudo service supervisor status
```
7. Make sure supervisord is enabled on system startup: 
```bash
sudo systemctl enable supervisor
```
8. Copy server supervisord config file to supervisord config path: 
```bash 
sudo cp supervisor/conf.d/tele-me.conf /etc/supervisor/conf.d/tele-me.conf
```
9. Restart supervisord: 
```bash 
sudo service supervisor restart
```



# TODO

- ___ Word Counter
- /tldr
-