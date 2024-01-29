{%- set release_string = salt['pillar.get']('_release_str') %}
{%- set hetzner_token = salt['environ.get']('HETZNER_TOKEN') %}

{%- do salt['environ.setenv'](
  {'ACMESH_vagrant_acmesh' ~ release_string ~ 'Gn98De_HETZNER_Token': hetzner_token}
)
%}
