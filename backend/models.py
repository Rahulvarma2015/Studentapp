from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable= False)
    grade = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(100), nullable = False)
    marks = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'subject': self.subject,
            'marks': self.marks,
        }