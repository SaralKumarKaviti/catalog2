from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import DummyPassword, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


engine=create_engine('sqlite:///test.db',connect_args={'check_same_thread': False},echo=True)
#engine=create_engine('sqlite:///iiit.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

app=Flask(__name__)

app.secret_key='super_secret_key'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='saralkumar442@gmail.com'
app.config['MAIL_PASSWORD']='saral2328'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)
otp=randint(000000,999999)
testEmail = ""

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html")

@app.route("/email")
def email():	
	return render_template("demo_email.html")

@app.route("/verify_email", methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	getData = session.query(DummyPassword).filter_by(email=email).count()
	if getData > 0:
		flash("User Already Exists",'warning')
		return render_template('demo_email.html')
	else:
		register = DummyPassword(
					email=email,					
					password=str(otp),
					status=0)
		print("----------",email)
		session.add(register)
		session.commit()

		msg=Message('Temporary Password',sender='saralkumar442@gmail.com',recipients=[email])
		msg.body="User Name: "+email+ " and Temporary Password: "+str(otp)
		mail.send(msg)
		flash('Temporary Password has been generated to Email ID, So Check it Once', "success")
	return render_template('login.html')


@app.route('/login', methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	try:
		if request.method == "POST":
			userDetails = session.query(DummyPassword).filter_by(
				email=request.form['email'],
				password=request.form['password']).first()
			if userDetails:				
				login_user(userDetails)
				print(userDetails.status, "--------------------------")
				if userDetails.status == 0:
					return redirect(url_for('reset_password'))
					#return redirect(url_for('reset_password'))
				elif  userDetails.status == 1:
					return render_template('home.html')				
			else:
				flash("Invalid Username or Password,","danger")
				return render_template("login.html", title="Login")
		else:
			#flash("Invalid Username or Password,","danger")
			return render_template("login.html", title="Login")
		
	except Exception as e:
		flash(str(e)+"Login Failed, Please Check & Try Again ...!","danger")
	else:
		return render_template("login.html", title="Login")
	return render_template('login.html')

@app.route("/reset_password",methods=['POST',"GET"])
def reset_password():
	if request.method=='POST':
		email = request.form['email']
		oldpassword=request.form['oldpass']
		newpassword=request.form['newpass']
		confirmpassword=request.form['confpass']
		status = 1
		
		getPassword=session.query(DummyPassword).filter_by(
			email=email,
			password=oldpassword ).first()
		if getPassword and (newpassword == confirmpassword):
			getPassword.password = newpassword
			getPassword.status = status
			# session.add(getPassword)
			session.commit()
			flash("Password Reseted Successfully",'success')
			return redirect(url_for('logout'))
		else:
			flash("Old Password / New/Confirm Password Not Match",'warning')
			return render_template('reset_password.html')	

	else:
		return render_template('reset_password.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


if __name__=='__main__':
	app.config['SECRET_KEY'] = 'e7a9804ba98684deefd88d6a6c8cd0db'
	login_manager = LoginManager(app)
	login_manager.login_view = 'login'
	login_manager.login_message_category = 'info'

	@login_manager.user_loader
	def load_user(user_id):
		return session.query(DummyPassword).get(int(user_id))
	app.run(debug=True)
	app.run(host='0.0.0.0', port=5000)



