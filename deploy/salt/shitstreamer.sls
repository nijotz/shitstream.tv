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

                            # video on demand for flv files
                            application vod {
                                play /var/www/site/flvs;
                            }

                            # video on demand for mp4 files
                            application vod2 {
                                play /var/www/site/mp4s;
                            }
                    }
            }
    - append_if_not_found: True

nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/shitstream
    - source: salt://config/nginx-shitstream

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
