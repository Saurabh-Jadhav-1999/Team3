import {configureStore} from '@reduxjs/toolkit'
import searchReducer from './../slices/searchSlice';
import getHotelDetailsReducer from './../slices/getHotelDetailsSlice'
export const store=configureStore({

    reducer:{
        search:searchReducer,
        getHotelDetails:getHotelDetailsReducer,
    }
})