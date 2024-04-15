from config import ma


class patientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'mobile_no', 'address', 'appointments', 'add_on')


pat_schema = patientSchema()
pats_schema = patientSchema(many=True)


class doctorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'd_name', 'specialist', 'visiting_hours', 'appointments',  'date')


doc_schema = doctorSchema()
docs_schema = doctorSchema(many=True)


class appointSchema(ma.Schema):
    class Meta:
        fields = ('id', 'doctor_id', 'patient_id', 'reason_visit', 'appointment_fix', 'appointment_time',  'date')


appoint_schema = appointSchema()
appoints_schema = appointSchema(many=True)

