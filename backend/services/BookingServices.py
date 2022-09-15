from dataclasses import fields
from itertools import count
from tabnanny import check
from typing import List
from unittest import result
from backend.models.HotelModel import Booking, booking_representation
from backend.services.HotelServices import getPerticularHotelById
from backend import db, app
from cerberus import Validator
from flask_restful import marshal_with
from sqlalchemy import func, or_, and_
from datetime import timedelta
from flask_restful import fields, marshal_with
from sqlalchemy import func

# method to validate booking data
def validateBookingData(data):
    booking_validation_schema = {
        "exclusive_room_count": {"type":"integer", "required":False},
        "economy_room_count": {"type":"integer", "required":False},
        "double_room_count": {"type":"integer", "required":False},
        "premium_room_count": {"type":"integer", "required":False},
        "check_in_date": {"type":"date", "required":True},
        "check_out_date": {"type":"date", "required":True},
        "child_count": {"type":"integer", "required":True},
        "adult_count": {"type":"integer", "required":True},
        "user_id": {"type":"integer", "required":True},
        "hotel_id": {"type":"integer", "required":True},
        "total_cost": {"type": "float", "required":True}
    }

    bookingValidator = Validator(booking_validation_schema)
    bookingValidator.allow_unknown = True
    result = bookingValidator.validate(data)
    return bookingValidator

# method to get count of booked room on perticular day for particular hotel and room type
def getAvailabilityCount(data, dte, hotel):
    from sqlalchemy import func
    print('getAvailability called')
    if data['exclusive_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.exclusive_count)).filter(Booking.hotel_id==hotel.hotel_id).filter(or_((Booking.check_in_date==dte),and_(dte>Booking.check_in_date, dte<Booking.check_out_date)))
        total = cursor.scalar()
        print(f"date:{dte} totalbooked:",total)
        return ["exclusive_count", hotel.exclusive_room_capacity]
    if data['economy_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.economy_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        print("total:",total)
        return ["economy_count", hotel.economy_room_capacity]
    if data['double_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.double_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        print("total:",total)
        return ["double_count", hotel.double_room_capacity]
    if data['premium_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.exclusive_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        print("total:",total)
        return ["premium_count", hotel.premium_room_capacity]
    return False

# representation to show the available room count of hotel
count_representation = {
    "room counts": fields.String
}
# method to convert data into count_representation form
@marshal_with(count_representation)
def showCount(data):
    return data


# method to check whether the hotel is available for that perticular checkin, checkout date by hotel_id
def checkHotelAvailability(hotel_id, hotel, check_in_date, check_out_date, adult_count, child_count):
    delta = check_out_date - check_in_date # get difference between checkout and checkin date
    availableRoomTypes = [] # to store available room types
    discount_applied_room_type = [] # to store discount applied room types

    eco_count_list = [] # to store count of economy rooms available on each day
    exclu_count_list = [] # to store count of exclusive rooms available on each day
    double_count_list = [] # to store count of double rooms available on each day
    prim_count_lsit = [] # to store count of premium rooms available on each day

    for x in range(delta.days+1):
        dte = check_in_date+timedelta(days=x)
        result1 = db.session.query(func.sum(Booking.exclusive_count).label("exclusive count"), func.sum(Booking.economy_count).label("economy count"), func.sum(Booking.double_count).label("double count"), func.sum(Booking.premium_count).label("premium count")).filter(and_(Booking.hotel_id==hotel_id,dte>=Booking.check_in_date, dte<=Booking.check_out_date)).group_by(Booking.hotel_id).all()
        if len(result1)>0:
            exclu_count_list.append(result1[0]['exclusive count'])
            eco_count_list.append(result1[0]['economy count'])
            double_count_list.append(result1[0]['double count'])
            prim_count_lsit.append(result1[0]['premium count'])
        else:
            exclu_count_list.append(0)
            eco_count_list.append(0)
            double_count_list.append(0)
            prim_count_lsit.append(0)

    # print("*"*10)
    # print("for hotel:",hotel_id)
    # print("Economy room booking for all dates:",eco_count_list)
    # print('exclusive room booking for all days:',exclu_count_list)
    # print('double room booking for all days:',double_count_list)
    # print("primium room booking for all days:", prim_count_lsit)
    # print("*"*10)

    # check and add exclusive rooms to array
    if max(exclu_count_list) < hotel.exclusive_room_count and (adult_count+child_count)<=hotel.exclusive_room_capacity:
        availableRoomTypes.append("exclusive_room")

    #check and add economy rooms to array
    if max(eco_count_list) < hotel.economy_room_count and (adult_count+child_count)<=hotel.economy_room_capacity:
        availableRoomTypes.append("economy_room")

    # check and add double rooms to array
    if max(double_count_list) < hotel.double_room_count and (adult_count+child_count)<=hotel.double_room_capacity:
        availableRoomTypes.append("double_room")

    # check and add primum room to array
    if max(prim_count_lsit) < hotel.premium_room_count and (adult_count+child_count)<=hotel.premium_room_capacity:
        availableRoomTypes.append("premium_room")

     # check if rooms are booked or not for each type
    if max(exclu_count_list) == 0:
        discount_applied_room_type.append("exclusive_room")

    if max(eco_count_list) == 0:
        discount_applied_room_type.append("economy_room")

    if max(double_count_list) == 0:
        discount_applied_room_type.append("double_room")

    if max(prim_count_lsit) == 0:
        discount_applied_room_type.append("premium_room")
    
    print("available room:", availableRoomTypes)
    print("discounted rooms:", discount_applied_room_type)

    return [availableRoomTypes, discount_applied_room_type]


def mayuriLogic(check_in_date, check_out_date, hotel_id):
    hotel = getPerticularHotelById(hotel_id)
    cursor = db.session.query(func.sum(Booking.economy_count)).filter(or_(and_(check_in_date<Booking.check_in_date,check_out_date>Booking.check_out_date) , and_(check_in_date==Booking.check_in_date,check_out_date>=Booking.check_out_date) ,and_(check_in_date==Booking.check_in_date ,check_out_date<Booking.check_out_date) ,and_(check_in_date<Booking.check_in_date ,check_out_date>Booking.check_in_date), and_(check_in_date<check_in_date ,check_out_date==Booking.check_in_date),and_(check_in_date>Booking.check_in_date ,check_in_date<Booking.check_out_date),and_(check_in_date>Booking.check_in_date ,check_in_date==Booking.check_out_date)))
    total = cursor.scalar()
    print("mayuri op:",total)

# method to check type of room booking for 
def checkRoomType(data, hotel):
    from sqlalchemy import func
    if "exclusive_room_count" in data.keys() and data['exclusive_room_count'] > 0:
        cursor = db.session.query(func.max(Booking.exclusive_count)).filter(Booking.hotel_id==hotel.hotel_id).filter(and_(Booking.check_in_date<=data['check_out_date'], Booking.check_out_date>=data['check_in_date']))
        total = cursor.scalar()
        print("total:",total)
        return ["exclusive_room", hotel.exclusive_room_capacity]
    if "economy_room_count" in data.keys() and data['economy_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.economy_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        return ["economy_room", hotel.economy_room_capacity]
    if "double_room_count" in data.keys() and data['double_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.double_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        print("total:",total)
        return ["double_room", hotel.double_room_capacity]
    if "premium_room_count" in data.keys() and data['premium_room_count'] > 0:
        cursor = db.session.query(func.sum(Booking.exclusive_count)).filter(Booking.hotel_id==hotel.hotel_id)
        total = cursor.scalar()
        print("total:",total)
        return ["premium_room", hotel.premium_room_capacity]
    return False

# method to get all the booking
def getBookings():
    return Booking.query.all()

# method to show booking details in particular format
@marshal_with(booking_representation)
def showBooking(data):
    return data


# method to add new booking
def addBooking(data, user, hotel):
    # get the user
    room_type = checkRoomType(data, hotel)

    if room_type == False:
        return {"error":"please select room type to continue"}
    # print('got the roomtype')

    if (data['adult_count']+data['child_count']) <= room_type[1]: # check if passenger count is less equal room capacity
        
        delta = data['check_out_date'] - data['check_in_date']
        
        availableResult = checkHotelAvailability(hotel.hotel_id, hotel, data['check_in_date'], data['check_out_date'], data['adult_count'], data['child_count'])
        if len(availableResult) == 0: #check if room types are availabe for dates and hotel return error if no
            print('returning error by length')
            return {"error": "The room you looking for is not available for searched dated's"}

        # combine the result of discountedList and available room type list
        availableResult = list(set(availableResult[0]).union(set(availableResult[1])))

        # if room type user searching for is not available for given detail's return error
        if room_type[0] not in availableResult:
            print("room type:",room_type[0])
            print('return error due to not available room')
            return {"error": "The room you looking for is not available for searched date's"}

        # changing room type for user response
        if "economy_room" in room_type:
            room_type[0] = "Economy Room"
        if "double_room" in room_type:
            room_type[0] = "Double Room"
        if "exclusive_room" in room_type:
            room_type[0] = "Exclusive Room"
        if "premium_room" in room_type:
            room_type[0] = "Premium Room"

        # add new booking 
        booking = Booking(check_in_date=data['check_in_date'], check_out_date=data['check_out_date'], child_count=data['child_count'], adult_count=data['adult_count'], exclusive_count=data['exclusive_room_count'], economy_count=data['economy_room_count'],double_count=data['double_room_count'],premium_count=data['premium_room_count'],bookingowner=user,hotelconcerned=hotel)
        db.session.add(booking)
        db.session.commit()
        
        # create response to send 
        response = {
            "b_id": booking.b_id,
            # "check_in_date": booking.check_in_date,
            # "check_out_date": booking.check_out_date,
            "guest_count": booking.adult_count+booking.child_count,
            "total_cost": data['total_cost'],
            "room_type": room_type[0]
            # "hotel_profile_picture": hotel.hotel_profile_picture
        }
        return response
    else:
        return {"error":"invalid guest count!"}

