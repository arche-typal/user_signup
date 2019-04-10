from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/validate")
def display_user_signup():
    #b4jinja#return username_form.format(username="", username_error="", password="", password_error="", verifypassword="", user_email="", user_email_error="")
    template = jinja_env.get_template('index.html')
    return template.render() #variables auto ="", no need to set-up


def is_three_to_twenty(astring):
    len_string = len(astring)
    if len_string > 3 and len_string < 20:
        return True
    else:
        return False

def check_for_space(astring):
    if " " in astring:
        return True
    else:
        return False

def same_password(astring,astringtwo):
	if astring == astringtwo:
		return True
	else:
		return False

def valid_email(anemail):
	if "@" in anemail and "." in anemail:
		return True
	else:
		return False

@app.route('/validate', methods=['POST'])
def validate_username():
    username = request.form["username"]
    password = request.form["password"]
    verifypassword = request.form["verifypassword"]
    user_email = request.form["user_email"]

    username_error = ""
    password_error = ""
    user_email_error = ""

    if check_for_space(username):
        username_error = "Please no spaces in username" 
    elif not is_three_to_twenty(username):
        username_error = "Please enter a username between 3 and 20 characters"

    #password == verifypassword True?
    if not same_password(password,verifypassword):
        password_error = "Passwords do not match"
    elif check_for_space(password):
        password_error = "Please no spaces in password."
    elif not is_three_to_twenty(password):
        password_error = "Please enter a password between 3 and 20 characters."

    #valid email: no space, 3-20, "@" and ".", preserve
    if not user_email == "":
        if check_for_space(user_email):
            user_email_error = "Please no spaces in email."   
        elif not is_three_to_twenty(user_email):
            user_email_error = "Please enter an email between 3 and 20 characters"
        elif not valid_email(user_email):
            user_email_error = "Email needs and '@' and '.' in it."    
    
    if not username_error and not password_error and not user_email_error:
        #Redirect to welcome page, [username]
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username)

    else:
        password = ""
        verifypassword = ""

        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error,  #set up because passing through
            password_error=password_error, 
            password=password,
            username=username,
            verifypassword=verifypassword,
            user_email=user_email,
            user_email_error=user_email_error)

app.run()