shitstream.tv
=============

Quickstart
----------
* Install docker.
```
https://docs.docker.com/engine/installation/
```

* Install docker-machine (if needed).
```
https://docs.docker.com/machine/install-machine/
```

* Install docker-compose
```
https://docs.docker.com/compose/install/
```

* Build and run shitstream
```
docker-compose build;docker-compose up
```

MORE TO COME

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
