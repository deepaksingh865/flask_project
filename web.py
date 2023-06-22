from flask import Flask, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)     # Creating an SQLAlchemy instance
app.app_context().push()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first= db.Column(db.String(20), unique=False, nullable=False)
    last = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=True)


@app.route("/echo",methods=['GET','POST'])
def echho():
    ec=request.args.get("echo","")
    response = "{}".format(ec)
    return "Hello echo"
	
@app.route("/home",methods=['GET','POST'])
def show():
    usershow=[]
    msg=""
    alldata = Profile.query.all()
    if request.method == 'POST':
        if request.form['find']=="Find":
            id = request.form['id']
            data = Profile.query.get(int(id))  #filter_by(first=byusername).first_or_404()
            if data == None:
                msg="ID: "+ id +" NOT FOUND"
            else:
                usershow=[data.id,data.first,data.last,data.age]
    
    return render_template("show.html",usershow=usershow,msg=msg,allusers=alldata)

@app.route("/delete", methods=['GET','POST'])
def delete():
    usershow=[]
    alldata = Profile.query.all()
    s=""
    if request.method == 'POST':
        id = request.form['id']
        user_data=Profile.query.get(int(id))
        if user_data == None:
            s="ID: " + str(id)+ " NOT FOUND FOR DELETION"
        else:
            usershow=[user_data.id,user_data.first,user_data.last,user_data.age]
            db.session.delete(user_data)
            db.session.commit()
            s="User data has been deleted for below user"
            return render_template("show.html",usershow=usershow,msg=s,allusers=alldata)
    
    return render_template("show.html",usershow=usershow,msg=s,allusers=alldata)

@app.route("/update", methods=['GET','POST'])
def update():
    alldata = Profile.query.all()
    s=""
    updated=[]
    if request.method == 'POST':
            i = request.form['id']
            data=Profile.query.get(int(i))
            if data == None:
                 s="ID: " + str(i)+ " NOT FOUND FOR UPDATE"
            else:
                    P_D=[data.id,data.first,data.last,data.age]
                    f = request.form['first']
                    l = request.form['last']
                    a = int(request.form['age'])
                    data.first=f
                    data.last=l
                    data.age=a
                    db.session.commit()
                    s="User data updated"
                    return render_template("update.html",status=s,UD=data,PD=P_D)
    
    return render_template("update.html",status=s,UD=updated,PD=updated)

@app.route("/create",methods = ['GET', 'POST'])
def user():
    s=""
    if request.method == 'POST':
        f = request.form['first']
        l = request.form['last']
        a = int(request.form['age'])
        user_data=Profile(first=f,last=l,age=a)
        db.session.add(user_data)
        db.session.commit()
        s="User created"
        return render_template("user.html",status=s)
    else:
        return render_template("user.html",status=s)
    
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'File uploaded successfully'
   return render_template('file.html')

if __name__ == "__main__":
    app.run(debug=True)
    
