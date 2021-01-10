from hotel_web_application.model import *
from hotel_web_application.hotelcontroller import remaining_accounts
from flask import render_template,request,redirect,url_for,session
from hotel_web_application.logincontroller import hotel_booking

@app.route('/registration/',methods=['GET','POST'])
def register_customer():
    msg = ''
    if request.method == 'POST':
        custname = request.form['custname']
        custadr = request.form['custadr']
        custcont = request.form['custcont']
        custmail = request.form['custmail']
        custaccno = request.form['custaccno']
        custpass = request.form['custpass']
        dbcust = Customer.query.filter(Customer.name == custname).first()
        dblogin = Login.query.filter_by(username=custname).first()
        if dbcust:
            if dbcust.id == int(request.form['id']):
                dbcust.address = custadr
                dbcust.contact = custcont
                dbcust.email = custmail
                dblogin.password = custpass
                if custaccno:
                    dbcust.accno = custaccno
                db.session.commit()
                msg = "Customer Data Updated Successfully..!"
                return render_template('customer_register.html',
                                       resp=msg,
                                       cust=Customer.dummy_cust(),
                                       acclist=remaining_accounts())
            msg = "Username Already Exist...!"
            return render_template('customer_register.html',
                                   resp=msg,
                                   cust=Customer.dummy_cust(),
                                   acclist=remaining_accounts())

        else:
            dbcust = Customer(name=custname, address=custadr, contact=custcont, email=custmail)
            dbcustomer = Login(username=custname, password=custpass)
            if custaccno:
                dbcust.accno = custaccno
            db.session.add_all([dbcust,dbcustomer])
            db.session.commit()
            msg = "Registration Successfully...!"
            return render_template('customer_register.html',
                                   resp=msg,
                                   cust=Customer.dummy_cust(),
                                   acclist=remaining_accounts())

    return render_template('customer_register.html',
                           cust=Customer.dummy_cust(),
                           acclist=remaining_accounts())

@app.route('/customer/edit/<user>')
def edit_customer_info(user):
    if 'userinfo' in session:
        cust = Customer.query.filter(Customer.name==user).first()
        if cust:
            return render_template('customer_register.html',
                                   cust=cust,
                                   acclist=remaining_accounts())
    return render_template('login.html', resp='')