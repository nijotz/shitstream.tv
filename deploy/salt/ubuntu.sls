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
      - vim-nox
      - autoconf
      - automake
      - build-essential
      - libass-dev
      - libfreetype6-dev
      - libgpac-dev
      - libsdl1.2-dev
      - libtheora-dev
      - libtool
      - libva-dev
      - libvdpau-dev
      - libvorbis-dev
      - libxcb1-dev
      - libxcb-shm0-dev
      - libxcb-xfixes0-dev
      - pkg-config
      - texi2html
      - zlib1g-dev
      - yasm
      - libx264-dev
      - libmp3lame-dev
      - libopus-dev

ffmpeg-src-dir:
  cmd.run:
    - name: mkdir -p ffmpeg
    - cwd: /usr/src/

ffmpeg-src:
  cmd.run:
    - name: wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2;tar xjvf ffmpeg-snapshot.tar.bz2
    - cwd: /usr/src/ffmpeg/
    - creates: /usr/src/ffmpeg/ffmpeg/
    - require:
      - cmd: ffmpeg-src-dir

ffmpeg-build:
  cmd.run:
    - name: PATH="/bin/:$PATH" PKG_CONFIG_PATH="/usr/src/ffmpeg/ffmpeg_build/lib/pkgconfig" ./configure --prefix="/usr/src/ffmpeg/ffmpeg_build" --pkg-config-flags="--static" --extra-cflags="-I/usr/src/ffmpeg/ffmpeg_build/include" --extra-ldflags="-L/usr/src/ffmpeg/ffmpeg_build/lib"  --bindir="/bin/"  --enable-gpl  --enable-libass  --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264 --enable-nonfree;PATH="/bin/:$PATH" make
    - cwd: /usr/src/ffmpeg/ffmpeg/
    - creates: /bin/ffmpeg
    - require:
      - cmd: ffmpeg-src

ffmpeg-install:
  cmd.run:
    - name: make install;make distclean;hash -r;export PATH="/usr/src/ffmpeg/bin:$PATH"
    - cwd: /usr/src/ffmpeg/ffmpeg
    - creates: /bin/ffmpeg
    - require:
      - cmd: ffmpeg-build

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
