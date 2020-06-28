from application import app
from flask import render_template,request, json, Response, redirect, flash, url_for, session, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from datetime import date
import random


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    patient1 = Patient(patient_id=1,
                    patient_name='Kirithiga',
                     patient_age=32,
                     date=str(date.today()),
                     type_of_bed="",
                     address="chrompet",
                     state="tamilnadu",
                     city="chennai")

    print('Database seeded1!')

    db.session.add(patient1)

    test_user = User(firstname='William',
                     lastname='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    
    print('Database seeded2!')

    medicine1 =Medicine(medicine_id=10929769162,
                        medicine_name="Fioricet",
                        quantity_available=100,
                        rate=20)
    db.session.add(medicine1)
    
    patient_medicine1 = Patient_Medicine(patient_id=1,
                                            medicine_id=10929769162,
                                            quantity_issued=10)
    
    
    db.session.add(patient_medicine1)
    db.session.commit()
    


@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")



@app.route('/patients', methods=['GET'])
def patients():
    patients_list = Patient.query.all()
    result = patients_schema.dump(patients_list)
    return jsonify(result.data)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        user = User(firstname=firstname, lastname=lastname, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


@app.route('/logincheck', methods=['POST'])
def logincheck():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        # jsonify(message="Login succeeded!", access_token=access_token)
        return render_template("index.html")
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/logout')
def logout():
    return redirect(url_for("login"))


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your patient API password is " + user.password,
                      sender="admin@patient-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401



@app.route('/patient_details/<int:patient_id>')
def patient_details(patient_id:int):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        result = patient_schema.dump(patient)
        return jsonify(result)
    else:
        return jsonify(message="That patient does not exist"), 404

@app.route('/add_patient', methods=["POST"])
def add_patient():
    patient_name = request.form['patient_name']
    test = Patient.query.filter_by(patient_name=patient_name).first()
    if test:
        return jsonify(message="There is already a patient by that name"), 409
    else:
        patient_id = int(request.form['patient_id'])
        patient_age = int(request.form['patient_age'])
        date = str(request.form['date'])
        type_of_bed = request.form['type_of_bed']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']

        new_patient = Patient(patient_id=patient_id, patient_name=patient_name, patient_age=patient_age, date=date, type_of_bed=type_of_bed, address=address, state=state, city=city)

        db.session.add(new_patient)
        db.session.commit()
        return jsonify(message="You added a patient"), 201



@app.route('/update_patient', methods=['POST'])
def update_patient():
    patient_id = int(request.form['patient_id'])
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        patient.patient_name = request.form['patient_name']
        patient.patient_age = int(request.form['patient_age'])
        patient.type_of_bed = request.form['type_of_bed']
        patient.address = request.form['address']
        patient.state = request.form['state']
        patient.city = request.form['city']
        
        db.session.commit()
        return jsonify(message="You updated a patient"), 202
    else:
        return jsonify(message="That patient does not exists"), 404


@app.route('/delete_patient/', methods=['POST'])
def delete_patient():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify(message="You deleted the patient successfully!!"), 202
    else:
        return jsonify(message="The patient does not exist"), 404

@app.route('/view_patient_screen/', methods=['POST'])
def view_patient_screen():
    patient =  Patient.query.all()
    if patient:
        return render_template("view_patient_screen.html", patient=patient)
    else:
        return jsonify(message="The patient does not exist"), 404


@app.route('/search_patient', methods=['POST'])
def search_patient():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        return render_template("search_patient.html", patient=patient)
    else:
        return jsonify(message="The patient does not exist"), 404


@app.route('/pharmacist_search_patient', methods=['POST'])
def pharmacist_search_patient():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    medicine_issued_for_patient = Patient_Medicine.query.filter_by(patient_id=patient_id).first()
    medicine_list = Medicine.query.all()
    for medicine in medicine_list:
        if medicine.medicine_id == medicine_issued_for_patient.medicine_id:
            rate = medicine.rate
            medicine_name = medicine.medicine_name
    if patient:
        return render_template("pharmacist_search_patient.html", patient=patient, medicine_issued_for_patient=medicine_issued_for_patient, rate=rate, medicine_name=medicine_name)
    else:
        return jsonify(message="The patient does not exist"), 404




        



# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True)
    patient_name = Column(String)
    patient_age = Column(Integer)
    date = Column(String)
    type_of_bed = Column(String)
    address = Column(String)
    state = Column(String)
    city = Column(String)

class Patient_Medicine(db.Model):
    __tablename__ = 'patient_medicine'
    patient_id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer)
    quantity_issued = Column(Integer)

class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicine_id = Column(Integer, primary_key=True)
    medicine_name = Column(String)
    quantity_available = Column(Integer)
    rate = Column(Integer)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'email', 'password')


class PatientSchema(ma.Schema):
    class Meta:
        fields = ('patient_id', 'patient_name', 'patient_age', 'date', 'type_of_bed', 'address', 'state', 'city')

class MedicineSchema(ma.Schema):
    class Meta:
        fields = ('medicine_id', 'medicine_name', 'quantity_available', 'rate')

class Patient_MedicineSchema(ma.Schema):
    class Meta:
        fields = ('patient_id', 'medicine_id', 'quantity_issued')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

medicine_schema = MedicineSchema()
medicines_schema = MedicineSchema(many=True)

patient_medicine_schema = Patient_MedicineSchema()
patient_medicines_schema = Patient_MedicineSchema(many=True)



if __name__ == '__main__':
    app.run()

