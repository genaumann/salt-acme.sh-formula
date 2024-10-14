---
{%- set os = grains['os'] | lower %}
{%- set osrelease = grains['osrelease'] | regex_replace('(\.)', '') | lower %}
{%- set saltrelease = grains['saltversion'] | regex_replace('(\.)', '') %}
{%- set release_str = os + osrelease + saltrelease %}
_release_str: {{ release_str }}
acme_sh:
  vagrant:
    email: ghtest@gn98.de
    certs:
      {{ 'acmesh' ~ release_str ~ '.gn98.de' }}:
        acme_mode: dns
        dns_plugin: dns_hetzner
        keysize: '4096'
        server: letsencrypt_test
        cert_path: /home/vagrant/crt
        retry:
          attempts: 3
      standalone.gn98.de:
        acme_mode: standalone
        server: https://localhost:14000/dir
        keysize: '2048'
        cert_path: /home/vagrant/crt
        insecure: true
        http_port: '5002'
        aliases:
          - www.standalone.gn98.de
      alpn.gn98.de:
        acme_mode: standalone-tls-alpn
        http_port: '5001'
        server: https://localhost:14000/dir
        cert_path: /home/vagrant/crt
        insecure: true
