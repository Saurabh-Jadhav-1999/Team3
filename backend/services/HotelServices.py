from importlib.metadata import requires
from backend.models.HotelModel import Hotel
from backend import db, app
from cerberus import Validator

# validation schema for hotel 
hotel_schema = {
    "hotel_name": {"type":"string", "required":True},
    "hotel_profile_picture":{"type":"string"},
    "hotel_images": {"type":"list", "required":True},
    "description":{"type":"string", "required":True},
    "city":{"type":"string", "required":True},
    "state":{"type":"string", "required":True},
    "country":{"type":"string", "required":True},
    "pincode":{"type":"integer", "required":True},
    "landmark":{"type":"string", "required":False},
    "address":{"type":"string", "required":True},
    "exclusive_room_count": {"type":"integer", "required":False},
    "economy_room_count": {"type":"integer", "required":False},
    "double_room_count": {"type":"integer", "required":False},
    "premium_room_count": {"type":"integer", "required":False},
    "exclusive_room_capacity": {"type":"integer", "required":False},
    "economy_room_capacity": {"type":"integer", "required":False},
    "double_room_capacity": {"type":"integer", "required":False},
    "premium_room_capacity": {"type":"integer", "required":False},
    "exclusive_room_rate": {"type":"integer", "required":False},
    "economy_room_rate": {"type":"integer", "required":False},
    "double_room_rate": {"type":"integer", "required":False},
    "premium_room_rate": {"type":"integer", "required":False},
    "allow_pet_cost": {"type":"integer", "required":False},
    "breakfast_for_people": {"type":"integer", "required":False},
    "extra_parking_rate":{"type":"integer", "required":False},
    "extra_pillow_rate":{"type":"integer", 'required':False},
    "hotel_facalities":{
        "type":"dict",
        "required":True,
        "schema":{
        "breakfast":{"type":"boolean", "required":True},
        "dinner":{"type":"boolean", "required":True},
        "outdoor_sport":{"type":"boolean", "required":True},
        "Berbeque":{"type":"boolean", "required":True},
        "Living_room":{"type":"boolean", "required":True},
        "Room_Service":{"type":"boolean", "required":True},
        "swimming_pool":{"type":"boolean", "required":True},	
        "Spa":{"type":"boolean", "required":True}
        }
    }
}

# method to validate hotel details 
def validateHotelData(data):
    print("Data in validateHotelData:",data)
    hotelValidator = Validator(hotel_schema)
    result = hotelValidator.validate(data)
    return hotelValidator

# method to add new hotel input is validated method data 
def addNewHotel(data):
    try:
        hotel = Hotel(data)
        db.session.add(hotel)
        db.session.commit()
        return hotel
    except Exception as e:
        print(e)
        return {"error":e}

# method to get all the hotels
def getAllHotels():
    return Hotel.query.all()

# method to get particular hotel by hotel id 
def getPerticularHotelById(id):
    try:
        return Hotel.query.filter_by(hotel_id=id).first()
    except Exception as e:
        return {"error:e"}