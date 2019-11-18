import React from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";

export default function ShowAndTellItem(item) {
  const handleClick = (event, item) => {
    console.log(item);
  };

  return (
    <TableRow key={item.id} onClick={event => handleClick(event, item)}>
      <TableCell>{item.start.dateTime}</TableCell>
      <TableCell>{item.end.dateTime}</TableCell>
      <TableCell>{item.presenter}</TableCell>
      <TableCell>{item.topic}</TableCell>
    </TableRow>
  );
}
