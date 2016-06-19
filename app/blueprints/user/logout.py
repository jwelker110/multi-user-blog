from app.helpers import Helper


class LogoutHandler(Helper):
    def get(self):
        self.session['user'] = None
        self.response.delete_cookie('user')
        self.redirect('/', True)
