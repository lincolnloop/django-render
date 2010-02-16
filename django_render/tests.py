from django import template
from django.test import TestCase
from django.contrib.auth.models import User


class TagTestCase(TestCase):
    """Helper class with some tag helper functions"""
    
    def installTagLibrary(self, library):
        template.libraries[library] = __import__(library)
        
    def renderTemplate(self, tstr, **context):
        tmpl = template.Template(tstr)
        cntxt = template.Context(context)
        return tmpl.render(cntxt)

class OutputTagTest(TagTestCase):
    
    def setUp(self):
        self.installTagLibrary('django_render.templatetags.render')
        self.user = User.objects.create(username='test')
        self.test_templates = os.path.join(os.path.dirname(
                                                os.path.realpath(__file__)), 
                                                'templates')
        
    def testDefaultTemplate(self):
        tmpl = "{% load render %}"\
                   "{% render user %}"
        o = self.renderTemplate(tmpl, user=self.user)
        self.assertEqual(o.strip(), '<a href="/users/test/">test</a>')

    def testModelTemplate(self):
        original_templdirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS += self.test_templates 
        tmpl = "{% load render %}"\
                   "{% render user %}"
        o = self.renderTemplate(tmpl, user=self.user)
        self.assertEqual(o.strip(), 'this is user test')
        settings.TEMPLATE_DIRS = original_templatedirs

    """ 
    def testAsVar(self):
        tmpl = "{% load geotagging %}"\
                   "{% get_objects_nearby obj.point as nearby_objs %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(tmpl, obj=self.denver)
        self.assertEqual(o.strip(), "1")

    def testShortDistance(self):
        # DIA is about 18 miles from downtown Denver
        short_tmpl = "{% load geotagging %}"\
                   "{% get_objects_nearby obj.point as nearby_objs within 17 %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(short_tmpl, obj=self.denver)
        self.assertEqual(o.strip(), "1")
        long_tmpl = short_tmpl.replace("17", "19")
        o = self.renderTemplate(long_tmpl, obj=self.denver)
        self.assertEqual(o.strip(), "2")

    def testLongDistance(self):
        # Ann Arbor is about 1122 miles from Denver
        short_tmpl = "{% load geotagging %}"\
                   "{% get_objects_nearby obj.point within 1115 as nearby_objs %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(short_tmpl, obj=self.denver)
        self.assertEqual(o.strip(), "2")
        long_tmpl = short_tmpl.replace("1115", "1125")
        o = self.renderTemplate(long_tmpl, obj=self.denver)
        self.assertEqual(o.strip(), "3")
    """
        
class SyntaxTagTest(TestCase):
    
    def getNode(self, strng):
        from django_render.templatetags.render import render
        return render(None, template.Token(template.TOKEN_BLOCK, 
                                                       strng))
        
    def assertNodeException(self, strng):
        self.assertRaises(template.TemplateSyntaxError, 
                          self.getNode, strng)

    def testInvalidSyntax(self):
        self.assertNodeException("render")
        self.assertNodeException("render obj bad_arg")
