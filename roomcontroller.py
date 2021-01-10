from hotel_web_application.model import *
from flask import request,render_template,session
from hotel_web_application.hotelcontroller import remaining_accounts


@app.route('/room/',methods=['GET','POST'])
def save_or_update_rooms():
    if 'userinfo' in session:
   #if user:
        msg  = ''
        if request.method == 'POST':
            rid = int(request.form['rid'])
            type = request.form['rtype']
            charge = request.form['rcharge']
            status = request.form['rstatus']
            qty = request.form['rqty']
            hotelids = request.form.getlist('hotelid')
            dbroom = Room.query.filter_by(id=rid).first()
            if dbroom:
                dbroom.type = type
                dbroom.charge = charge
                dbroom.status = status
                dbroom.qty = qty
                hotellist = []
                for hotel in hotelids:
                    hotellist.append(Hotel.query.filter_by(id=hotel).first())
                dbroom.rhotelref = hotellist
                db.session.commit()
                msg = "Room Info Updated Successfully..!"
            else:
                dbroom = Room(id=rid,type=type,charge=charge,status=status,qty=qty)
                hotellist = []
                for hotel in hotelids:
                    hotellist.append(Hotel.query.filter_by(id=hotel).first())
                dbroom.rhotelref.extend(hotellist)
                db.session.add(dbroom)
                db.session.commit()
                msg = "Room Info Created Successfully...!"


        return render_template('dashboard.html', resp='addroom', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

@app.route('/room/edit/<int:rid>')
def edit_Room_info(rid):
    if 'userinfo' in session:
        room = Room.query.filter_by(id=rid).first()
        msg=''
        return render_template('dashboard.html', resp='editroom', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=room,
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

@app.route('/room/delete/<int:rid>')
def delete_Room_info(rid):
    if 'userinfo' in session:
        msg = ''
        room = Room.query.filter_by(id=rid).first()
        if room:
            db.session.delete(room)
            db.session.commit()
            msg = "Room Removed Successfully..!"
        return render_template('dashboard.html', resp='deleteroom', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

FLAG = True

@app.route('/rooms/<val>',methods=['GET'])
def toggle_room_type(val):
    if 'userinfo' in session:
        global FLAG
        msg=''
        allrooms = Room.query.all()
        if FLAG:
            if val == 'rid':
                allrooms.sort(key=lambda room : room.id,reverse =True)
            elif val == 'rtype':
                allrooms.sort(key=lambda room : room.type)
            elif val == 'rcharge':
                allrooms.sort(key=lambda room: room.charge)
            elif val == 'rstatus':
                allrooms.sort(key=lambda room: room.status)
            FLAG = False
        else:
            FLAG = True
        return render_template('dashboard.html', resp='addroom', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=allrooms,
                               roomlist=allrooms, menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

if __name__ == '__main__':
    app.run(debug=True)