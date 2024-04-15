from config import db, app
from datetime import datetime


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(150), unique=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    add_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, age, mobile_no, address):
        self.name = name
        self.age = age
        self.mobile_no = mobile_no
        self.address = address


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(100), nullable=False)
    specialist = db.Column(db.String(100), nullable=False)
    visiting_hours = db.Column(db.String(50), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, d_name, specialist, visiting_hours,):
        self.d_name = d_name
        self.specialist = specialist
        self.visiting_hours = visiting_hours


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    reason_visit = db.Column(db.String(200), nullable=False)
    appointment_fix = db.Column(db.String(50), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, doctor_id, patient_id, reason_visit, appointment_fix):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.reason_visit = reason_visit
        self.appointment_fix = appointment_fix


with app.app_context():
 db.create_all()
