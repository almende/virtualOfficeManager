/* eslint-disable no-script-url */
import React, { useState, useEffect } from "react";
import axios from "axios";

import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Title from "./Title";
import { withStyles } from "@material-ui/core/styles";
import Moment from "moment";
import ShowAndTellEditItem from "./ShowAndTellEditItem";

const StyledTableCell = withStyles((theme) => ({
  head: {
    fontWeight: 700,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

export default function ShowAndTellList() {
  const [data, setData] = useState([]);
  const [query] = useState("10");
  const [open, setOpen] = useState(false);

  // ModalItems
  const [modalStart, setModalStart] = useState(null);
  const [modalPresenter, setModalPresenter] = useState(null);
  const [modalTopic, setModalTopic] = useState(null);
  const [modalId, setModalId] = useState(null);

  // const stitem = React.forwardRef(ShowAndTellEditItem);

  const handleClick = (event, item) => {
    setModalStart(item.start.dateTime);
    setModalPresenter(item.presenter);
    setModalTopic(item.topic);
    setModalId(item.id);
    setOpen(true);
    console.log(item);
  };

  async function handleDialogSave() {
    console.log({
      start: modalStart,
      presenter: modalPresenter,
      topic: modalTopic,
      id: modalId,
    });

    await patchData({
      presenter: modalPresenter,
      topic: modalTopic,
      id: modalId,
    });

    fetchData(false);
  }

  function getStartDateTimeDurationFromEntry(entry) {
    const start = new Date(entry.start.dateTime);
    const end = new Date(entry.end.dateTime);

    entry.start["date"] = new Moment(entry.start.dateTime).format("ll");
    entry.start["time"] = new Moment(entry.start.dateTime).format("LT");
    entry["duration_ms"] = end - start;
  }

  async function fetchData(ignore) {
    const result = await axios("http://localhost:8040/gcal/view/" + query);

    result.data.forEach(getStartDateTimeDurationFromEntry);

    if (!ignore) setData(result.data);

    return result;
  }

  async function patchData(payload) {
    const entry = await axios.patch(
      "http://localhost:8040/gcal/event",
      payload
    );

    return entry;
  }

  useEffect(() => {
    let ignore = false;

    fetchData(ignore);
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
            <StyledTableCell>Date</StyledTableCell>
            <StyledTableCell>Time</StyledTableCell>
            <StyledTableCell>Duration</StyledTableCell>
            <StyledTableCell>Presenter</StyledTableCell>
            <StyledTableCell>Topic</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item) => (
            <TableRow
              hover
              key={item.id}
              onClick={(event) => handleClick(event, item)}
            >
              <TableCell>{item.start.date}</TableCell>
              <TableCell>{item.start.time}</TableCell>
              <TableCell>{item.duration_ms / 1000 / 60} minutes</TableCell>
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

      <ShowAndTellEditItem
        modalStart={modalStart}
        modalPresenter={modalPresenter}
        modalTopic={modalTopic}
        setModalPresenter={setModalPresenter}
        setModalTopic={setModalTopic}
        setOpen={setOpen}
        handleDialogSave={handleDialogSave}
        open={open}
      ></ShowAndTellEditItem>
    </React.Fragment>
  );
}
