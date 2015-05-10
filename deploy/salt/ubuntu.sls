shitstreamer-pkgs:
  pkg.installed:
    - pkgs:
      - dpkg-dev
      - tmux
      - toilet
      - vim-nox

nginx-src:
  cmd.run:
    - name: apt-get source nginx=1.4.6
    - creates: /usr/src/nginx-1.4.6/
    - cwd: /usr/src/

nginx-rtmp-module-src:
  git.latest:
    - name: https://github.com/arut/nginx-rtmp-module.git
    - rev: master
    - target: /usr/src/nginx-rtmp-module/

nginx-debian-rules:
  file.blockreplace:
    - name: /usr/src/nginx-1.4.6/debian/rules
    - marker_start: '--add-module=$(MODULESDIR)/ngx_http_substitutions_filter_module \'
    - content: '            --add-module=/usr/src/nginx-rtmp-module/ \'
    - marker_end: '>$@'

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

nginx-install-pkg:
  pkg.installed:
    - sources:
      - nginx-common: /usr/src/nginx-common_1.4.6-1ubuntu3.2_all.deb
      - nginx-full: /usr/src/nginx-full_1.4.6-1ubuntu3.2_amd64.deb

motd:
  file.managed:
    - name: /etc/update-motd.d/zz-shitstream.tv
    - user: root
    - mode: 775
    - source: salt://config/motd.txt
