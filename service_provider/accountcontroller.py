from hotel_web_application.model import Account,app,db
import json

@app.route('/api/account/',methods=['GET'])
def get_all_accounts():
    accounts = Account.query.all()
    all_accounts_dict = []
    for acc in accounts:
        account_dict = {
            "account_id" : acc.id,
            "account_type": acc.type,
            "account_balance":acc.balance
        }
        all_accounts_dict.append(account_dict)
    return json.dumps(all_accounts_dict)

from flask import request

@app.route("/api/new/account/",methods=['POST'])
def add_new_account():
    reqbody = request.get_json()
    errors = {}
    if not reqbody:
        return json.dumps({"error" : "Request body with params [id/type/balanace/] required"})

    id = reqbody.get('id')
    if not id:
        errors["ID"] = "Account id required"
    else:
        account = Account.query.filter_by(id=id).first()
        if account:
            return json.dumps({"error" : "Account already exist..!"})
        else:
            type = reqbody.get('type')
            bal = reqbody.get('balance')
            if not type:
                errors["TYPE"] = "Account Type Required"
            if not bal or bal<0:
                errors['BALANCE'] = "INvalid Balance "
            if errors:
                return json.dumps({"error" : errors})
            else:
                acc = Account(id=id,balance=bal,type=type)
                db.session.add(acc)
                db.session.commit()
                return json.dumps({"success" : "Account created Successfully....!"})
    return json.dumps({"error" : errors})

@app.route("/account/status/<int:accid>")
def check_account_balance(accid):
    acc = Account.query.filter_by(id=accid).first()
    if acc:
        return json.dumps({"Balance is " : acc.balance})
    else:
        return json.dumps({"ERROR" : "Invalid Account Number"})

#end user -- request --> expected response page -->
#application -- request -- expected - serialized data -->

if __name__ == '__main__':
    app.run(debug=True)