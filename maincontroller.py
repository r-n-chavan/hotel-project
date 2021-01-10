from hotel_web_application import accountscontroller,hotelcontroller,menucontroller,roomcontroller,logincontroller,customer_controller
from hotel_web_application.config import app,db


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)