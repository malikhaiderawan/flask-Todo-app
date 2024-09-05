
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



#class for Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,title, desc):

        self.title = title
        self.desc = desc

    def __repr__(self) -> str:
        return f'{self.title}-{self.desc}'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def Todo_show():
    if request.method=="POST":

        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('home.html',allTodo=allTodo)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get(id)
    if todo is None:
        return "Todo not found", 404

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    return render_template('update.html', get=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')






if __name__ == '__main__':
    app.run(debug=True)
