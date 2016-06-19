import os
import random
import string
from hashlib import sha256

import jinja2
import webapp2
from webapp2_extras import sessions
from secret import SECRET

template_dir = os.path.join(os.getcwd(), 'templates/')
J = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Helper(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def generate_csrf(self):
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in xrange(32))
        self.session['csrf_token'] = token
        return token

    def validate_csrf(self, token):
        if token is None:
            return False
        return self.session.get('csrf_token') == token

    def generate_sig(self, data):
        h = sha256(data + SECRET).hexdigest()
        return data + '|' + h

    def validate_sig(self, h):
        data = h.split('|')[0]
        return h == sha256(data + SECRET).hexdigest()

    def retrieve_sig_data(self, h):
        return h.split('|')[0]

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_temp(self, template, **kw):
        template = J.get_template(template)
        return template.render(kw)

    def render(self, template, **kw):
        self.write(self.render_temp(template, **kw))
