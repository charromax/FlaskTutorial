import flask
from flask import request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(200), nullable= False)
    completed = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default= datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'POST':
        newTask = Todo(content= request.form['content'])

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'Insert failed!'
    else:
        tasks = Todo.query.order_by(Todo.date_added).all()
        return render_template('index.html', tasks = tasks)

if __name__ == "__main__":
    app.run()