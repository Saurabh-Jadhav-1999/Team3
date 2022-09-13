import { Button } from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";
import style from "./SearchButton.module.css";
import { useSelector, useDispatch } from "react-redux";
import { fetchHotelList } from "./../../slices/searchSlice";

export const SearchButton = () => {
  const dispatch = useDispatch();
  const location = useSelector((state) => state.search.location);
  const checkIn = useSelector((state) => state.search.checkIn);
  const checkOut = useSelector((state) => state.search.checkOut);
  const adultcount=useSelector(state=>state.search.totalAdult);
  const childcount=useSelector(state=>state.search.totalChild);
  const navigate = useNavigate();

  const navigateTo = () => {
    navigate('/search-hotels')
  }
  return (
    <>
      <Button
        className={style.searchBtn}
        variant="contained"
        size="large"
        onClick={(e) => {
          dispatch(fetchHotelList({ location, checkIn, checkOut,adultcount,childcount }));
          navigateTo();
        }}
      >
        Search
      </Button>
    </>
  );
}
