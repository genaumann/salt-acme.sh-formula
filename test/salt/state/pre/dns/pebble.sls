{%- set dns = ['standalone.gn98.de', 'www.standalone.gn98.de', 'alpn.gn98.de'] %}

pebble_sleep:
  module.run:
    - test.sleep:
      - 15

{%- for entry in dns %}
  {%- set data = {"host": entry, "addresses": [grains['ipv4'][0]]} %}
pebble_set_dns_{{ entry }}:
  http.query:
    - name: http://localhost:8055/add-a
    - method: POST
    - data: '{{ data | json | string }}'
    - header_dict:
        Content-Type: application/json
    - status: 200
    - require:
      - module: pebble_sleep
  host.present:
    - name: {{ entry }}
    - ip: {{ grains['ipv4'][0] }}
{%- endfor %}
