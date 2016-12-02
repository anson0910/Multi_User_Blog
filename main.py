import os
import jinja2
import webapp2
from google.appengine.ext import db
from datetime import datetime
from pytz import timezone

from models import Post
from models import User

from utils.hashing_salt_functions import *
from utils.validate_info import *


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

    def login(self, user):
        """
        Logs in user, responds with cookie, and redirects to welcome page
        :param user: instance of User model
        """
        user_id = user.key().id()
        cookie_val = make_secure_val(str(user_id))
        self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % cookie_val)
        self.redirect('/welcome')

    def get_user_id(self):
        """Returns user id if user is logged in, otherwise None"""
        # get the string of format user_id|hash(user_id) from cookie
        cookie_val = self.request.cookies.get('user_id')
        if cookie_val:
            return check_secure_val(cookie_val)


class MainPage(Handler):
    """Handler for front page, which lists most recent 10 posts"""
    def get(self):
        posts = db.GqlQuery('SELECT * FROM Post '
                            'ORDER BY created DESC LIMIT 10')
        self.render('blog.html', posts=posts)


class NewPostPage(Handler):
    """Handler for creating new post"""
    def render_newpost(self, subject='', content='', error_msg=''):
        self.render('new_post.html', subject=subject, content=content, error_msg=error_msg)

    def get(self):
        self.render_newpost()

    def post(self):
        user_id = self.get_user_id()
        if not user_id:
            self.redirect('/login')
            return

        subject, content = self.request.get('subject'), self.request.get('content')
        if subject and content:
            curr_time_str = datetime.now(timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M')
            post = Post(subject=subject, content=content, created=curr_time_str, user_id=user_id)
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


class EditPostPage(Handler):
    """Handler for editing post"""
    def render_editpost(self, subject='', content='', error_msg=''):
        self.render('edit_post.html', subject=subject, content=content, error_msg=error_msg)

    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        # verify user's identity
        self.render_editpost(post.subject, post.content)


class SignupHandler(Handler):
    """Handler for user sign up"""
    def get(self):
        self.render('user_signup.html')

    def post(self):
        def is_valid():
            """
            Verifies validity of input fields, and populates dict if invalid
            :return: True if input is valid
            """
            valid = True
            if not valid_username(username):
                params['err_username'] = "That's not a valid username."
                valid = False
            elif User.get_by_name(username):
                params['err_username'] = "That user already exists."
                valid = False

            if not valid_password(password):
                params['err_password'] = "That wasn't a valid password."
                valid = False
            elif password != verify:
                params['err_verify'] = "Your passwords didn't match."
                valid = False

            if not valid_email(email):
                params['err_email'] = "That's not a valid email."
                valid = False
            return valid

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = {'username': username,
                  'email': email}

        if is_valid():
            user = User.register(name=username, pw=password, email=email)
            self.login(user)
        else:
            self.render('user_signup.html', **params)


class LoginHandler(Handler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(name=username, pw=password)
        if not user:
            self.render('login.html', username=username, err_msg='Invalid login')
        else:
            self.login(user)


class LogoutHandler(Handler):
    def get(self):
        self.response.delete_cookie('user_id', path='/')
        # or as in lesson, self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/signup')


class WelcomeHandler(Handler):
    def get(self):
        user_id = self.get_user_id()
        if user_id:
            user = User.get_by_id(int(user_id))
            self.render('welcome.html', username=user.name)
            return
        self.redirect('/signup')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpost', NewPostPage),
                               ('/([0-9]+)/edit', EditPostPage),
                               ('/([0-9]+)', PostPage),
                               ('/signup', SignupHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/welcome', WelcomeHandler)],
                              debug=True)

