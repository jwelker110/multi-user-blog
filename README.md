# Multi-User Blog

The goal of this project is to create a simple multi-user blog along the lines of "Medium". 

Users should be able to create an account with login/logout functionality, and create/edit/delete posts and comments.

Checkout the [live](https://multi-user-blog-1340.appspot.com/) version of this project.

### Project specifications

Blog must include the following features:
- Front page that lists blog posts.
- A form to submit new entries.
- Blog posts have their own page.

Registration must include the following features:
- A registration form that validates user input, and displays the error(s) when necessary.
- After a successful registration, a user is directed to a welcome page with a greeting, “Welcome, *name*” where *name* is a name set in a cookie.
- If a user attempts to visit a restricted page without being signed in (without having a cookie), then redirect to the Signup page.

Login must include the following features:
- Have a login form that validates user input, and displays the error(s) when necessary.

Users must include the following features:
- Users should only be able to edit/delete their posts. They receive an error message if they disobey this rule.
- Users can like/unlike posts, but not their own. They receive an error message if they disobey this rule.
- Users can comment on posts. They can only edit/delete their own posts, and they should receive an error message if they disobey this rule.

Code must conform to the [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)

### Setting up the project

1. [Clone](https://github.com/jwelker110/multi-user-blog.git) this repo.
2. Create a folder called lib in the project root.
3. Using [pip](https://pip.pypa.io/en/stable/installing/), `pip install -t /path/to/lib pycrypto` and `pip install -t /path/to/lib wtforms`
4. In the project's *helpers* folder, create a *secret.py* file and place `SECRET = 'YOUR SECRET HERE'` on the first line.
5. Follow instructions below for installing and setting up Google App Engine with the project.

### Setting up your computer

1. [Install Python](https://www.python.org/downloads/) if necessary.
2. [Install Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
3. Open GoogleAppEngineLauncher.
4. [Sign Up for a Google App Engine Account](https://appengine.google.com/).
5. Create a new project in [Google’s Developer Console](https://console.cloud.google.com/) using a unique name.
6. Create a new project from the file menu and choose this project's folder.
7. Deploy this project by pressing deploy in GoogleAppEngineLauncher.
8. When developing locally, click “Run” in GoogleAppEngineLauncher and visit localhost:Port in your favorite browser, where Port is the number listed in GoogleAppEngineLauncher’s table under the column Port.

