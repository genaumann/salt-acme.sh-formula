{%- set pkgs = ['socat'] %}

pkg_pre-install:
  pkg.installed:
    - pkgs: {{ pkgs }}

pkg_install_docker_pip:
  pip.installed:
    - name: docker <= 6.1.3 # see https://github.com/geerlingguy/internet-pi/issues/567
    - reload_modules: True

pkg_install_docker-compose_pip:
  pip.installed:
    - name: docker-compose
    - extra_args:
      - --no-build-isolation # see https://stackoverflow.com/questions/76708329/docker-compose-no-longer-building-image-attributeerror-cython-sources
    - reload_modules: True
