{% set user = 'vagrant' %}

database:
  postgres_database:
    - name: shitstream
    - present
    - require:
      - pkg: packages

postgres-user:
  postgres_user.present:
    - name: {{ user }}
    - password: password
    - superuser: True

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
    - unless: test -d /usr/src/nginx-rtmp-module/

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

/etc/init/gunicorn.conf:
  file.managed:
    - source: salt://config/gunicorn.conf

gunicorn:
  service:
    - running
    - require:
      - pkg: packages
      - file: /etc/init/gunicorn.conf

/etc/init/producer.conf:
  file.managed:
    - source: salt://config/producer.conf

producer:
  service:
    - running
    - require:
      - pkg: packages
      - file: /etc/init/producer.conf

/etc/init/veejay.conf:
  file.managed:
    - source: salt://config/veejay.conf

veejay:
  service:
    - running
    - require:
      - pkg: packages
      - file: /etc/init/veejay.conf

github.com:
  ssh_known_hosts:
    - present
    - fingerprint: 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48

git-shitstream:
  git.latest:
    - name: git@github.com:nijotz/shitstream.tv.git
    - target: /var/www/shitstream/project
    - rev: master
    - unless: test -d /var/www/shitstream/
    - require:
      - pkg: packages
      - ssh_known_hosts: github.com
      - file: /etc/sudoers.d/ssh-agent
      - file: /var/www/shitstream

/etc/sudoers.d/ssh-agent:
  file.managed:
    - source: salt://config/sudo-ssh-agent
    - mode: 440

python-pkgs:
  pip.installed:
    - names:
      - virtualenv
      - requests >= 1.0.0
    - require:
      - pkg: packages

/var/www/shitstream:
  file.directory:
    - makedirs: True
  virtualenv.managed:
    - system_site_packages: False
    - requirements: /var/www/shitstream/project/requirements.txt
    - require:
      - git: git-shitstream
      - pip: python-pkgs
