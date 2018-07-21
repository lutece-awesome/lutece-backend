# Lutece-Online-Judge
[![Python](https://img.shields.io/badge/python-3.5.4-red.svg?style=flat-square)](https://www.python.org/downloads/release/python-354/)
[![Django](https://img.shields.io/badge/django-2.0.4-ff69b4.svg?style=flat-square)](https://www.djangoproject.com/)

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

+ Install redis
<pre>
    sudo apt-get update
    sudo apt-get install redis-server
</pre>

+ Run redis
<pre>
    sudo service redis-server start
</pre>