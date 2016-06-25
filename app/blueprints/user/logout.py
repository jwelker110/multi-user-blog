from app.helpers import Helper


class LogoutHandler(Helper):
    def get(self):
        self.invalidate_sig()
        self.redirect('/')
