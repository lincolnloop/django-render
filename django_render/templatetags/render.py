from django import template
from django.db import models
from django.template.context import Context
from django.template.loader import render_to_string

register = template.Library()

class RenderNode(template.Node):
    def __init__(self, obj, using=None):
        self.obj = obj
        self.using = using
        
    def render(self, context):
        try:
            var = template.resolve_variable(self.obj, context)
        except template.VariableDoesNotExist:
            return ""
        if not isinstance(var, models.Model):
            return ""
        template_root = 'render/%s/%s' % (var._meta.app_label, 
                                          var._meta.object_name.lower())
        if self.using:
            template_name = '%s__%s' % (template_root, self.using)
        else:
            template_name = '%s.html' % template_root
        template_list = [
            template_name,
            'render/default.html',
        ]

        # We probably want access to variables added by the context processors
        # so let's copy the existing context since we might not have access
        # to the request object.
        render_context = Context()
        for dict in context.dicts:
            render_context.dicts.append(dict.copy())
        render_context['render_obj'] = var
        rendered = render_to_string(template_list, render_context)
        return rendered 

@register.tag
def render(parser, token):
    """
    Renders a model-specific template for any model instance.
    
    ``render`` works like a model-aware inclusion tag and is used like so::
    
        {% render obj %}
        
    Assuming ``obj`` is an instance of the ``Post`` model from the ``blog``
    application, this tag will render ``render/blog/post.html`` passing
    the second-argument to the template as ``obj``. The template name is
    ``render/[application_name]/[model_name].html`` in lower-case.

    If you'd like to use different templates in different areas of your
    site, you can do so with the ``using`` argument. For example::
        
        {% render obj using long.html %}

    This will render the template ``render/[application_name]/[model_name]__long.html``

    In the event the necessary template cannot be found, ``render/default.html``
    will be used.
       
    """
    
    bits = token.split_contents() 

    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r tag takes at least 2 arguments" % bits[0])

    item = bits[1]
    args = {}
    biter = iter(bits[2:])
    for bit in biter:
        if bit == "using":
            args["using"] = biter.next()
        else:
            raise template.TemplateSyntaxError("%r tag got an unknown argument: %r" % (bits[0], bit))
    
    return RenderNode(item, **args)
