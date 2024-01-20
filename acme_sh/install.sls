{%- from 'acme_sh/map.jinja' import acme_sh with context %}

{%- for user, config in acme_sh.items() %}
acme_sh_install_{{ user }}:
  acme_sh.installed:
    - email: {{ config['email'] }}
    - user: {{ user }}
  {%- if config.get('upgrade') %}
    - upgrade: {{ config['upgrade'] }}
  {%- endif %}
  {%- if config.get('force') %}
    - force: {{ config['force'] }}
  {%- endif %}
{%- endfor %}
