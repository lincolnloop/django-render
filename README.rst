Django Render
=============

Overview
---------

Django render provides a template tag that works similar to an `inclusion tag <http://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags>`_, however it will attempt to use a custom template for each model. This is useful when iterating over a list of heterogeneous model instances or a queryset with generic relationships.


Installation
-------------

1. ``pip install -e git+git://github.com:lincolnloop/django-render.git#egg=django-render``
2. Add ``django_render`` to your ``INSTALLED_APPS``


Basic Usage
-----------

Create a template for each model you want to render in ``render/<application_name>/<model_name>.html`` in your template directory. The object will be passed to the template context as ``render_obj``.

Here is an example of how to use the tag in your templates::

    {% load render %}
    {% for obj in misc_object_list %}
        {% render obj %}
    {% endfor %}

For advanced usage see the docstring in ``django_render/templatetags/render.py``.


Acknowledgements
----------------

Thanks to Jacob Kaplan-Moss' `Jellyroll <http://github.com/jacobian/jellyroll>`_ for the inspiration.
