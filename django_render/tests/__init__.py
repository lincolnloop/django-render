import os

from django import template
from django.conf import settings
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
        original_tmpldirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS += (self.test_templates,) 
        tmpl = "{% load render %}"\
                   "{% render user %}"
        o = self.renderTemplate(tmpl, user=self.user)
        self.assertEqual(o.strip(), 'this is user test')
        settings.TEMPLATE_DIRS = original_tmpldirs

    def testCustomTemplate(self):
        original_tmpldirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS += (self.test_templates,) 
        tmpl = "{% load render %}"\
                   "{% render user using custom.html %}"
        o = self.renderTemplate(tmpl, user=self.user)
        self.assertEqual(o.strip(), 'this is a custom template for user test')
        settings.TEMPLATE_DIRS = original_tmpldirs

    def testMissingCustomTemplate(self):
        "Missing templates revert to default template"
        tmpl = "{% load render %}"\
                   "{% render user using missing.html %}"
        o = self.renderTemplate(tmpl, user=self.user)
        self.assertEqual(o.strip(), '<a href="/users/test/">test</a>')
        
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
