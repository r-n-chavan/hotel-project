from hotel_web_application.model import *
from flask import render_template,request,session,url_for,redirect
from hotel_web_application.dao import num
from hotel_web_application.hotelcontroller import remaining_accounts

@app.route('/login/',methods=['GET',"POST"])
def authenticate_user():
    msg = ''
    if request.method == 'POST':
        fuser = request.form['user']
        fpass = request.form['pass']
        login = Login.query.filter(Login.username==fuser,Login.password==fpass).first()
        if login:
            if login.username=='admin' and login.password=='admin123':
                session['userinfo'] = login.username
                return redirect(url_for('dashboard_page'))
            else:
                session['userinfo'] = login.username
                return redirect(url_for('hotel_booking'))
        msg = "Incorrect Username or Password!"
    return render_template('login.html',resp = msg)

@app.route('/dashboard/',methods=['GET'])
def dashboard_page():
    if 'userinfo' in session:
        if session['userinfo'] == 'admin':
            return render_template('dashboard.html',resp='', user=session['userinfo'],hotellist = Hotel.query.all(),
                               hotel = Hotel.dummy_hotel(),
                               acclist = remaining_accounts(),room = Room.dummy_room(),
                               roomlist = Room.query.all(),menu = Menu.dummy_menu(),
                               menulist = Menu.query.all(),account = Account.dummy_account(),
                               acclist2 = Account.query.all())
    return render_template('login.html', resp='')

@app.route('/logout/',methods=['GET'])
def logout():
    if 'userinfo' in session:
        session.pop('userinfo')
    return redirect(url_for('hotel_booking'))

@app.route('/hotel_booking/',methods=['GET'])
def hotel_booking():
    if 'userinfo' in session:
        if session['userinfo'] != 'admin':
            return render_template('book_hotel.html',user=session['userinfo'],hotellist=Hotel.query.all())
    return render_template('book_hotel.html', user='',hotellist=Hotel.query.all(),cust='')

@app.route('/booked/<user>')
def room_booking(user):
    if 'userinfo' in session:
        if session['userinfo'] != 'admin':
            cust = Customer.query.filter(Customer.name==user).first()
            return render_template('booking_room.html',user=cust,num=next(num),)
    return render_template('login.html', resp='')

@app.route('/booked/')
def room_empty():
    return render_template('login.html', resp='')

# if __name__ == '__main__':
#     app.run(debug=True)

