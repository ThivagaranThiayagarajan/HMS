# from application import app
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Float
# from flask_marshmallow import Marshmallow
# # database models
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# #

# class User(db.Model):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     firstname = Column(String)
#     lastname = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)


# class Patient(db.Model):
#     __tablename__ = 'patients'
#     patient_id = Column(Integer, primary_key=True)
#     patient_name = Column(String)
#     patient_age = Column(Integer)
#     date = Column(String)
#     type_of_bed = Column(String)
#     address = Column(String)
#     state = Column(String)
#     city = Column(String)

# class Patient_Medicine(db.Model):
#     __tablename__ = 'patient_medicine'
#     pm_id = Column(Integer, primary_key=True)
#     patient_id = Column(Integer)
#     medicine_id = Column(Integer)
#     quantity_issued = Column(Integer)

# class Medicine(db.Model):
#     __tablename__ = 'medicine'
#     medicine_id = Column(Integer, primary_key=True)
#     medicine_name = Column(String)
#     quantity_available = Column(Integer)
#     rate = Column(Integer)

# class Diagnostic(db.Model):
#     __tablename__ = 'diagnostic'
#     diagnostic_id = Column(Integer, primary_key=True)
#     name_of_the_test = Column(String)
#     amount = Column(Integer)

# class PatientDiagnostic(db.Model):
#     __tablename__ = 'patientdiagnostic'
#     pd_id = Column(Integer, primary_key=True)
#     patient_id = Column(Integer)
#     diagnostic_id = Column(Integer)


# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'firstname', 'lastname', 'email', 'password')


# class PatientSchema(ma.Schema):
#     class Meta:
#         fields = ('patient_id', 'patient_name', 'patient_age', 'date', 'type_of_bed', 'address', 'state', 'city')

# class MedicineSchema(ma.Schema):
#     class Meta:
#         fields = ('medicine_id', 'medicine_name', 'quantity_available', 'rate')

# class Patient_MedicineSchema(ma.Schema):
#     class Meta:
#         fields = ('patient_id', 'medicine_id', 'quantity_issued')

# class DiagnosticSchema(ma.Schema):
#     class Meta:
#         fields = ('diagnostic_id', 'name_of_the_test', 'amount')

# class PatientDiagnosticSchema(ma.Schema):
#     class Meta:
#         fields = ('pd_id', 'patient_id', 'diagnostic_id')


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# patient_schema = PatientSchema()
# patients_schema = PatientSchema(many=True)

# medicine_schema = MedicineSchema()
# medicines_schema = MedicineSchema(many=True)

# patient_medicine_schema = Patient_MedicineSchema()
# patient_medicines_schema = Patient_MedicineSchema(many=True)

# diagnostic_schema = DiagnosticSchema()
# diagnostics_schema = DiagnosticSchema(many=True)

# patient_diagnosticSchema = PatientDiagnosticSchema()
# patients_diagnosticSchema = PatientDiagnosticSchema(many=True)