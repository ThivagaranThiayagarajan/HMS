from application import app
from flask import render_template,request, json, Response, redirect, flash, url_for, session, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from datetime import date
import random,os


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

# print("begin here")


with open('application/cities.json', 'r') as cities:
    city = json.load(cities)
states=[]
cities=[]
j=0
for i in city:
    state= i['state'] 
    states.append(state)
    citi = i['name']
    cities.append(citi)
    j=j+1

states = list( dict.fromkeys(states) )        
# print (states)
# print ("End of states...")
# print (cities)

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
    patient1 = Patient(patient_id=110,
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
    
    medicine2 =Medicine(medicine_id=8296652588,
                        medicine_name="Ibuprofen",
                        quantity_available=100,
                        rate=6)
    db.session.add(medicine1)
    db.session.add(medicine2)
    
    patient_medicine1 = Patient_Medicine(pm_id=1, patient_id=110,
                                            medicine_id=10929769162,
                                            quantity_issued=10)
                                            
    
    
    db.session.add(patient_medicine1)

    diagnostic1 = Diagnostic(diagnostic_id=101, name_of_the_test='CBP', amount=2000)
    diagnostic2 = Diagnostic(diagnostic_id=102, name_of_the_test='Lipid', amount=1500)
    
    
    db.session.add(diagnostic1)
    db.session.add(diagnostic2)

    diagnostic3 = Diagnostic(diagnostic_id=103, name_of_the_test='ECG', amount=3000)
    diagnostic4 = Diagnostic(diagnostic_id=104, name_of_the_test='Echo', amount=4000)
    db.session.add(diagnostic3)
    db.session.add(diagnostic4)


    patient_diagnostic1 = PatientDiagnostic(pd_id=1, patient_id=110, diagnostic_id=101)
    db.session.add(patient_diagnostic1)
    db.session.commit()
    
    


@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("index.html")

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


@app.route('/create_patient')
def create_patient():
    return render_template("create_patient.html")

@app.route('/add_patient', methods=["POST"])
def add_patient():
    patient_name = request.form['patient_name']
    test = Patient.query.filter_by(patient_name=patient_name).first()
    if test:
        return jsonify(message="There is already a patient by that name"), 409
    else:
        patient_id = random.randint(10000,99999)
        patient_age = int(request.form['patient_age'])
        date = str(request.form['date'])
        type_of_bed = str(request.form['type_of_bed'])
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']

        new_patient = Patient(patient_id=patient_id, patient_name=patient_name, patient_age=patient_age, date=date, type_of_bed=type_of_bed, address=address, state=state, city=city)

        db.session.add(new_patient)
        db.session.commit()
        return jsonify(message="You added a patient and patient id is "+str(patient_id)), 201




@app.route('/update_patient')
def update_patient():
    return render_template("update_patient.html")



@app.route('/update_patient2', methods=['POST'])
def update_patient2():
    patient_id = int(request.form['patient_id'])
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        return render_template("update_patient3.html", patient=patient)
    else:
        flash("alert(No patient under the given ID)")
        return render_template("update_patient.html")

@app.route('/update_patient3', methods=['POST'])
def update_patient3():
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
    




@app.route('/delete_patient')
def delete_patient():
    return render_template("search_patient.html",page_value="Delete Patient",button_value="Delete")

@app.route('/delete_patient2', methods=['POST'])
def delete_patient2():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify(message="You deleted the patient successfully!!"), 202
    else:
        return jsonify(message="The patient does not exist"), 404



@app.route('/view_patient_screen')
def view_patient_screen():
    patient =  Patient.query.all()
    if patient:
        return render_template("view_patient_screen.html", patient=patient)
    else:
        return jsonify(message="The patient does not exist"), 404



@app.route('/search_patient')
def search_patient():
    return render_template("search_patient.html",page_value="Patient Search",button_value="Search")

@app.route('/display_patient', methods=['POST'])
def display_patient():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    page_value=request.form['search_button']
    print(page_value)
    if patient:
        return render_template("display_patient.html", patient=patient,page_value=page_value,patient_id=patient_id)
    else:
        return jsonify(message="The patient does not exist"), 404

##################__MEDICINE__#########################

@app.route('/pharmacist_search_patient1')
def pharmacist_search_patient1():
    return render_template("diagnostic_search_patient1.html",page_value="Pharmacists Search Patient",button_value="Search")


@app.route('/pharmacist_search_patient_bill3')
def pharmacist_search_patient_bill3():
    return render_template("diagnostic_search_patient1.html",page_value="Pharmacists Patient Bill Search",button_value="Search")

@app.route('/pharmacist_search_patient2', methods=['POST'])
def pharmacist_search_patient2():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    medicine_issued_for_patient = Patient_Medicine.query.all()
    medicine_list = Medicine.query.all()
    rate=[]
    medicine_name=[]
    if patient:
        return render_template("pharmacist_search_patient2.html", patient_id=patient_id, patient=patient, medicine_list=medicine_list, medicine_issued_for_patient=medicine_issued_for_patient, rate=rate, medicine_name=medicine_name)
    else:
        return jsonify(message="The patient does not exist"), 404


@app.route('/get_med_count', methods=['POST'])
def get_med_count():
    patient_id = int(request.form['patient_id'])
    p = Patient.query.filter_by(patient_id=patient_id).first()
    if p:
        count=int(request.form['count'])
        return render_template("get_med_details.html", count=count, patient_id=patient_id)
    else:
        return render_template("not_exist.html")


@app.route('/issue_medicine', methods=['POST'])
def issue_medicine():
    patient_id = int(request.form['patient_id'])
    p = Patient.query.filter_by(patient_id=patient_id).first()
    count = int(request.form['count'])
    print(count)
    medicine_name_list=[]
    quantity_list=[]
    if p:
        for i in range(count):
            medicine_name_list.append(request.form['medicine_name'+str(i)])
            quantity_list.append(int(request.form['quantity'+str(i)]))
        medicines = Medicine.query.all()
        patient_medicines = Patient_Medicine.query.all()
        count2=len(patient_medicines)
    
        for i in range(count):
            mn = Medicine.query.filter_by(medicine_name=medicine_name_list[i]).first()
            if mn and mn.quantity_available>=quantity_list[i]:
                print(mn.medicine_name)
                print(mn.quantity_available)
                mn.quantity_available-=quantity_list[i]
                print(mn.quantity_available)
                db.session.commit()

                pm = Patient_Medicine.query.filter_by(patient_id=patient_id).first()
                if pm:
                    print(patient_id, pm.patient_id)
                    med = Patient_Medicine.query.filter_by(medicine_id=mn.medicine_id).first()
                    if med:
                        print(mn.medicine_id, pm.medicine_id)
                        print("patient and medicine already exist")
                        med.quantity_issued+=quantity_list[i]
                        db.session.commit()
                    else:
                        print("new medicine.... old patient")
                        print(mn.medicine_id, pm.medicine_id)
                        patient_medicine1 = Patient_Medicine(pm_id=count2+1, patient_id=pm.patient_id,
                                                medicine_id=mn.medicine_id,
                                                quantity_issued=quantity_list[i])
                        db.session.add(patient_medicine1)
                        count2=count2+1
                        db.session.commit()
                else:
                    print(patient_id, pm.patient_id, mn.medicine_id)
                    print("###################")
                    print("new patient... new medicine")
                    patient_medicine1 = Patient_Medicine(pm_id=count2+1, patient_id=patient_id,
                                                medicine_id=mn.medicine_id,
                                                quantity_issued=quantity_list[i])
                    db.session.add(patient_medicine1)
                    db.session.commit()
                    count2=count2+1
            print("********************")
    else:
        print("no such patient exist")
    return render_template("issue_medicines.html", medicines=medicines, medicine_name_list=medicine_name_list, quantity_list=quantity_list)




@app.route("/medicine_list")
def medicine_list():
    medicines = Medicine.query.all()
    return render_template("medicine_list.html", medicines=medicines)


@app.route('/pharmacist_search_patient_bill4', methods=['POST'])
def pharmacist_search_patient_bill4():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    medicine_issued_for_patient = Patient_Medicine.query.all()
    medicine_list = Medicine.query.all()
    rate=[]
    medicine_name=[]
    if patient:
        return render_template("pharmacist_search_patient_bill4.html", patient=patient, medicine_list=medicine_list, medicine_issued_for_patient=medicine_issued_for_patient, rate=rate, medicine_name=medicine_name)
    else:
        return jsonify(message="The patient does not exist"), 404



##################### DIAGNOSTIC #########################


@app.route('/diagnostic_search_patient1')
def diagnostic_search_patient1():
    return render_template("diagnostic_search_patient1.html",page_value="Diagnostics Search Patient",button_value="Search")


@app.route('/diagnostic_bill_search_patient3')
def diagnostic_bill_search_patient3():
    return render_template("diagnostic_search_patient1.html",page_value="Diagnostics Patient Bill Search",button_value="Search")


@app.route('/diagnostic_search_patient2', methods=['POST'])
def diagnostic_search_patient2():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    diagnostic_for_patient = PatientDiagnostic.query.all()
    diagnostic_list = Diagnostic.query.all()

    if patient:
        return render_template("diagnostic_search_patient2.html", patient_id=patient_id, patient=patient, diagnostic_list=diagnostic_list, diagnostic_for_patient=diagnostic_for_patient)
    else:
        return jsonify(message="The patient does not exist"), 404



@app.route('/get_diagnostic_count', methods=['POST'])
def get_diagnostic_count():
    patient_id = int(request.form['patient_id'])
    p = Patient.query.filter_by(patient_id=patient_id).first()
    if p:
        count=int(request.form['count'])
        return render_template("get_diagnostic_details.html", count=count, patient_id=patient_id)
    else:
        return render_template("not_exist.html")


@app.route('/issue_diagnostic', methods=['POST'])
def issue_diagnostic():
    patient_id = int(request.form['patient_id'])
    p = Patient.query.filter_by(patient_id=patient_id).first()
    count = int(request.form['count'])
    print(count)
    test_name_list=[]
    test_to_be_conducted=[]
    amount_list=[]
    if p:
        for i in range(count):
            test_name_list.append(request.form['name_of_the_test'+str(i)])
            amount_list.append(int(request.form['amount'+str(i)]))
        diagnostics = Diagnostic.query.all()
        patient_diagnostic = PatientDiagnostic.query.all()
        count2=len(patient_diagnostic)
    
        for i in range(count):
            dn = Diagnostic.query.filter_by(name_of_the_test=test_name_list[i]).first()
            if dn:
                print(dn.name_of_the_test)
                print(dn.amount)
                db.session.commit()

                pd = PatientDiagnostic.query.filter_by(patient_id=patient_id).first()
                if pd:
                    print(patient_id, pd.patient_id)
                    dia = PatientDiagnostic.query.filter_by(diagnostic_id=dn.diagnostic_id).first()
                    if dia:
                        print(dn.diagnostic_id, pd.diagnostic_id)
                        print("Diagnosis already conducted....")
                        db.session.commit()
                    else:
                        print("Diagnosis has to be conducted")
                        print(dn.diagnostic_id, pd.diagnostic_id)
                        test_to_be_conducted.append(dn.name_of_the_test)
                        print(test_to_be_conducted)
                        patient_diagnostic1 = PatientDiagnostic(pd_id=count2+1, patient_id=pd.patient_id,
                                                diagnostic_id=dn.diagnostic_id)
                        db.session.add(patient_diagnostic1)
                        count2=count2+1
                        db.session.commit()
                else:
                    print(patient_id, pd.patient_id, dn.diagnostic_id)
                    print("###################")
                    print("new patient... new Diagnostic")
                    test_to_be_conducted.append(dn.name_of_the_test)
                    patient_diagnostic1 = PatientDiagnostic(pd_id=count2+1, patient_id=patient_id,
                                                diagnostic_id=dn.diagnostic_id)
                    db.session.add(patient_diagnostic1)
                    db.session.commit()
                    count2=count2+1
            print("********************")
    else:
        print("no such patient exist")
    print(test_to_be_conducted)
    return render_template("issue_diagnostic.html", diagnostics=diagnostics, test_to_be_conducted=test_to_be_conducted, amount_list=amount_list)


@app.route("/diagnostic_list")
def diagnostic_list():
    diagnostics = Diagnostic.query.all()
    return render_template("diagnostic_list.html", diagnostics=diagnostics)



@app.route('/diagnostic_bill_search_patient4', methods=['POST'])
def diagnostic_bill_search_patient4():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    diagnostic_for_patient = PatientDiagnostic.query.all()
    diagnostic_list = Diagnostic.query.all()
    rate=[]
    medicine_name=[]
    if patient:
        return render_template("diagnostic_bill_search_patient4.html", patient=patient, diagnostic_list=diagnostic_list, diagnostic_for_patient=diagnostic_for_patient, rate=rate, medicine_name=medicine_name)
    else:
        return jsonify(message="The patient does not exist"), 404


        


#################### BILL DETAILS ############################


@app.route('/bill_search_patient')
def bill_search_patient():
    return render_template("bill_search_patient.html")

@app.route('/patient_bill', methods=['POST'])
def patient_bill():
    patient_id=int(request.form['patient_id'])
    patient =  Patient.query.filter_by(patient_id=patient_id).first()
    
    medicine_issued_for_patient = Patient_Medicine.query.all()
    medicine_list = Medicine.query.all()

    total_medicine_bill=0
    for med in medicine_list:
        for mp in medicine_issued_for_patient:
            if med.medicine_id == mp.medicine_id:
                total_medicine_bill+=(mp.quantity_issued*med.rate)
                    
    
    diagnostic_for_patient = PatientDiagnostic.query.all()
    diagnostic_list = Diagnostic.query.all()

    total_diagnostic_bill=0
    for dia in diagnostic_list:
        for dp in diagnostic_for_patient:
            if dia.diagnostic_id == dp.diagnostic_id:
                total_diagnostic_bill+=dia.amount
    
    grand_total=total_medicine_bill+total_diagnostic_bill
    
    if patient:
        return render_template("patient_bill.html", total_medicine_bill=total_medicine_bill, total_diagnostic_bill=total_diagnostic_bill, grand_total=grand_total, medicine_issued_for_patient=medicine_issued_for_patient, medicine_list=medicine_list, patient=patient, diagnostic_list=diagnostic_list, diagnostic_for_patient=diagnostic_for_patient)
    else:
        return jsonify(message="The patient does not exist"), 404

@app.route('/edit_diagnostics')
def edit_diagnostics():
    diagnostics = Diagnostic.query.all()
    return render_template("edit_diagnostics.html",diagnostics=diagnostics)

@app.route('/edit_medicines')
def edit_medicines():
    medicines = Medicine.query.all()
    return render_template("edit_medicines.html",medicines=medicines)


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
    pm_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    medicine_id = Column(Integer)
    quantity_issued = Column(Integer)

class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicine_id = Column(Integer, primary_key=True)
    medicine_name = Column(String)
    quantity_available = Column(Integer)
    rate = Column(Integer)

class Diagnostic(db.Model):
    __tablename__ = 'diagnostic'
    diagnostic_id = Column(Integer, primary_key=True)
    name_of_the_test = Column(String)
    amount = Column(Integer)

class PatientDiagnostic(db.Model):
    __tablename__ = 'patientdiagnostic'
    pd_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    diagnostic_id = Column(Integer)


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

class DiagnosticSchema(ma.Schema):
    class Meta:
        fields = ('diagnostic_id', 'name_of_the_test', 'amount')

class PatientDiagnosticSchema(ma.Schema):
    class Meta:
        fields = ('pd_id', 'patient_id', 'diagnostic_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

medicine_schema = MedicineSchema()
medicines_schema = MedicineSchema(many=True)

patient_medicine_schema = Patient_MedicineSchema()
patient_medicines_schema = Patient_MedicineSchema(many=True)

diagnostic_schema = DiagnosticSchema()
diagnostics_schema = DiagnosticSchema(many=True)

patient_diagnosticSchema = PatientDiagnosticSchema()
patients_diagnosticSchema = PatientDiagnosticSchema(many=True)



if __name__ == '__main__':
    app.run()

