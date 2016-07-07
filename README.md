shitstream.tv
=============

Quickstart
----------
* Install vagrant.
```
https://www.vagrantup.com/downloads.html
```

* Install virtualbox.
```
https://www.virtualbox.org/wiki/Downloads
```

* Setup the vagrant VM.
```
cd deploy; vagrant up
```
or
```
cd deploy; VAGRANT_LOG=info vagrant up
```
for debugging

* Watch shit stream.
```
http://localhost:8080
```

Development
-----------
If you want to run the server manually rather than through gunicorn:
```
sudo service gunicorn stop
cd /var/www/shitstream/project/site/; /var/www/shitstream/bin/python manage.py runserver
```

Logs:
* /var/log/gunicorn.log
* /var/log/upstart/veejay.log
* /var/log/upstart/producer.log
* /var/log/nginx/error.log
