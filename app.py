from flask import Flask,render_template,url_for,redirect,request,session,jsonify,make_response,json
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
#from flask_login import UserMixin,LoginManager
from datetime import timedelta
from werkzeug.security import generate_password_hash,check_password_hash
#from flask_restful import Api,Resource ,reqparse,abort,fields,marshal_with
from flask_login import LoginManager
from flask_migrate import Migrate 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='dbmongocli'
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),nullable=False,unique=True)
	password = db.Column(db.String(80),nullable=False)
	#users can have many post for there is the one to many realtionship for the users to the many post .
	teacher = db.relationship('Teacher',backref='user',uselist=False)
	student = db.relationship('Student',backref='user',uselist=False)


	def __repr__(self):
		return self.username

class Teacher(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	teacher = db.Column(db.Integer,db.ForeignKey('user.id'))
	name = db.Column(db.String(20),nullable=False)
	phone_number = db.Column(db.String(20))
	address = db.Column(db.String(20),nullable=False)
	class_name = db.Column(db.String(20))


class Student(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	student = db.Column(db.Integer,db.ForeignKey('user.id'))
	name = db.Column(db.String(20),nullable=False)
	phone_number = db.Column(db.String(20),unique=True)
	address = db.Column(db.String(20),nullable=False)
	class_name = db.Column(db.String(20))


class Classes(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	classname = db.Column(db.String(20),nullable=False)

@app.route('/createclass',methods=['GET','POST'])
def createclass():
	if request.method == "POST":
		className = request.form.get('email')
		instance = Classes(classname= className)
		db.session.add(instance)
		db.session.commit()
		data = Classes.query.all()
		return render_template('classshow.html',data=data)
	
	return render_template('createclass.html')

@app.route('/classdelete/<int:pk>', methods = ['GET','POST'])
def classdelete(pk):
	instance = Classes.query.filter_by(id=pk).first()
	db.session.delete(instance)
	db.session.commit()
	data = Classes.query.all()
	return render_template('classshow.html',data=data)

@app.route('/classupdate/<int:pk>' ,methods = ['GET','POST'])
def classupdate(pk):
	if request.method == "POST":
		className = request.form.get('email')
		instance = Classes.query.filter_by(id=pk).first()
		instance.classname = className
		db.session.add(instance)
		db.session.commit()
		data = Classes.query.all()
		return render_template('classshow.html',data=data)

	data = Classes.query.filter_by(id=pk).first()
	print(data)
	return render_template('classupdate.html',data=data)


@app.route('/getclass',methods=['GET'])
def getclass():
	data = Classes.query.all()
	return render_template('classshow.html',data=data)


@app.route('/studentupdate/<int:pk>',methods =['GET','POST'])
def studentupdate(pk):
	if request.method == "POST":
		Name = request.form.get('name')
		phone_number = request.form.get('number')
		address = request.form.get('address')
		instance = Student.query.filter_by(id=pk).first()
		instance.name = Name
		instance.address = address 
		instance.phone_number= phone_number
		db.session.add(instance)
		db.session.commit()
		return render_template('student.html',student=instance)
	
	instance = Student.query.filter_by(id =pk).first()
	return render_template('update.html',instance=instance)


@app.route('/createclassteacher/<int:pk>',methods =['GET','POST'])
def createclassteacher(pk):
	if request.method == "POST":
		classname = request.form.get('classess')
		print(classname)
		instance = Teacher.query.filter_by(id=pk).first()
		instance.class_name = classname
		db.session.add(instance)
		db.session.commit()

		return render_template('front.html',teacher=instance)
	item = Teacher.query.filter_by(id=pk).first()
	query = Classes.query.all()
	instance ={'query':query,'data':item}
	return render_template('teacherclass.html',**instance)

@app.route('/createclassstudent/<int:pk>',methods =['GET','POST'])
def createclassstudent(pk):
	if request.method == "POST":
		classname = request.form.get('classess')
		print(classname)
		instance = Student.query.filter_by(id=pk).first()
		instance.class_name = classname
		db.session.add(instance)
		db.session.commit()
		return render_template('student.html',student=instance)
	item = Student.query.filter_by(id=pk).first()
	query = Classes.query.all()
	instance ={'query':query,'data':item}
	return render_template('studentclass.html',**instance)




@app.route('/studentdelete/<int:pk>',methods =['GET','POST'])
def studentdelete(pk):
	instance = Student.query.filter_by(id=pk).first()
	user = instance.student
	db.session.delete(instance)
	db.session.commit()
	user_data = User.query.filter_by(id=user).first()
	db.session.delete(user_data)
	db.session.commit()
	return render_template('index.html')



@app.route('/')
def hello_world():
	return "hello i m hemant and how are you"

@app.route('/products')
def index():
	return "This is the application for the python developer"

@app.route('/home')
def Home():
	return render_template('index.html')

@app.route('/signup')
def signup():
	user_list = User.query.all()
	usernames = []
	for user in user_list:
		usernames.append(user.username)
	return render_template('register.html', user=usernames)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/studentlogin',methods =['GET','POST'])
def Studentlogin():
	if request.method == "POST":
		username = request.form.get('email')
		plain_password = request.form.get('pwd')
		user=User.query.filter_by(username=username).first()
		context = {}
		if user:
			if check_password_hash(user.password,plain_password):
				user = User.query.filter_by(username=username).first()
				student = user.id
				student = Student.query.filter_by(student = student).first()
				context ={'student':student}
				return render_template('student.html',student=student)
		else:
			error = "User Does Not Exist with the Username"
			return render_template('studentlogin.html',error = error)
	
  
	return render_template('studentlogin.html')


@app.route('/login_valid',methods=['POST'])
def login_valid():
	username = request.form.get('email')
	plain_password = request.form.get('pwd')
	user=User.query.filter_by(username=username).first()
	context = {}
	if user:
		if check_password_hash(user.password,plain_password):
			user = User.query.filter_by(username=username).first()
			teacher = user.id
			teacher = Teacher.query.filter_by(teacher = teacher).first()
			context ={'teacher':teacher}
			
			return render_template('front.html',teacher=teacher)
		else:
			return "password does not match"
	
	
	return "user not exist"

@app.route('/studentsignup',methods=['GET','POST'])
def studentsignup():
	if request.method == "POST":
		username=request.form.get('email')
		password=generate_password_hash(request.form.get('pwd'))
		repassword=request.form.get('repwd')
		Name = request.form.get('name')
		phone_number = request.form.get('number')
		address = request.form.get('address')
		user=User.query.filter_by(username=username).first()
		if not user:
			obj=User(username=username,password=password)
			db.session.add(obj)
			db.session.commit()
			obj = User.query.filter_by(username =username).first()

			student = Student(student= obj.id,name=Name,phone_number=phone_number,address=address,class_name="none")
			db.session.add(student)
			db.session.commit()
			student= Student.query.filter_by(student=obj.id).first()
			context = {'student':student}
			return render_template('student.html',student=student)
		else:
			error="User is Already Registered"
			return render_template('studentregister.html',error=error)
	else:
		return render_template('studentregister.html')



@app.route('/delete/<int:pk>',methods =['GET'])
def Delete(pk):
	instance = Teacher.query.filter_by(id=pk).first()
	user = instance.teacher
	db.session.delete(instance)
	db.session.commit()
	user_data = User.query.filter_by(id = user).first()
	db.session.delete(user_data)
	db.session.commit()
	return render_template('index.html')

@app.route('/update/<int:pk>',methods=['GET','POST'])
def delete(pk):
	if request.method == "POST":
		Name = request.form.get('name')
		phone_number = request.form.get('number')
		address = request.form.get('address')
		instance = Teacher.query.filter_by(id=pk).first()
		instance.name = Name
		instance.address = address 
		instance.phone_number= phone_number
		db.session.add(instance)
		db.session.commit()
		return render_template('front.html',teacher=instance)
	
	instance = Teacher.query.filter_by(id = pk).first()
	return render_template('teacherupdate.html',instance=instance) 
	


@app.route('/update/<int:pk>',methods =['POST'])
def Update(pk):
	instance = Tecaher.query.filter_by(id=pk).first()
	
@app.route('/register_user',methods=['POST'])
def register_user():
	username=request.form.get('email')
	password=generate_password_hash(request.form.get('pwd'))
	repassword=request.form.get('repwd')
	Name = request.form.get('name')
	phone_number = request.form.get('number')
	address = request.form.get('address')
	user=User.query.filter_by(username=username).first()
	if not user:
		obj=User(username=username,password=password)
		db.session.add(obj)
		db.session.commit()
		obj = User.query.filter_by(username =username).first()
		teacher = Teacher(teacher= obj.id,name=Name,phone_number=phone_number,address=address,class_name="none")
		db.session.add(teacher)
		db.session.commit()
		teacher= Teacher.query.filter_by(teacher=obj.id).first()
		
		return render_template('front.html',teacher = teacher)
	else:
		error="User is Already Registered"
		return render_template('register.html',error=error)

@app.route('/logout')
def Logout():
	active = False 
	return render_template('main.html',context=active)


@app.route('/contact/')
def Contact():
	return "Contacts to me"
	

if __name__=="__main__":
	app.run(Debug=True)


