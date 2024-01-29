---
docker:
  wanted:
    - docker
    - compose
  pkg:
    {%- if grains['os'] == 'Rocky' %}
    deps:
      - python3-pip
      - git
      - tar
      - python3-dnf-plugin-versionlock
    {%- elif grains['os'] == "SUSE" %}
    deps:
      - python3-pip
      - python3-docker
      - git
      - tar
    {%- endif %}
    docker:
      use_upstream: repo
    compose:
      use_upstream: binary

  compose:
    applications:
      - pebble
    pebble:
      path: /opt/pebble/docker-compose.yml
