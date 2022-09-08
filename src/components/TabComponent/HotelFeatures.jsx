import { Box, Typography } from "@material-ui/core";
import { Stack } from "@mui/system";
import React from "react";
import styles from "./HotelFeatures.module.css";
import WifiIcon from "@mui/icons-material/Wifi";
import PoolIcon from "@mui/icons-material/Pool";
import GolfCourseIcon from "@mui/icons-material/GolfCourse";
import AirportShuttleOutlinedIcon from "@mui/icons-material/AirportShuttleOutlined";
import LocalHospitalOutlinedIcon from "@mui/icons-material/LocalHospitalOutlined";
import CoronavirusOutlinedIcon from "@mui/icons-material/CoronavirusOutlined";

const HotelFeatures = () => {
  return (
    <Box>
      <Typography className={styles.heading}>Hotel Features</Typography>
      <Stack direction={"row"} spacing={2}>
        <Typography component={"span"}>
          <WifiIcon className={styles.iconStyle} /> Wi-fi
        </Typography>
        <Typography component={"span"}>
          <PoolIcon className={styles.iconStyle} /> Infinity Pool
        </Typography>
        <Typography component={"span"}>
          <GolfCourseIcon className={styles.iconStyle} /> Golf Course
        </Typography>
        <Typography component={"span"}>
          <AirportShuttleOutlinedIcon className={styles.iconStyle} /> Airport
          Shuttle
        </Typography>
        <Typography component={"span"}>
          <LocalHospitalOutlinedIcon className={styles.iconStyle} /> On Call
          Doctor
        </Typography>
        <Typography component={"span"}>
          <CoronavirusOutlinedIcon className={styles.iconStyle} /> Covid safety
          Protocols
        </Typography>
      </Stack>
    </Box>
  );
};

export default HotelFeatures;
