shitstream.tv
=============

* Install vagrant.
```
https://www.vagrantup.com/downloads.html
```

* Setup the vagrant VM.
```
cd deploy; vagrant up
```

* Deploy over and over until it actually works.
```
vagrant ssh
salt-call --local state.highstate
salt-call --local state.highstate
salt-call --local state.highstate
salt-call --local state.highstate
```

* Load the streamer. You'll just see a loading spinner.
```
http://localhost:8080
```

* Publish some shit.
```
ffmpeg -re -i site/mp4s/mirror.mp4 -c copy -f flv rtmp://localhost:1935/stream/live
```

* Watch shit stream.
