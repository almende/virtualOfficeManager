/* eslint-disable no-script-url */
import React, { useState, useEffect } from "react";
import axios from "axios";

import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Title from "./Title";
import ShowAndTellItem from "./ShowAndTellItem";

export default function ShowAndTellList() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState("10");

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
            <TableCell>Start</TableCell>
            <TableCell>End</TableCell>
            <TableCell>Presenter</TableCell>
            <TableCell>Topic</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>{data.map(item => ShowAndTellItem(item))}</TableBody>
      </Table>
      {/* <div className={classes.seeMore}>
        <Link color="primary" href="javascript:;">
          See more orders
        </Link>
      </div> */}
    </React.Fragment>
  );
}
