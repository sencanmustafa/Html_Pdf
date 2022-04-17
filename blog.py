# -*- coding:utf-8 -*-
import jinja2
import pdfkit
import wtforms
from flask import Flask ,Response, render_template ,flash,redirect,url_for,session,logging,request,make_response
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
import urllib.parse
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash,check_password_hash
import data_acces
from functools import wraps


class LoginForm(Form):
    username = StringField("Username",validators=[validators.length(min=3),validators.DataRequired()])
    password= PasswordField("Password",validators=[validators.DataRequired("Password")])
class HtmlForm(Form):
    text1 = StringField("Text1",validators=[validators.data_required("TEXT")])
    text2 = StringField("Text2",validators=[validators.data_required("TEXT")])

app = Flask(__name__)
app.secret_key = "mustiler463"



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return decorated_function

@app.route("/login", methods = ["GET","POST"])

def login():
    Login_form = LoginForm(request.form)
    if request.method == "POST":
        t_username = Login_form.username.data
        t_password = Login_form.password.data
        if data_acces.validate(t_username, t_password):
            session["logged_in"] = True
            session["username"] = t_username
            flash(f"Correct! You logged in {t_username}!","success")
            return redirect(url_for("convert"))
        else:
            flash("Wrong Username or Password","danger")
            return redirect(url_for("login"))


    return render_template("login.html",form=Login_form)



@app.route("/get_pdf",methods = ["GET","POST"])
@login_required
def get_pdf():
    session['my_list'] = data_acces.list
    if request.method == "POST":
        rendered = render_template('get_pdf.html')
        pdf = pdfkit.from_string(rendered,False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-disposition'] = 'attachment ; filename = output.pdf'
        return response
    return redirect(url_for('converted'))

@app.route("/converted",methods = ["GET","POST"])
@login_required
def converted():
    session['my_list'] = data_acces.list
    return render_template("converted.html")

@app.route("/logout")
def logout():
    data_acces.list.clear()
    session.clear()
    return redirect(url_for("login"))


@app.route("/convert",methods = ["GET","POST"])
@login_required
def convert():
    html_form = HtmlForm(request.form)
    if request.method == "POST":
        data_text1 = html_form.text1.data
        data_text2 = html_form.text2.data
        data_acces.list.append(data_text1)
        data_acces.list.append(data_text2)
        flash("Converted...","success")
        session['my_list'] = data_acces.list
        return redirect(url_for("converted",my_list = data_acces.list))
    return render_template("convert.html",form = html_form)










@app.route("/")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)


