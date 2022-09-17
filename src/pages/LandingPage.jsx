import { LandingHotelPicture } from "../components/landingHotelPicture/LandingHotelPicture";
import { FeaturedDestinations } from "../components/featuredDestinations/FeaturedDestinations";
import "react-toastify/dist/ReactToastify.css";
import { SuggestedHotels } from '../components/StaticComponents/SuggestedHotels'
import { fetchSuggestedHotels } from "../slices/suggestedHotelsSlice";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { TrendingCities } from '../components/StaticComponents/TrendingCities'
import { TravelYourPassion } from '../components/travelYourPassion/TravelYourPassion'
export const LandingPage = () => {

  const dispatch = useDispatch();
  const status = useSelector(state => state.suggestedHotels.status);
  const loginStatus = useSelector(state => state.login.token)
  const token = localStorage.getItem("token")

  useEffect(() => {
    dispatch(fetchSuggestedHotels(token))
  }, [loginStatus])


  return (
    <>
      <div>
        <LandingHotelPicture />
        <div style={{ position: "relative", marginTop: "5vh !important" }}>
          {status === "succeeded" && loginStatus !== null && <SuggestedHotels />}
          <TrendingCities />
          <FeaturedDestinations sx={{ marginTop: "50vh" }} />
        </div>
        <TravelYourPassion />
      </div>
    </>
  );
};
