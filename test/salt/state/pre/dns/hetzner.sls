{%- set release_string = salt['pillar.get']('_release_str') %}
{%- set hetzner_token = salt['environ.get']('HETZNER_TOKEN') %}
{%- set dns_zone_id = salt['http.query'](
    'https://dns.hetzner.com/api/v1/zones',
    header_dict={'Auth-API-Token': hetzner_token},
  )['body'] | load_json | json_query('zones[?name==`gn98.de`].id') | first
%}

{%- if dns_zone_id is not none %}

  {%- set recordID = salt['http.query'](
      'https://dns.hetzner.com/api/v1/records?zone_id=' ~ dns_zone_id,
      header_dict={'Auth-API-Token': hetzner_token}
    )['body'] | load_json | json_query('records[?name==`acmesh' ~ release_string ~ '`].id') | first | default(none)
  %}

  {%- set data = {
      "zone_id": dns_zone_id,
      "type": "CNAME",
      "name": 'acmesh' ~ release_string ~ '',
      "value": "gnaumann.de"
    }
  %}

  {%- if recordID is none %}

hetzner_dns_set_record_{{ release_string }}:
  http.query:
    - name: https://dns.hetzner.com/api/v1/records
    - method: POST
    - header_dict:
        Auth-API-Token: {{ hetzner_token }}
        Content-Type: application/json
    - status: 200
    - data: '{{ data | json | string }}'

    {%- endif %}

{%- else %}

hetzner_dns_no_zone_error:
  test.fail_without_changes:
    - name: No zone found for gn98.de
    - failhard: true

{%- endif %}

