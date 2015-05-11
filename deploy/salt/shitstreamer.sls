nginx-cfg:
  file.blockreplace:
    - name: /etc/nginx/nginx.conf
    - marker_start: '# RTMP config -- start'
    - marker_end: '# RTMP config -- end'
    - content: |
            rtmp {
                    server {
                            listen 1935;
                            chunk_size 4000;
                            application stream { live on; }
                    }
            }
    - append_if_not_found: True
    - require:
      - pkg: nginx-install-pkg

nginx-rtmp-module-src:
  git.latest:
    - name: https://github.com/arut/nginx-rtmp-module.git
    - rev: master
    - target: /usr/src/nginx-rtmp-module/

rtmp-stats:
  file.copy:
    - name: /var/www/stat.xsl
    - source: /usr/src/nginx-rtmp-module/stat.xsl
    - makedirs: True

nginx-service:
  service.running:
    - name: nginx
    - watch:
      - file: nginx-cfg
      - file: nginx-site
