from flask import Flask, jsonify, request
from config import db
from config import app, jwt
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from model import Patient, Doctor, Appointment
from serial import pat_schema, pats_schema, doc_schema, docs_schema, appoint_schema, appoints_schema


@app.route('/login', methods=['POST'])
def login_required():
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        # Validate username and password
        if username != 'joyce' or password != 'joy@2727':
            raise Exception('Invalid username or password')

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


@app.route('/patient', methods=['POST'])
def add_patient():
    try:
        name = request.json.get('name')
        age = request.json.get('age')
        mobile_no = request.json.get('mobile_no')
        address = request.json.get('address')

        # Check if all required fields are present
        if not all([name, age, mobile_no, address]):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if mobile_no is a string and has 10 digits
        if not (isinstance(mobile_no, str) and len(mobile_no) == 10 and mobile_no.isdigit()):
            return jsonify({"error": "Invalid mobile number"}), 400

        # Check if patient with the same name already exists
        existing_patient = Patient.query.filter_by(name=name).first()
        if existing_patient:
            return jsonify({'error': 'Patient already exists'}), 409

        # Create a new patient
        new_patient = Patient(name=name, age=age, mobile_no=mobile_no, address=address)
        db.session.add(new_patient)
        db.session.commit()

        return pat_schema.jsonify(new_patient), 201
    except (KeyError, ValueError) as e:
        return jsonify({"error": "Invalid request format"}), 400


# Route for retrieving details of a specific patient
@app.route('/patient/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    return pat_schema.jsonify(patient)


@app.route('/patient/details', methods=['GET'])
def get_details():
    patient_details = Patient.query.all()
    sto = pats_schema.dump(patient_details)
    return jsonify(sto)


@app.route('/patient/<int:id>', methods=['PUT'])
def update_patient(id):
    name = request.json.get('name')
    age = request.json.get('age')
    mobile_no = request.json.get('mobile_no')
    address = request.json.get('address')

    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Update patient attributes
    if name is not None:
        patient.name = name
    if age is not None:
        patient.age = age
    if mobile_no is not None:
        patient.mobile_no = mobile_no
    if address is not None:
        patient.address = address

    db.session.commit()

    return pat_schema.jsonify({'message': 'Patient updated successfully'})


# Route for deleting a patient
@app.route('/patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    db.session.delete(patient)
    db.session.commit()
    return pat_schema.jsonify({'message': 'Patient deleted successfully'}),404


@app.route('/doctor', methods=['POST'])
def create_doctor():
    try:
        d_name = request.json['d_name']
        specialist = request.json['specialist']
        visiting_hours = request.json['visiting_hours']

    except KeyError:
        return jsonify({'error': 'Missing required fields (d_name, specialist, visiting_hours)'}), 400

    existing_doctor = Doctor.query.filter_by(d_name=d_name).first()
    if existing_doctor:
        return jsonify({'error': 'Patient already exists'}), 409

    # Create a new Doctor object
    new_doctor = Doctor(d_name, specialist, visiting_hours)
    db.session.add(new_doctor)
    db.session.commit()

    return doc_schema.jsonify(new_doctor), 201


@app.route('/doctor', methods=['GET'])
def get_patient_details():
    doctor_details = Doctor.query.all()
    all_doctors = docs_schema.dump(doctor_details)
    return jsonify(all_doctors)


@app.route('/doctor/<int:doctor_id>', methods=['PUT'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor:
        data = request.json
        doctor.d_name = data.get('d_name', doctor.name)
        doctor.specialist = data.get('specialist', doctor.specialist)
        doctor.visiting_hours = data.get('visiting_hours', doctor.visiting_hours)
        db.session.commit()
        return doc_schema.jsonify({'message': 'Doctor updated successfully'})
    else:
        return jsonify({'error': 'Doctor not found'}), 404


@app.route('/doctor/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return doc_schema.jsonify({'message': 'Doctor deleted successfully'})
    else:
        return jsonify({'error': 'Doctor not found'}), 404


@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    reason_visit = data.get('reason_visit')
    appointment_fix = data.get('appointment_fix')

    if not all([doctor_id, patient_id, reason_visit,appointment_fix]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        reason_visit=reason_visit,
        appointment_fix=appointment_fix)
    # Check if patient with the same appointments already exists
    existing_appoint = Appointment.query.filter_by(appointment_fix=appointment_fix).first()
    if existing_appoint:
        return jsonify({'error': 'appointment booked already'}), 409

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully'}), 201


# Route for retrieving details of a specific appointment
@app.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    appointment_data = {
        'id': appointment.id,
        'doctor_id': appointment.doctor_id,
        'patient_id': appointment.patient_id,
        'reason_visit': appointment.reason_visit,
        'appointment_fix': appointment.appointment_fix,
        'appointment_time': appointment.appointment_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    return appoint_schema.jsonify(appointment_data)


# Route for updating an appointment
@app.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.json
    appointment.reason_visit = data.get('reason_visit', appointment.reason_visit)
    db.session.commit()

    return jsonify({'message': 'Appointment updated successfully'})


# Route for deleting an appointment
@app.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment deleted successfully'})


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
