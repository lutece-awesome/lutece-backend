# Lutece-Online-Judge
[![Python](https://img.shields.io/badge/python-3.7.0-red.svg?style=flat-square)](https://www.python.org/downloads/release/python-370/)
[![Django](https://img.shields.io/badge/django-2.1.5-ff69b4.svg?style=flat-square)](https://www.djangoproject.com/)
[![Build Status](https://travis-ci.com/lutece-awesome/lutece-backend.svg?branch=master)](https://travis-ci.com/lutece-awesome/lutece-backend)

Simplicity online judge

## Installation

+ Install requirements
<pre>
    pip3 install -r requirements/requirements.txt
</pre>

+ Create configurion file
<pre>
    cp Lutece/config.py.tempalte Lutece/config.py
</pre>

+ Install rabbitmq-server
### Debian:
<pre>
    sudo apt-get update
    sudo apt-get install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
</pre>

### Arch:
<pre>
    sudo pacman -S rabbitmq
    sudo systemctl enable rabbitmq
    sudo systemctl start rabbitmq
</pre>

+ Set task user
<pre>
    # <strong>You need to set Judger AUTH_KEY</strong>
    $ sudo rabbitmqctl add_user task_user AUTH_KEY
    $ sudo rabbitmqctl set_user_tags task_user normal
    $ sudo rabbitmqctl add_vhost judger_host
    $ sudo rabbitmqctl set_permissions -p judger_host task_user ".*" ".*" ".*"
</pre>


+ Install redis for websocket backend
### Debian:
<pre>
    $ sudo apt-get update
    $ sudo apt-get install redis-server
    $ sudo systemctl enable redis-server
    $ sudo systemctl start redis-server
</pre>

### Arch:
<pre>
    $ sudo pacman -S redis
    $ sudo systemctl enable redis
    $ sudo systemctl start redis
</pre>

### Set running mode
open the <b>.bash_profile</b> file and append the following:

```
    # Lutece settings, can be 'dev' or 'prod' or 'travis', default is dev
    export lutece_runtime_mode=dev
```

Then source the terminal to make the change work:
<pre>
    $ source ~/.bash_profile
</pre>

### Create data folder
<pre>
    mkdir ~/lutece_data
</pre>