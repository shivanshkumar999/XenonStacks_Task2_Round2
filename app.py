from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jamesbond990',
    'database': 'university',
}

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


app = Flask(__name__)

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

@app.route("/contactmail", methods=["POST","GET"])
def contactmail():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        message = request.form.get('message')

    body = f"""\
            <html>
            <body>
            <p>Hello, {name}.<br>
            Thanks for contacting Shivansh. He will get in touch with you shortly on the following contact details provided by you.</p><br>
            <p>Name : <span style='font-weight:bolder'>{name}</span></p>
            <p>Email : <span style='font-weight:bolder'>{email}</span></p>
            <p>Mobile No. : <span style='font-weight:bolder'>{mobile}</span></p>
            <p>Message : <span style='font-weight:bolder'>{message}</span></p>
            </body>
            </html>
            """
    
    res = f'Thanks for contacting me, {name}'
    SendEmail('shivanshkumar752@gmail.com', f"{name} contacted you via portfolio website", body)
    return render_template('contact.html', res = res)


@app.route("/logintest", methods=["POST","GET"])
def logintest():
    if request.method=='POST':
        uid = request.form.get('name')
        password = request.form.get('pass')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM students WHERE uid = %s AND password = %s"
        cursor.execute(query, (uid, password))
        student = cursor.fetchone()

    # Close the database connection
        cursor.close()
        conn.close()

    if student:
        # Successful login
        res = f"Welcome, {student[1]}!"
    else:
        # Failed login
        res = "Invalid uid or password. Please try again."
    return render_template('loginsuccess.html', res = res)

@app.route("/login")
def login():
    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True)

