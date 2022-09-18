import * as React from "react";
import { useEffect } from "react";
import arrow from "./../../assets/images/ArrowImg.png";
import TextField from "@mui/material/TextField";
import { LocalizationProvider } from "@mui/x-date-pickers-pro";
import { AdapterDayjs } from "@mui/x-date-pickers-pro/AdapterDayjs";
import { DateRangePicker } from "@mui/x-date-pickers-pro/DateRangePicker";
import styles from "./DateSelector.module.css";
import { Box } from "@mui/material";
import moment from "moment/moment";
import { useSelector, useDispatch } from "react-redux";
import { setCheckIn, setCheckOut } from "../../slices/searchSlice";

export default function DateSelector() {
  const [dateValues, setDateValues] = React.useState([null, null]);
  const dispatch = useDispatch();

  const checkin = useSelector((state) => state.search.checkIn);
  const checkout = useSelector((state) => state.search.checkOut);
  useEffect(() => {
    setDateValues([checkin, checkout]);
  }, [checkin, checkout]);

  return (
    <LocalizationProvider
      dateAdapter={AdapterDayjs}
      localeText={{ start: "Check-in", end: "Check-out" }}
    >
      <DateRangePicker
        minDate={new Date()}
        disablePast
        clearable
        value={dateValues}
        format="MM.DD.YYYY"
        onChange={(newValue) => {
          if (newValue[0] != null && newValue[1] != null) {
            const checkInDateValue = moment(new Date(newValue[0])).format(
              "YYYY-MM-DD"
            );
            const checkOutDateValue = moment(new Date(newValue[1])).format(
              "YYYY-MM-DD"
            );

            dispatch(setCheckIn(checkInDateValue), () => {});
            dispatch(setCheckOut(checkOutDateValue), () => {});
          }
        }}
        renderInput={(startProps, endProps) => (
          <React.Fragment>
            <TextField
              format="MM.DD.YYYY"
              className={styles.dateInp}
              {...startProps}
              style={{ backgroundColor: "white" }}
            />
            <Box
              className={styles.arrow}
              src={arrow}
              component="img"
              style={{ zIndex: 99, backgroundColor: "white" }}
            />

            <TextField
              format="MM/DD/YYYY"
              className={styles.dateInp}
              {...endProps}
            />
          </React.Fragment>
        )}
      />
    </LocalizationProvider>
  );
}
