# Flasko

A simple Flask application setup guide within a Python Anaconda environment. I created a WSGI entry point so that any WSGI-capable application server can interface with it, and then configured the Gunicorn app server to provide this function. Afterward, I created a systemd unit file to automatically launch the application server on boot. I created a Nginx server block that passes web client traffic to the application server, relaying external requests.

### SSH

Go to your machine
```
ssh paperspace@172.83.8.197
```
Set up [password-less](https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login) SSH login

```
ssh-copy-id paperspace@172.83.8.197
```
Save host to config
```
nano .ssh/config
```
```
Host servo
     HostName 172.83.8.197
     IdentityFile ~/.ssh/id_rsa
     User paperspace
     LocalForward 8888 localhost:8888
```

### Update 
Ubuntu updated
  
```
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### Anaconda


Install Anaconda
https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-18-04

Update Anaconda
```
conda update conda
conda update anaconda
```

### Packages

Test default python version
```
python -V
```
Create Anaconda Environment
```
conda create -n fastai python=3.x.x
conda activate fastai
```

Install [Fastai](https://github.com/fastai/fastai)
```
conda install -c pytorch -c fastai fastai
```
Restart and test fastai
```
sudo reboot
conda activate fastai
conda list | grep fastai
python
```
```
from fastai.basics import *
torch.ones(2,2)
```
```
conda deactivate
conda create --name flasko --clone fastai
```

### Server
Mostly:
https://linoxide.com/linux-how-to/install-flask-python-ubuntu/

But that might help aswell:
https://peteris.rocks/blog/deploy-flask-apps-using-anaconda-on-ubuntu-server/
```
nano /etc/systemd/system/flaskproject.service
```
```
[Unit]
Description=Gunicorn instance to serve flaskproject
After=network.target

[Service]
User=paperspace
Group=www-data
WorkingDirectory=/home/paperspace/flaskproject
ExecStart=/home/paperspace/anaconda3/envs/flasko/bin/gunicorn --workers 3 --bind unix:flaskproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```


#### Links
[Gunicorn](https://gunicorn.org/) config [file](https://stackoverflow.com/questions/12063463/where-is-the-gunicorn-config-file)  
[Nginx](https://www.nginx.com/) log [file](https://stackoverflow.com/questions/1706111/where-can-i-find-the-error-logs-of-nginx-using-fastcgi-and-django)  
Setting [timezone](https://askubuntu.com/questions/323131/setting-timezone-from-terminal) from terminal  
WSGI [tutorial](http://wsgi.tutorial.codepoint.net/)  
Nginx [timeout](https://asdqwe.net/blog/solutions-504-gateway-timeout-nginx/)  
Server [172.83.8.197](http://172.83.8.197/)  
