from hotel_web_application.model import *
import random

#logincontroller --> admin/admin123 -->             add/remove/update/get/getall -- rooms/menus/hotel/account
#roomcontroller  - crud
#accountcontroller  - crud
#hotelcontroller  -- crud
#menucontroller  -- crud
def dummy_hotels(n):
    hotellist = []
    hotels = Hotel.query.all()
    startrange = 1111
    if hotels:
        startrange = hotels[-1].id+1
    for item in range(n):
        ac=Account(id=111+item, type='Current', balance=random.randint(1000,10000))
        db.session.add(ac)
        db.session.commit()
        print('Account Saved')

        hotel = Hotel(accno=ac.id,id=startrange+item, name=f'Sayaji{item}', address=f'Pune,wakad {item}', contact=f'020-1223445{item}', website='www.sayaji.com')
        hotellist.append(hotel)
    return hotellist

TYPES = ['STANDARD','DELUX','NORMAL','PREMIUM']

def dummy_rooms():
    count = 1
    for item in range(10):
        room = Room(id=count, type=TYPES[random.randint(0,3)], charge=random.randint(1000,5000), status='A', hotelid=1111)
        db.session.add(room)
        db.session.commit()
        count = count + 1

    for item in range(7):
        room = Room(id=count, type=TYPES[random.randint(0,3)], charge=random.randint(1000,5000), status='A', hotelid=1112)
        db.session.add(room)
        db.session.commit()
        count = count + 1

    for item in range(12):
        room = Room(id=count, type=TYPES[random.randint(0,3)], charge=random.randint(1000,5000), status='A', hotelid=1113)
        db.session.add(room)
        db.session.commit()
        count = count + 1

#Hotel(id=1111,name='Sayaji',address='Pune,wakad',contact='020-12234453',website='www.sayaji.com')

def generate_hotels():
    db.session.add_all(dummy_hotels(3))
    db.session.commit()
    print('Hotels Added')

def generate_rooms():
    dummy_rooms()
    print('Rooms Added..')

def generate_menus():
    menulist = []
    count = 1
    for item in range(random.randint(5,20)):
        m1 = Menu(id=count,name=f'XXXXX{random.randint(1,999)}',price=random.randint(350,750),hotelid=1111)
        count = count+1
        menulist.append(m1)

    for item in range(random.randint(5,20)):
        m1 = Menu(id=count, name=f'YYYYYY{random.randint(1,999)}', price=random.randint(350,1000), hotelid=1112)
        count = count + 1
        menulist.append(m1)

    for item in range(random.randint(5,20)):
        m1 = Menu(id=count, name=f'ZZZZZ{random.randint(1,999)}', price=random.randint(350,950), hotelid=1113)
        count = count + 1
        menulist.append(m1)

    db.session.add_all(menulist)
    db.session.commit()
    print('Menu added into hotels..')

import time
if __name__ == '__main__':
    db.drop_all()
    print('Removed Existing Data')
    time.sleep(2)
    db.create_all()
    print('Created New Tables')

    generate_hotels()
    print('Hotels Generated')

    dummy_rooms()
    print('Rooms Added ')
    generate_menus()
