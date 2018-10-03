# Lutece-Online-Judge
[![Python](https://img.shields.io/badge/python-3.7.0-red.svg?style=flat-square)](https://www.python.org/downloads/release/python-370/)
[![Django](https://img.shields.io/badge/django-2.1.1-ff69b4.svg?style=flat-square)](https://www.djangoproject.com/)

Simplicity online judge

## Installation

+ Install requirements
<pre>
    pip3 install -r requirements/requirements.txt
</pre>

+ Install rabbitmq-server and set task_user
<pre>
    sudo apt-get update
    sudo apt-get install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
    sudo systemctl status rabbitmq-server
    sudo rabbitmqctl add_user task_user AUTH_KEY # you need to set Judger AUTH_KEY
    sudo rabbitmqctl set_user_tags task_user normal
    sudo rabbitmqctl add_vhost judger_host
    sudo rabbitmqctl set_permissions -p judger_host task_user ".*" ".*" ".*"
</pre>

+ Install redis for websocket backend
<pre>
    sudo apt-get update
    sudo apt-get install redis-server
</pre>

## User configuring

+ <b>Any change</b> during this step need to <b>overwrite</b> into data/constant.py

+ Generate running user
```
$ sudo useradd -m lutece_running_user
$ sudo passwd lutece_running_user
```

+ Create data directory
```
# Set the data dir for data
$ mkdir ~/lutece_data
```

+ Generate ssh key for data user
```
su lutece_running_user
ssh-keygen
```