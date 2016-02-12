from enum import Enum
# tricky: need to divide value spaces into enums, but they are not consistently prefixed?
# need to partition the longest first match
# xl goes last... dt, xlHpc, ht

{% for prefix, constants in defines.items() %}
class {{prefix}}(Enum):
    {%- for key, value in constants %}
    {{key|identifier}} = {{value}}
    {%- endfor %}
{% endfor %}

__all__ = [ {% for prefix in defines.keys() %}'{{prefix}}'{% endfor %} ]