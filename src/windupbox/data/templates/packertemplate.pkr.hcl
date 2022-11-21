{% for var in variables %}
variable "{{ var.name }}" {
  type    = {{ var.type }}
  default = "{{ var.default }}"
}
{% endfor %}

{% for source in sources %}
source "{{ source.first_label }}" "{{ source.second_label }}" {
  {% for key, attr in source.attributes.items() %}{{ attr.name }} = {{ attr.str_value() }}
  {% endfor %}
}
{% endfor %}

build {
  sources = {{ buildblock.get_sources_as_str() }}
  {% for provisioner in buildblock.provisioners %}

  provisioner "{{ provisioner.type }}" {
    {% for key, attr in provisioner.attributes.items() %}{{ attr.name }} = {{ attr.str_value() }}
    {% endfor %}
  }
  {% endfor %}
  {% for postprocessor in buildblock.postprocessors %}

  post-processor "{{ postprocessor.type }}" {
    {% for key, attr in postprocessor.attributes.items() %}{{ attr.name }} = {{ attr.str_value() }}
    {% endfor %}
  }
  {% endfor %}
}
