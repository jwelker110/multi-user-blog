from app import Helper


class CreateHandler(Helper):
    def get(self):
        self.render('blog_create.html')
