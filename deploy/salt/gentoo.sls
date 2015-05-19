include:
  - shitstreamer

packages:
  pkg.installed:
    - pkgs:
      - app-portage/gentoolkit
      - app-misc/tmux
      - app-misc/toilet
      - app-editors/vim
      - media-video/ffmpeg
      - net-misc/youtube-dl

portage-env:
  file.managed:
    - name: /etc/portage/env/rtmp
    - content: NGINX_ADD_MDULES=/usr/src/nginx-rtmp-module/
    - makedirs: True

package-env:
  file.blockreplace:
    - name: /etc/portage/package.env
    - content: www-servers/nginx rtmp
    - append_if_not_found: True

nginx-install-pkg:
  pkg.installed:
    - name: www-servers/nginx
    - require:
      - git: nginx-rtmp-module-src
      - file: portage-env
      - file: package-env

nginx-site:
  file.managed:
    - name: /etc/nginx/shitstream.conf
    - source: salt://config/nginx-shitstream

# TODO: dis be broke
nginx-site-cfg:
  file.blockreplace:
    - name: /etc/nginx/nginx.conf
    - content: include shitstream.conf;
    - append_if_not_found: True
    - require:
      - file: nginx-site
