include:
  - shitstreamer

packages:
  pkg.installed:
    - pkgs:
      - dpkg-dev
      - git
      - libpq-dev
      - postgresql
      - python-dev
      - python-pip
      - tmux
      - toilet
      - uwsgi-plugin-python
      - vim-nox

nginx-src:
  cmd.run:
    - name: apt-get source nginx=1.4.6
    - creates: /usr/src/nginx-1.4.6/
    - cwd: /usr/src/

nginx-debian-rules:
  file.blockreplace:
    - name: /usr/src/nginx-1.4.6/debian/rules
    - marker_start: '--add-module=$(MODULESDIR)/ngx_http_substitutions_filter_module \'
    - content: '            --add-module=/usr/src/nginx-rtmp-module/ \'
    - marker_end: '>$@'
    - require:
      - cmd: nginx-src

nginx-build-dep:
  cmd.run:
    - name: apt-get -y build-dep nginx && touch /root/builddeps
    - creates: /root/builddeps

nginx-build-pkg:
  cmd.run:
    - name: dpkg-buildpackage -b
    - cwd: /usr/src/nginx-1.4.6/
    - output_loglevel: info
    - creates: /usr/src/nginx-full_1.4.6-1ubuntu3.2_amd64.deb
    - require:
      - git: nginx-rtmp-module-src
      - cmd: nginx-src
      - file: nginx-debian-rules
      - cmd: nginx-build-dep

nginx-install-pkg:
  pkg.installed:
    - sources:
      - nginx-common: /usr/src/nginx-common_1.4.6-1ubuntu3.2_all.deb
      - nginx-full: /usr/src/nginx-full_1.4.6-1ubuntu3.2_amd64.deb
    - require:
      - cmd: nginx-build-pkg

nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/shitstream
    - source: salt://config/nginx-shitstream
