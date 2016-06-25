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

    def validate_user(self):
        # make sure we are logged in right meow
        # validate the cookie itself, since we need to be sure
        # they are who they say they are
        if not self.validate_sig():
            self.invalidate_sig()
            return None
        user = self.retrieve_sig_data()

        sess_user = self.session.get('user')
        if sess_user is None:
            self.invalidate_sig()
            return None
        if user != sess_user:
            # the user is not who they say they are
            self.invalidate_sig()
            return None
        return user

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
        self.response.set_cookie('user', data + '|' + h)

    def validate_sig(self):
        h = self.request.cookies.get('user', '')
        data = h.split('|')[0]
        if h == '' or h != data + '|' + sha256(data + SECRET).hexdigest():
            self.invalidate_sig()
            return False
        return True

    def retrieve_sig_data(self):
        h = self.request.cookies.get('user')
        if h is None:
            return None
        return h.split('|')[0]

    def invalidate_sig(self):
        self.response.delete_cookie('user')
        self.session['user'] = None

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_temp(self, template, **kw):
        template = J.get_template(template)
        return template.render(kw)

    def render(self, template, **kw):
        self.write(self.render_temp(template, user=self.validate_user(), **kw))

