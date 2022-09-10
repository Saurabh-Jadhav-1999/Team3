
from backend import db, app  
from backend.models.HotelModel import SearchHistory
from backend.services.UserServices import getPerticularUser
from backend.services.HotelServices import getPerticularHotelById
from cerberus import Validator
import datetime

# method to validate input data for history table
def validateHistoryData(data):
    historySchema = {
        "searchHistory_id": {"type":"integer", "required":True},
        "ip": {"type":"string", "required":True},
        "location": {"type":"string", "required":True},
        "search_date": {"type":"date", "required":True},
        "number_times": {"type":"integer", "required":True},
        "user_id": {"type":"integer", "required":True},
        "hotel_id": {"type":"integer", "required":True}
    }

    historyValidator = Validator(historySchema)
    result = historyValidator.validate(data)
    return historyValidator

# add new history in history model
def addHistory(data):
    #get user
    user = getPerticularUser(data['user_id'])
    #get hotel 
    hotel = getPerticularHotelById(data['hotel_id'])
    #create new history instance
    searchHistory = SearchHistory(ip=data['ip'],location=data['location'],search_date=datetime.datetime.utcnow(),number_times=data['number_times'],owner=user,reviewed=hotel)  
    db.session.add(searchHistory)
    db.session.commit()
    return searchHistory

# method to get all the history 
def getHistory():
    return SearchHistory.query.all()