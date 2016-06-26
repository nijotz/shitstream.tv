DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql:///shitstream?user={{ salt['pillar.get']('user') }}"
HOST = '0.0.0.0'
PORT = 5000
MOVIE_DIR = '/var/www/shitstream/project/site/mp4s'
