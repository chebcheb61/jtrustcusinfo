from flask import Flask, render_template, request, redirect, url_for, flash
from pusher import Pusher
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Clists1234@database-1.cukrhbgepqax.ap-southeast-1.rds.amazonaws.com/jtrust'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    
# configure pusher object
pusher = Pusher(
    app_id='1208042',
    key='2690251fcfe4d024df15',
    secret='538573ba34fd5e79e74c',
    cluster='ap1',
    ssl=True)
    

ROWS_PER_PAGE = 5        
@app.route('/')
@app.route('/index')
def Index():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    all_data = Data.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    if q: 
        all_data = Data.query.filter(or_(Data.cusSeg.ilike(q), Data.rmId.ilike(q), Data.cif.ilike(q), Data.accNum.ilike(q), Data.cusName.ilike(q), Data.minOtt.ilike(q), Data.comPerOtt.ilike(q),Data.cabFee.ilike(q), Data.minItt.ilike(q),Data.comPerItt.ilike(q),Data.maxItt.ilike(q))).paginate(page=1, per_page=ROWS_PER_PAGE)

    return render_template("index.html", employees = all_data)
        



#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('accNum'))

        my_data.cusSeg = request.form['cusSeg']
        my_data.rmId = request.form['rmId']
        my_data.cif = request.form['cif']
        my_data.accNum = request.form['accNum']
        my_data.cusName = request.form['cusName']
        my_data.minOtt = request.form['minOtt']
        my_data.comPerOtt = request.form['comPerOtt']
        my_data.minItt = request.form['minItt']
        my_data.comPerItt = request.form['comPerItt']
        my_data.maxItt = request.form['maxItt']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<accNum>/', methods = ['GET', 'POST'])
def delete(accNum):
    my_data = Data.query.get(accNum)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        cusSeg = request.form['cusSeg']
        rmId = request.form['rmId']
        cif = request.form['cif']
        accNum = request.form['accNum']
        cusName = request.form['cusName']
        minOtt = request.form['minOtt']
        comPerOtt = request.form['comPerOtt']
        cabFee = request.form['cabFee']
        minItt = request.form['minItt']
        comPerItt = request.form['comPerItt']
        maxItt = request.form['maxItt']


        my_data = Data(cusSeg, rmId, cif, accNum, cusName, minOtt, comPerOtt, cabFee, minItt, comPerItt, maxItt)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))







#Creating model table for our CRUD database
class Data(db.Model):
    '''id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))'''

    cusSeg = db.Column(db.String(100))
    rmId = db.Column(db.String(100))
    cif = db.Column(db.String(100))
    accNum = db.Column(db.Integer, primary_key = True)
    cusName = db.Column(db.String(100))
    minOtt = db.Column(db.Float)
    comPerOtt = db.Column(db.Float)
    cabFee = db.Column(db.Float)
    minItt = db.Column(db.Float)
    comPerItt = db.Column(db.Float)
    maxItt = db.Column(db.Float)  

    def __init__(self, cusSeg, rmId, cif, accNum, cusName, minOtt, comPerOtt, cabFee, minItt, comPerItt, maxItt):
    #def __init__(self, name, email, phone):

        '''self.name = name
        self.email = email
        self.phone = phone'''

        self.cusSeg = cusSeg
        self.rmId = rmId
        self.cif = cif
        self.accNum = accNum
        self.cusName = cusName
        self.minOtt = minOtt
        self.comPerOtt = comPerOtt
        self.cabFee = cabFee
        self.minItt = minItt
        self.comPerItt = comPerItt
        self.maxItt = maxItt



        
if __name__ == '__main__':
        app.run(debug=True)
