import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
  hotelId: "",
  hotel_name:"",
  noOfPassengers: "",
  totalCost: 0,
  status:"",
  city_name: "",
  allow_to_bring_pet: "",
  lunch_per_person_per_day: "",
  parking: "",
  room_type: "",
  room_type_cost: 0,
  finalbooking: [],
  // extra_pillow: "",
};

export const finalBookNow = createAsyncThunk(
  "bookNowRoom/finalBookNow",
  async (
    { checkin, checkout, adultcount, childcount, hotelid, totalcost },
    thunkAPI
  ) => {
    try {
      const config = {
        headers: {
          "x-auth-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImpvaG5kb2VAZ21haWwuY29tIiwidXNlcl9pZCI6MX0.8ZJAWETPMMyxQygChY7t3d1GdrxGo16UQ_MkF6D-OGg",
        },
      };
      const cost=parseInt(totalcost);
      const hid=parseInt(hotelid);
      const acnt=parseInt(adultcount);
      const ccnt=parseInt(childcount);
      const bodyParameters = {
        check_in_date: `${checkin}`,
        check_out_date: `${checkout}`,
        adult_count: acnt,
        child_count: ccnt,
        hotel_id: hid,
        exclusive_room_count: 1,
        economy_room_count: 0,
        double_room_count: 0,
        premium_room_count: 0,
        total_cost: cost,
      };

     
      return axios
        .post(
          "https://hotelbooking-backend.herokuapp.com/booking",
          bodyParameters,
          config
        )
        .then((response) => {
    
          return response.data;
        });
    } catch (error) {
      return error;
    }
  }
);

export const bookNowSlice = createSlice({
  name: "bookNowRoom",
  initialState: initialState,
  reducers: {
    setHotelId: (state = initialState, action) => {
      state.hotelId = action.payload;
    },
    setNoOfPassengers: (state = initialState, action) => {
      state.noOfPassengers = action.payload;
    },
    setTotalCost: (state = initialState, action) => {
      state.totalCost = action.payload;
    },
   
    setCityName: (state = initialState, action) => {
      state.city_name = action.payload;
    },
    setAllowToBringPet: (state = initialState, action) => {
      state.allow_to_bring_pet = parseInt(action.payload);
      state.totalCost += parseInt(action.payload);
    },
    setLunchPerPersonPerDay: (state = initialState, action) => {
      state.lunch_per_person_per_day = parseInt(action.payload);
      state.totalCost += parseInt(action.payload);
    },
    setParking: (state = initialState, action) => {
      state.parking = parseInt(action.payload);
      state.totalCost += parseInt(action.payload);
    },
    unsetAllowToBringPet: (state = initialState, action) => {
      state.allow_to_bring_pet = 0;
      state.totalCost -= parseInt(action.payload);
    },
    unsetLunchPerPersonPerDay: (state = initialState, action) => {
      state.lunch_per_person_per_day = 0;
      state.totalCost -= parseInt(action.payload);
    },
    unsetParking: (state = initialState, action) => {
      state.parking = 0;
      state.totalCost -= parseInt(action.payload);
    },
    setRoomType: (state = initialState, action) => {
      state.room_type = action.payload;
    },
    setRoomTypeCost: (state = initialState, action) => {
      state.room_type_cost = parseInt(action.payload.bp);
      state.totalCost = action.payload.bp*action.payload.Difference_In_Days;
    },
  },
  extraReducers: {
    [finalBookNow.pending]: (state, action) => {
      state.status = "loading";

    },
    [finalBookNow.rejected]: (state, action) => {
      state.status = "rejected";

    },
    
    [finalBookNow.fulfilled]: (state, action) => {
      state.status = "succeeded";
      state.finalbooking = action.payload;
    
    },
   
  },
});

export const {
  setHotelId,
 
  setNoOfPassengers,
  setAllowToBringPet,
  setExtraPillow,
  setLunchPerPersonPerDay,
  setCityName,
  setParking,
  setTotalCost,
  unsetAllowToBringPet,
  unsetLunchPerPersonPerDay,
  unsetParking,
  setRoomTypeCost,
  setRoomType,
} = bookNowSlice.actions;
export default bookNowSlice.reducer;
