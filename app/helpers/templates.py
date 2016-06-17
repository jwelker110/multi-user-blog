import os
import jinja2
import webapp2

template_dir = os.path.join(os.getcwd(), 'templates/')
J = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Helper(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_temp(self, template, **kw):
        template = J.get_template(template)
        return template.render(kw)

    def render(self, template, **kw):
        self.write(self.render_temp(template, **kw))

