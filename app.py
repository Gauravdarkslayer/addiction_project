from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from random import randint
import smtplib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/devansh/Desktop/Addiction/addiction_project/database.db'
# 'sqlite:////Users/devansh/Desktop/Addiction/addiction_project/database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(80))
    l_name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/testing")
def testing():
    return render_template("request_submitted.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/request1")
def request1():
    return render_template("Submit_Request.html")

@app.route("/signup")
def signup():
    return render_template("register.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("This is request . form",request.form)
        mail = request.form["email"]
        passw = request.form["passw"]
        print("I am inside Login Method")
        login = user.query.filter_by(email=mail).first()
        if login is not None:
            exact_password=login.password
            if exact_password == passw:
                return render_template("Submit_Request.html")
            else:
                temp={"msg":"Password Is Incorrect Please Try Again !"}
                return render_template("login.html",**temp)
        else:
            temp={"msg":"Email ID is not registered Please Sign Up"}
            return render_template("login.html",**temp)
    else:        
        return render_template("login.html")


f_name,l_name,mail,passw="","","",""
otp = randint(1000,9999)
print(otp)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        global f_name,l_name,mail,passw
        
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        mail = request.form['mail']
        passw = request.form['passw']


        c_email = user.query.filter_by(email=mail).first()
        if c_email is not None:
            print("Hello I am In")
            temp={"msg":"User Already Exists"}
            return render_template('register.html',**temp)
        else:
        ### SENDING OTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('www.gaurav10bhojwani@gmail.com','inuajyeavvhhcxfo')
            subject="otp for prevent you"
            body="DO NOT SHARE THIS OTP WITH ANYONE"+" "+str(otp)
            msg=f'subject: {subject}\n\n{body}'
            # global myemail
            server.sendmail(
                    'www.gaurav10bhojwani@gmail.com',
                    mail,
                    # 'gaurav10me@gmail.com',
                    msg
                )   
            # myemail=request.POST.get('email')    
            print("sent successfully")
            server.quit()
            #####OTP SENT
            return render_template("verify_email.html")
    return render_template("register.html")


@app.route("/email_verify",methods=["GET","POST"])
def email_verify():
    global otp
    print(otp)
    c_otp = request.form.get("otp")
    if otp == int(c_otp):
        register = user(f_name = f_name,l_name=l_name,email = mail, password = passw)
        db.session.add(register)
        db.session.commit()
    return redirect("/login")


# @app.route("/submit_req")
# def submit_req():
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
