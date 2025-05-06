from flask import Flask, jsonify, request
from config import config
from models import User, db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/students', methods=['GET'])
def get_students():
    students = User.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = User(
        name=data['name'],
        grade=data['grade'],
        subject=data['subject'],
        marks=data['marks']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = User.query.get_or_404(student_id)
    return jsonify(student.to_dict())

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = User.query.get_or_404(student_id)
    student.name = data['name']
    student.grade = data['grade']
    student.subject = data['subject']
    student.marks = data['marks']
    db.session.commit()
    return jsonify({
        "message": "Student updated successfully",
        "student": student.to_dict()
    }), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = User.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify(message='Student deleted successfully'), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
