{% from 'acme_sh/map.jinja' import acme_sh with context %}

{%- for user, config in acme_sh.items() %}
  {%- if config.get('certs') is mapping %}
    {%- for domain, cert_config in config['certs'].items() %}
acme_sh_cert_{{ user }}_{{ domain }}:
  acme_sh.cert:
    - name: {{ domain }}
    - acme_mode: {{ cert_config['acme_mode'] }}
      {%- if cert_config.get('aliases') %}
    - aliases: {{ cert_config['aliases'] }}
      {%- endif %}
    - server: {{ cert_config.get('server', 'letsencrypt') }}
    - keysize: {{ cert_config.get('keysize', '4096') }}
      {%- if cert_config.get('dns_plugin') %}
    - dns_plugin: {{ cert_config['dns_plugin'] }}
      {%- endif %}
      {%- if cert_config.get('webroot') %}
    - webroot: {{ cert_config['webroot'] }}
      {%- endif %}
      {%- if cert_config.get('http_port') %}
    - http_port: {{ cert_config['http_port'] }}
      {%- endif %}
    - user: {{ user }}
      {%- if cert_config.get('cert_path') %}
    - cert_path: {{ cert_config['cert_path'] }}
      {%- endif %}
      {%- if cert_config.get('dns_credentials') %}
    - dns_credentials: {{ cert_config['dns_credentials'] }}
      {%- endif %}
    - force: {{ cert_config.get('force', False) }}
      {%- if cert_config.get('valid_to') %}
    - valid_to: {{ cert_config['valid_to'] }}
      {%- endif %}
      {%- if cert_config.get('valid_from') %}
    - valid_from: {{ cert_config['valid_from'] }}
      {%- endif %}
    {%- endfor %}
  {%- endif %}
{%- endfor %}
