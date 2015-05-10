shitstream.tv
=============

* Install vagrant:
```
https://www.vagrantup.com/downloads.html
```

* Setup the vagrant VM:
```
cd deploy; vagrant up
```

* Deploy over and over until it actually works
```
vagrant ssh
salt-call --local state.highstate
salt-call --local state.highstate
salt-call --local state.highstate
salt-call --local state.highstate
```

* Stream shit
```
http://localhost:8080
```
