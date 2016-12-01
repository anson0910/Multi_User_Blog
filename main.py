import os
import jinja2
import webapp2
from google.appengine.ext import db
from datetime import datetime
from pytz import timezone

from models import Post


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    """General Handler"""
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    """Handler for front page, which lists most recent 10 posts"""
    def get(self):
        posts = db.GqlQuery('SELECT * FROM Post '
                            'ORDER BY created DESC LIMIT 10')
        self.render('blog.html', posts=posts)


class NewPostPage(Handler):
    """Handler for creating new post"""
    def render_newpost(self, subject='', content='', error_msg=''):
        self.render('newpost.html', subject=subject, content=content, error_msg=error_msg)

    def get(self):
        self.render_newpost()

    def post(self):
        subject, content = self.request.get('subject'), self.request.get('content')
        if subject and content:
            curr_time_str = datetime.now(timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M')
            post = Post(subject=subject, content=content, created=curr_time_str)
            post.put()
            self.redirect('/' + str(post.key().id()))
        else:
            error_msg = 'We need both a subject and some content!'
            self.render_newpost(subject, content, error_msg)


class PostPage(Handler):
    """Permalink for a specific post, give id of post in URL"""
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        self.render('permalink.html', post=post)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpost', NewPostPage),
                               ('/([0-9]+)', PostPage)],
                              debug=True)

