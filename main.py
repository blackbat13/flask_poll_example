from datetime import timedelta, timezone

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "adfk3l5k3lkasdlk5l34wka5l"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///polls.db"

db = SQLAlchemy(app)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200))
    pub_date = db.Column("date published", db.DateTime)
    choices = db.relationship("Choice", backref="question", cascade="all, delete")

    def __str__(self):
        return self.question_text

    def was_published_recently(self) -> bool:
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now


class Choice(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    choice_text = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.choice_text


@app.route("/")
def index():
    latest_question_list = Question.query.order_by(Question.pub_date.desc()).all()
    return render_template("index.html", latest_question_list=latest_question_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
