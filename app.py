from flask import Flask, request, session
from flask.templating import render_template
import requests, json

app = Flask(__name__)


@app.route('/')
def login():
    message=""
    return render_template('login.html', message = message)

@app.route('/home')
def user_home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupQues')
def signup_ques():
    return render_template('signup_question.html')

@app.route('/loginQues')
def login_ques():
    return render_template('login_question.html')

@app.route('/validSignUp')
def valid_signup():
    return render_template('confirmSignUp.html')

@app.route('/forgotPassword') 
def forgot_password():
    return render_template('forgotPassword.html')

@app.route('/validForgotPassword')
def confirm_forgot_password():
    return render_template('confirmForgotPassword.html')

@app.route("/user_login",methods=['POST','GET'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    data = {'username':email,'password':password}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/login", json=data)
    print(response.json()['status'])
    if(response.json()['status'] == 'success'):
        return render_template("home.html",email=email)
    else:
        message="Incorrect password or username"
        return render_template("login.html", message = message)

@app.route("/user_signup",methods=['POST','GET'])
def user_signup():
    print("into signup")
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmpassword=request.form['confirmpassword']
    university=request.form['university']
    role=request.form['role']
    print(role)
    if password == confirmpassword :
        data = {'email':email,'password':password,'name':name,'university':university,'username':email,'role':role}
        response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/signup", json=data)     
        if response.json()['message']=="Success, Enter OTP":
            return render_template('confirmSignUp.html', username = email, password = password, name = name, university = university,role = role)
        else:
            message=response.json()['message']
            return render_template("signup.html", message = message) 
    else:
        message="Password are not matching"
        return render_template("signup.html", message = message)      



@app.route("/signupValidate",methods=['POST','GET'])
def signup_validate():
    #Write logic to check signup otp
    email = request.form['email']
    password = request.form['password']
    otp = request.form['otp']
    name = request.form['name']
    university = request.form['university']
    role=request.form['role']
    data = {'password':password,'code':otp,'username':email,'name':name,'university':university,'role':role}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/confirmsignup", json=data) 
    if "code" in response.json():
        message="Successfully Registered"
        return render_template('login.html',message=message)
    else:
        message = response.json()['message']
        return render_template('confirmSignUp.html', role=role,username = email, password = password,name=name,university=university, message = message)


@app.route("/userForgotPassword",methods=['POST','GET'])
def password_forgot():
    #Write logic to reset password
    email = request.form['email']
    data = {'username':email}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/forgotpassword", json=data) 
    print(response.json())
    if response.json()['success']=="True":
        return render_template('confirmForgotPassword.html')
    else:
        message = response.json()['message']
        return render_template('forgotPassword.html',message=message)


@app.route("/passwordValidate",methods=['POST','GET'])
def password_validate():
    #Write logic to reset password otp
 
    return render_template('login.html')


@app.route("/signupQues",methods=['POST','GET'])
def ques_signup():
    ques1 = request.form['ques1']
    ans1 = request.form['ans1']
    ques2 = request.form['ques2']
    ans2 = request.form['ans2']
    ques3 = request.form['ques3']
    ans3 = request.form['ans3']
    data = {ques1:ans1,ques2:ans2,ques3:ans3}
    print(data)
    message="Signed Up"
    return render_template('login.html', message = message)

@app.route("/loginQues",methods=['POST','GET'])
def ques_login():
    answer = request.form['answer']
    print(answer)
    return "Logged In"

@app.route("/logout",methods=['POST','GET'])
def user_logout():
    email = request.form['email']
    data = {'username':email}
    response = requests.post("https://ril4n9as71.execute-api.us-east-1.amazonaws.com/prod/userlogout", json=data) 
    if response.json()['success']=="True":
        message="Logged Out Successfully"
        return render_template('login.html', message = message)
    else:
        return render_template('login.html')

@app.route("/resendOTPCode",methods=['POST','GET'])
def resend_otp_code():
    email = request.form.get('email')
    password = request.form['password']
    data = {'username':email}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/resendcode", json=data) 
    if response.json()['success']=="True":
        message = "Code Sent Again"
        return render_template('confirmSignUp.html', username = email, password = password, message = message)
    else:
        message = "Error Sending Code, Please Try Again"
        return render_template('confirmSignUp.html', username = email, password = password, message = message)    

if __name__ == '__main__':
    app.run()