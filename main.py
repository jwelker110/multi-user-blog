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
import os

import jinja2
import webapp2

j = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Helper(webapp2.RequestHandler):
    def render(self, template, params):
        template = j.get_template('index.html')
        self.response.write(template.render(params))

    def render_template(self, template, **kw):
        self.render(self, template, **kw)


class MainHandler(Helper):
    def get(self):
        self.render_template('index.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
