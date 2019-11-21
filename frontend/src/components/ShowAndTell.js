/* eslint-disable no-script-url */
import React, { useState, useEffect } from "react";
import axios from "axios";

import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Title from "./Title";
import { withStyles, makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";

function rand() {
  return Math.round(Math.random() * 20) - 10;
}

function getModalStyle() {
  const top = 50 + rand();
  const left = 50 + rand();

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`
  };
}

const StyledTableCell = withStyles(theme => ({
  head: {
    fontWeight: 700
  },
  body: {
    fontSize: 14
  }
}))(TableCell);

const useStyles = makeStyles(theme => ({
  paper: {
    position: "absolute",
    width: 400,
    backgroundColor: theme.palette.background.paper,
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  }
}));

export default function ShowAndTellList() {
  const classes = useStyles();
  const [data, setData] = useState([]);
  const [query] = useState("10");
  const [modalStyle] = React.useState(getModalStyle);
  const [open, setOpen] = React.useState(false);
  const [modalItem, setModalItem] = React.useState(null);

  const handleClick = (event, item) => {
    setModalItem(item);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    let ignore = false;

    async function fetchData() {
      const result = await axios("http://localhost:8040/gcal/view/" + query);
      if (!ignore) setData(result.data);
    }

    fetchData();
    return () => {
      ignore = true;
    };
  }, [query]);

  return (
    <React.Fragment>
      <Title>Upcoming show-and-tells</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <StyledTableCell>Start</StyledTableCell>
            <StyledTableCell>End</StyledTableCell>
            <StyledTableCell>Presenter</StyledTableCell>
            <StyledTableCell>Topic</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map(item => (
            <TableRow
              hover
              key={item.id}
              onClick={event => handleClick(event, item)}
            >
              <TableCell>{item.start.dateTime}</TableCell>
              <TableCell>{item.end.dateTime}</TableCell>
              <TableCell>{item.presenter}</TableCell>
              <TableCell>{item.topic}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {/* <div className={classes.seeMore}>
        <Link color="primary" href="javascript:;">
          See more orders
        </Link>
      </div> */}

      <Modal
        aria-labelledby="simple-modal-title"
        aria-describedby="simple-modal-description"
        open={open}
        onClose={handleClose}
      >
        <div style={modalStyle} className={classes.paper}>
          <h2 id="simple-modal-title">Show and tell entry</h2>
          <p id="simple-modal-description">
            {modalItem ? modalItem.description : "no data"}
          </p>
        </div>
      </Modal>
    </React.Fragment>
  );
}
