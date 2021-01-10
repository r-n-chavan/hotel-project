from hotel_web_application.config import db,app

class GenericModel(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    active = db.Column('active', db.String(10),default='Yes')

menu_hotel = db.Table('menu_hotel',
        db.Column('menu_id',db.ForeignKey('menu.menu_id'),unique=False),
        db.Column('hotel_id',db.ForeignKey('hotel.hotel_id'),unique=False)
)

#Menu(id=991,name='XXXXX',price=394.45,hotelid=12)
class Menu(GenericModel):
    id = db.Column('menu_id', db.Integer(), primary_key=True)
    name = db.Column('menu_name', db.String(40),)
    price = db.Column('menu_price', db.Float(),default=350.0)
    href = db.relationship('Hotel',secondary=menu_hotel, backref=db.backref("menuref", lazy=True))

    @staticmethod
    def dummy_menu():
        return Menu(id=0, name='', price=0.0)

room_hotel = db.Table('room_hotel',
                      db.Column('room_id',db.ForeignKey('room.room_id')),
                      db.Column('hotel_id',db.ForeignKey('hotel.hotel_id'))
                      )
#Hotel(id=1111,name='Sayaji',address='Pune,wakad',contact='020-12234453',website='www.sayaji.com')
class Hotel(GenericModel):
    id = db.Column('hotel_id',db.Integer(),primary_key=True)
    name = db.Column('hotel_name',db.String(40),unique=True)
    address = db.Column('hotel_address',db.String(40))
    contact = db.Column('hotel_contact',db.String(40))
    website = db.Column('hotel_website', db.String(40))
    accno = db.Column("acc_id", db.ForeignKey("account.acc_no"), unique=True, nullable=True)
    roomref = db.relationship("Room",secondary=room_hotel,backref=db.backref("rhotelref",uselist=True))
    orderref = db.relationship("Mainorder", lazy=True, backref="ohotelref", uselist=True)

    @staticmethod
    def dummy_hotel():
        return Hotel(id=0, name='',address='', contact=0, website='')

#Room(id=1,type='STD',charge=1922.45,status='A',hotelid=)

class Room(GenericModel):
    id = db.Column('room_id', db.Integer(), primary_key=True)
    type = db.Column('room_type', db.String(40),)
    charge = db.Column('room_charge',db.Float())
    status = db.Column('room_status',db.String(30))
    qty = db.Column('room_qry',db.Integer())

    @staticmethod
    def dummy_room():
        return Room(id=0,type='',charge='',status='',qty=0)

#Account(id=111,type='Current',balance=1022.234)
class Account(GenericModel):
    id = db.Column('acc_no', db.Integer(), primary_key=True)
    type = db.Column('acc_type', db.String(40))
    balance = db.Column('acc_bal', db.Float())
    hotelref = db.relationship(Hotel,lazy=True,backref="haccref",uselist=True)
    custref = db.relationship("Customer",lazy=True,backref="caccref",uselist=True)

    @staticmethod
    def dummy_account():
        return Account(id=0,type='',balance=0.0)



class Customer(GenericModel):
    id = db.Column('cust_id', db.Integer(), primary_key=True)
    name = db.Column('cust_name', db.String(40), unique=True)
    address = db.Column('cust_address', db.String(40),)
    contact = db.Column('cust_contact',db.Integer())
    email = db.Column('cust_email',db.String(40))
    accno = db.Column("acc_id", db.ForeignKey("account.acc_no"), unique=True, nullable=True)
    orderref = db.relationship("Mainorder",lazy=True,backref="custref",uselist=True)

    @staticmethod
    def dummy_cust():
        return Customer(id=0, name='', address='', contact='', email='')

class ProcessedOrder(GenericModel):
    id = db.Column('pr_order_id', db.Integer(), primary_key=True)
    orderId = db.Column("order_id",db.ForeignKey("mainorder.order_id"),unique=False)
    menuid =  db.Column("menus",db.ForeignKey("menu.menu_id"),unique=False,nullable=True)
    roomid = db.Column("room",db.ForeignKey("room.room_id"),unique=False,nullable=True)
    finalprice = db.Column('menu_price', db.Float())
    qty = db.Column('menu_qty', db.Integer())

class Mainorder(GenericModel):
    id = db.Column('order_id', db.Integer(), primary_key=True)
    cid = db.Column('cust_id', db.ForeignKey("customer.cust_id"),nullable=False,unique=False)
    hid = db.Column('hotel_id', db.ForeignKey("hotel.hotel_id"),nullable=False,unique=False)
    billamount = db.Column('total_bill', db.Float())


class Login(GenericModel):
    username = db.Column('username', db.String(20), primary_key=True)
    password = db.Column('password', db.String(20))

# if __name__ == '__main__':
#     cust = Login.query.filter_by(username='ravindra').first()
#     db.session.delete(cust)
#     db.session.commit()
#
#     cust = Customer.query.filter_by(id=1).first()
#     db.session.delete(cust)
#     db.session.commit()

    # m = Menu(id=3333, name='Kolhapuri', price=150, hotelid=2222)
    # db.session.add(m)
    # db.session.commit()

    # db.drop_all()
    #
    # db.create_all()
    # login = Login(username="admin",password="admin123")
    # db.session.add(login)
    # db.session.commit()

    # ht = Hotel(101, 'Sayaji', 'Pune-wakad', '020-12234453', 'www.sayaji.com',None)
    #db.session.add(ht)
    #db.session.commit()

'''
Hotel Booking Service..
        Hotel
        Rooms
        Account
        Menu
        Order
        Customer
        
ALTER USER 'yourusername'@'localhost' IDENTIFIED WITH mysql_native_password BY 'youpassword';


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
'''