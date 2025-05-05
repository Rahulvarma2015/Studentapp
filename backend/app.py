from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_Tt17iCnZeuUD@ep-quiet-sunset-a4w3h99s-pooler.us-east-1.aws.neon.tech/studentdb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'


with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Routes
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': student.id,
        'name': student.name,
        'grade': student.grade,
        'subject': student.subject,
        'marks': student.marks
    } for student in students])

@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'id': student.id,
        'name': student.name,
        'grade': student.grade,
        'subject': student.subject,
        'marks': student.marks
    })

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        name=data['name'],
        grade=data['grade'],
        subject=data['subject'],
        marks=data['marks']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({
        'message': 'Student added successfully',
        'id': new_student.id
    }), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    
    student.name = data['name']
    student.grade = data['grade']
    student.subject = data['subject']
    student.marks = data['marks']
    
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)