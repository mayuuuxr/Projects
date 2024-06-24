from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    sr_no= db.Column(db.Integer,primary_key = True)
    Title= db.Column(db.String(200),nullable = False)
    Desc = db.Column(db.String(500),nullable = False)
    Time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
      return f"{self.sr_no} - {self.Title}"
    

@app.route("/",methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
        todo_title = (request.form['Title'])
        todo_desc = (request.form['Desc'])
        data = Todo(Title = todo_title,Desc = todo_desc)
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    alltodo = Todo.query.all()

    return render_template('index.html',alltodo = alltodo)

@app.route('/update/<int:sr_no>',methods = ['GET','POST'])
def update(sr_no):
    if request.method=='POST':
        todo_Title = (request.form['Title'])
        todo_Desc = (request.form['Desc'])
        data = Todo.query.filter_by(sr_no = sr_no).first()
        data.Title = todo_Title
        data.Desc = todo_Desc
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sr_no = sr_no).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    todo = Todo.query.filter_by(sr_no = sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ =="__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)