from hotel_web_application.model import *
from flask import request,render_template,session

def remaining_accounts():
    acclist = Account.query.all()
    accl = []
    for acc in acclist:
        if not acc.hotelref and not acc.custref:
            accl.append(acc)
    return accl

@app.route('/hotel/',methods=['GET','POST'])
def save_or_update_hotels():
    if 'userinfo' in session:
        msg  = ''
        if request.method == 'POST':
            hotelid = int(request.form.get('hotelid'))
            hotelname = request.form['hotelname']
            hoteladr = request.form['hoteladr']
            hotelcont = request.form['hotelcont']
            hotelwebsite = request.form['hotelwebsite']
            dbhotel = Hotel.query.filter_by(id=hotelid).first()
            if dbhotel:
                dbhotel.id = hotelid
                dbhotel.name = hotelname
                dbhotel.address = hoteladr
                dbhotel.contact = hotelcont
                dbhotel.website = hotelwebsite
                hotelaccno = request.form['hotelaccno']
                if hotelaccno:
                    dbhotel.accno = hotelaccno
                db.session.commit()
                msg = "Hotel Updated Successfully..!"
            else:
                dbhotel = Hotel(id=hotelid,name=hotelname,address=hoteladr,contact=hotelcont,website=hotelwebsite)
                hotelaccno = request.form['hotelaccno']
                # print(hotelaccno)
                if hotelaccno:
                    dbhotel.accno = hotelaccno
                db.session.add(dbhotel)
                db.session.commit()
                msg = "Hotel Created Successfully...!"

        return render_template('dashboard.html',resp='addhotel',msg=msg, user=session['userinfo'],hotellist = Hotel.query.all(),
                               hotel = Hotel.dummy_hotel(),
                               acclist = remaining_accounts(),room = Room.dummy_room(),
                               roomlist = Room.query.all(),menu = Menu.dummy_menu(),
                               menulist = Menu.query.all(),account = Account.dummy_account(),
                               acclist2 = Account.query.all())
    return render_template('login.html', resp='')

@app.route('/hotel/edit/<int:hotelid>')
def edit_hotel_info(hotelid):
    if 'userinfo' in session:
        msg=''
        hotel = Hotel.query.filter_by(id=hotelid).first()
        # print(hotel.accref.type)
        return render_template('dashboard.html', resp='edithotel', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=hotel,
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

@app.route('/hote/delete/<int:hotelid>')
def delete_hotel_info(hotelid):
    if 'userinfo' in session:
        msg = ''
        hotel = Hotel.query.filter_by(id=hotelid).first()
        if hotel:
            db.session.delete(hotel)
            db.session.commit()
            msg = "Hotel Removed Successfully..!"
        return render_template('dashboard.html', resp='deletehotel', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')
