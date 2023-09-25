from todo import db
from datetime import datetime

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), nullable = False)
    password = db.Column(db.String(32), nullable = False)

    def __repr__(self):
        return f"User(email: {self.email})"
