<!--<h1>'{{ config.site_name }}'</h1>-->
{{ config.extra.added_key }}
<p>
<img src="_images/Percona_Color_Dark.svg" alt="Percona logo" />
</p>
<h1>Server for MongoDB {{ config.plugins.macros.variables.release }}</h1>
{% if config.site_description %}
<h1>{{ config.site_description }}</h1>
{% endif %} 
<h2>{{ config.plugins.macros.variables.release }} ({{ config.plugins.macros.variables.date['8_3_13'] }})</h2>
<br>
<br>