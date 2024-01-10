from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

import os

app = Flask(__name__)

mydb = mysql.connector.connect(
    host= os.environ['host'],
    user= os.environ['user'],
    password= os.environ['password'],
    database= os.environ['database'],
)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'jamesbond990'
# app.config['MYSQL_DB'] = 'university'

#  Send mail function
def SendEmail(toaddr,subject,message):
    fromaddr = "666anonymailer999@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'html'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    try:
        s.login(fromaddr, "kxwapeedoljoghol")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        return "Email successfully sent. Wait for Shivansh to contact you."
    except:
        return "An Error occured while sending email."
    finally:
        s.quit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/programs")
def programs():
    return render_template('programs.html') 

@app.route("/about")
def about():
    return render_template('about.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/signup",methods=['POST','GET'])
def signup():
    return render_template('signup.html')

@app.route("/contactmail", methods=["POST","GET"])
def contactmail():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

    body = f"""\
            <html>
            <body>
            <p>Hello, {name}.<br>
            Thanks for contacting The Gurukul. He will get in touch with you shortly on the following contact details provided by you.</p><br>
            <p>Name : <span style='font-weight:bolder'>{name}</span></p>
            <p>Email : <span style='font-weight:bolder'>{email}</span></p>
            <p>Message : <span style='font-weight:bolder'>{message}</span></p>
            </body>
            </html>
            """
    SendEmail('shivanshkumar752@gmail.com', f"{name} contacted you via portfolio website", body)

    cursor = mydb.cursor()

    # Check if the username and password match a record in the database
    # query = "insert into students (uid, password) values (%s,%s)"
    query = "insert into contactqueries (name,email,message) values ( %s, %s,%s)"
    cursor.execute(query,(name,email,message))
    mydb.commit()

    return render_template('contact.html', res = f'Thanks for contacting Us, {name}. We will get back to you shortly.')


@app.route("/signuptest", methods=["POST","GET"])
def signuptest():
    if request.method=='POST':
        uid = request.form.get('name')
        password = request.form.get('pass')

        cursor = mydb.cursor()

        # Check if the username and password match a record in the database
        # query = "insert into students (uid, password) values (%s,%s)"
        query = "insert into students (uid,password) values ( %s, %s)"
        cursor.execute(query,(uid,password))
        mydb.commit()

        query = "select * from students where uid = %s and password = %s"
        cursor.execute(query,(uid,password))
        student = cursor.fetchone()

        # Close the cursor
        cursor.close()

    if student:
        # Successful login
        res = f"Welcome, {student[0]}!, You are registered Now."
    else:
        # Failed login
        res = "Some error occoured. Please try again."
    return render_template('loginsuccess.html', res = res)


@app.route("/logintest", methods=["POST","GET"])
def logintest():
    if request.method=='POST':
        uid = request.form.get('name')
        password = request.form.get('pass')

        cursor = mydb.cursor()

        # Check if the username and password match a record in the database
        # query = "insert into students (uid, password) values (%s,%s)"
        query = "select * from students where uid = %s and password = %s"
        cursor.execute(query,(uid,password))
        student = cursor.fetchone()

        # Close the cursor
        cursor.close()

    if student:
        # Successful login
        res = f"Welcome, {student[0]}!"
    else:
        # Failed login
        res = "Invalid uid or password. Please try again."
    return render_template('loginsuccess.html', res = res)

@app.route("/login")
def login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)

