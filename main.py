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
from google.appengine.ext import db


class Location(db.Model):
    hashtag = db.StringProperty(required=True)
    location = db.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('SocLoc mola!!')
        # insert
        imagen = Location(hashtag="4", location="5,3")
        print imagen
        imagen.put()


class Foto(webapp2.RequestHandler):
    def get(self):
        # select
        q = Location.all()
        #q.filter("id=", 3)
        hashtag = q.get().hashtag
        location= q.get().location
        self.response.write(hashtag+" : "+location)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/f', Foto)
], debug=True)
