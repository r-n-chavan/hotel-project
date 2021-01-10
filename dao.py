
def create_hotel_booking_number():
    num = 1000
    while num:
        yield num
        num += 1

num = create_hotel_booking_number()
