{% set env = salt['grains.get']('env', default='dev') %}

base:
  '*':
    - {{ env }}
