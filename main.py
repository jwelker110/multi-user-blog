#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from app.helpers import Helper, SECRET, J, datetimefilter, shortenfilter
from app.blueprints.user import RegisterHandler, LoginHandler, LogoutHandler
from app.blueprints.post import PostCreateHandler, PostEditHandler, PostHandler, PostDeleteHandler
from app.blueprints.filter import DefaultHandler, AuthorHandler


config = {'webapp2_extras.sessions': {
    'secret_key': SECRET,
}}

J.filters['datetime'] = datetimefilter
J.filters['shorten'] = shortenfilter


class MainHandler(Helper):
    def get(self):
        self.render('index.html')


app = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    (r'/author/.*', AuthorHandler),
    ('/user/register', RegisterHandler),
    ('/user/login', LoginHandler),
    ('/user/logout', LogoutHandler),
    ('/post/create', PostCreateHandler),
    ('/post/view', PostHandler),
    ('/post/edit', PostEditHandler),
    ('/post/delete', PostDeleteHandler)
], config=config, debug=True)
