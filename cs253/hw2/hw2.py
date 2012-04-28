# Standard libs
import cgi
import re
import urllib

# GAE libs
import webapp2

VALID_USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
VALID_PASSWORD_REGEX = re.compile(r"^.{3,20}$")
VALID_EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class Form:
    def __init__(self):
        # ROT13 textare
        self.text                   = ""

        # Signup fields
        self.username               = ""
        self.email                  = ""

        # Signup errors
        self.username_error         = ""
        self.password_error         = ""
        self.confirm_password_error = ""
        self.email_error            = ""

        self.html_template = """<form action="/rot13" method="post">
  <fieldset>
    <legend>ROT13 Encoder</legend>
    <div><textarea name="text">%(text)s</textarea><div>
    <div><input type="submit"><div>
  </fieldset>
</form>

<form action="/signup" method="post">
  <fieldset>
    <legend>Sign Up</legend>
    <div>
      <label for="username">
        Username:
        <input type="text" id="username" name="username" value="%(username)s">
        <span style="color:#f00">%(username_error)s</style>
      </label>
    </div>
    <div>
      <label for="password">
        Password:
        <input type="password" id="password" name="password">
        <span style="color:#f00">%(password_error)s</style>
      </label>
    </div>
    <div>
      <label for="confirm_password">
        Confirm Password:
        <input type="password" id="confirm_password" name="verify">
        <span style="color:#f00">%(confirm_password_error)s</style>
      </label>
    </div>
    <div>
      <label for="email">
        Email (optional):
        <input type="text" id="email" name="email" value="%(email)s">
        <span style="color:#f00">%(email_error)s</style>
      </label>
    </div>
    <div>
      <input type="submit">
    </div>
  </fieldset>
</form>
"""
    def render(self):
        return self.html_template % { "text"                   : self.text,
                                      "username"               : self.username,
                                      "email"                  : self.email,
                                      "username_error"         : self.username_error,
                                      "password_error"         : self.password_error,
                                      "confirm_password_error" : self.confirm_password_error,
                                      "email_error"            : self.email_error }

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, Udacity!')

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if not username:
            username = "buddy"
        self.response.out.write('<h1>Welcome, %s!</h1>' % (cgi.escape(username, quote=True)))

class ROT13(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(Form().render())

    def post(self):
        input_text = self.request.get("text")

        if not input_text:
            self.redirect("/hw2")

        encoded_text = input_text.encode("rot13")
        escaped_encoded_text = cgi.escape(encoded_text, quote=True)

        form = Form()
        form.text = escaped_encoded_text

        self.response.out.write(form.render())

class SignUp(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(Form().render())

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_confirm_password = self.request.get("verify")
        user_email = self.request.get("email")

        form = Form()
        has_errors = False

        # Validate username
        if user_username:
            form.username = cgi.escape(user_username, quote=True)

            if not VALID_USERNAME_REGEX.match(user_username):
                form.username_error = "That's not a valid username."
                has_errors = True
        else:
            form.username_error = "That's not a valid username."
            has_errors = True

        # Validate password
        if not user_password or not VALID_PASSWORD_REGEX.match(user_password):
            form.password_error = "That wasn't a valid password."
            has_errors = True
        else:
            # Validate password confirmation
            if user_password != user_confirm_password:
                form.confirm_password_error = "Your passwords didn't match."
                has_errors = True

        # Validate email
        if user_email:
            form.email = cgi.escape(user_email, quote=True)

            if not VALID_EMAIL_REGEX.match(user_email):
                form.email_error = "That's not a valid email."
                has_errors = True

        if has_errors:
            self.response.out.write(form.render())
        else:
            urlencoded_username = urllib.quote_plus(user_username)
            self.redirect("/welcome?username=%s" % (urlencoded_username))

app = webapp2.WSGIApplication([('/', MainPage),
                               ("/welcome", Welcome),
                               ("/rot13", ROT13),
                               ("/signup", SignUp)],
                              debug=True)
