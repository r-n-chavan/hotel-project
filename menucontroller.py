from hotel_web_application.model import *
from flask import request,render_template,session
from hotel_web_application.hotelcontroller import remaining_accounts

@app.route('/menu/',methods=['GET','POST'])
def save_or_update_menu():
    if 'userinfo' in session:
        msg  = ''
        if request.method == 'POST':
            menuid = int(request.form['menuid'])
            menuname = request.form['menuname']
            menuprice = request.form['menuprice']
            menuhotels = request.form.getlist('menuhotels')
            dbmenu = Menu.query.filter_by(id=menuid).first()
            if dbmenu:
                dbmenu.type = menuid
                dbmenu.name = menuname
                dbmenu.price = menuprice
                if menuhotels:
                    hotellist = []
                    for hotel in menuhotels:
                        hotellist.append(Hotel.query.filter_by(id=hotel).first())
                    # print(dbmenu.href)
                    dbmenu.href = hotellist
                db.session.commit()
                msg = "Menu Updated Successfully..!"
            else:
                dbmenu = Menu(id=menuid,name=menuname,price=menuprice)
                hotellist = []
                if menuhotels:
                    for hotel in menuhotels:
                        hotellist.append(Hotel.query.filter_by(id=hotel).first())
                    dbmenu.href.extend(hotellist)
                db.session.add(dbmenu)
                db.session.commit()
                msg = "Menu Created Successfully...!"

        return render_template('dashboard.html', resp='addmenu', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

@app.route('/menu/edit/<int:menuid>')
def edit_menu_info(menuid):
    if 'userinfo' in session:
        msg = ''
        menu = Menu.query.filter_by(id=menuid).first()
        return render_template('dashboard.html', resp='editmenu', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=menu,
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

@app.route('/menu/delete/<int:menuid>')
def delete_menu_info(menuid):
    if 'userinfo' in session:
        msg = ''
        dbmenu = Menu.query.filter_by(id=menuid).first()
        if dbmenu:
            db.session.delete(dbmenu)
            db.session.commit()
            msg = "Menu Removed Successfully..!"
        return render_template('dashboard.html', resp='deletemenu', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')