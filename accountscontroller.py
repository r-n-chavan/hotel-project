from hotel_web_application.model import *
from flask import request,render_template,session
from hotel_web_application.logincontroller import remaining_accounts


@app.route('/account/',methods=['GET','POST'])
def save_or_update_accounts():
    if 'userinfo' in session:
        msg  = ''
        if request.method == 'POST':
            accno = int(request.form['accid'])
            acctype = request.form['accty']
            accbal = request.form['accbal']
            dbacc = Account.query.filter_by(id=accno).first()
            if dbacc:
                dbacc.type = acctype
                dbacc.balance = accbal
                db.session.commit()
                msg = "Acccount Updated Successfully..!"

            else:
                dbacc = Account(id=accno,type=acctype,balance=accbal)
                db.session.add(dbacc)
                db.session.commit()
                msg = "Account Created Successfully...!"

        return render_template('dashboard.html', resp='addacc', msg=msg, user=session['userinfo'],
                               hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')
@app.route('/account/edit/<int:acid>')
def edit_account_info(acid):
    if 'userinfo' in session:
        return render_template('dashboard.html', resp='editacc', user=session['userinfo'], hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),acc='show active',
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.query.filter_by(id=acid).first(),
                               acclist2=Account.query.all())

    return render_template('login.html', resp='')
@app.route('/account/delete/<int:acid>')
def delete_account_info(acid):
    if 'userinfo' in session:
        msg = ''
        acc = Account.query.filter_by(id=acid).first()
        if acc:
            db.session.delete(acc)
            db.session.commit()
            msg = "Account Removed Successfully..!"
        return render_template('dashboard.html', resp='deleteacc', msg=msg, user=session['userinfo'], hotellist=Hotel.query.all(),
                               hotel=Hotel.dummy_hotel(),
                               acclist=remaining_accounts(), room=Room.dummy_room(),
                               roomlist=Room.query.all(), menu=Menu.dummy_menu(),
                               menulist=Menu.query.all(), account=Account.dummy_account(),
                               acclist2=Account.query.all())
    return render_template('login.html', resp='')

# if __name__ == '__main__':
#     app.run(debug=True)