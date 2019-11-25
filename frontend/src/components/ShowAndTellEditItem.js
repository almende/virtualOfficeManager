/* eslint-disable no-script-url */
import React from "react";
import Dialog from "@material-ui/core/Dialog";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import Button from "@material-ui/core/Button";

export default function ShowAndTellEditItem(props) {
  const handleCancel = () => {
    props.setOpen(false);
  };

  const handleSave = () => {
    props.setOpen(false);
    props.handleDialogSave();
  };

  return (
    <Dialog
      aria-labelledby="simple-modal-title"
      aria-describedby="simple-modal-description"
      open={props.open}
      onClose={handleCancel}
    >
      <DialogTitle>Show and tell entry</DialogTitle>
      <DialogContent>
        <b>Date:</b> {props.modalStart ? props.modalStart : "no data"}
        <TextField
          autoFocus
          margin="dense"
          id="presenter"
          label="Presenter"
          type="string"
          fullWidth
          defaultValue={props.modalPresenter ? props.modalPresenter : "no data"}
          onChange={event => props.setModalPresenter(event.target.value)}
        />
        <TextField
          autoFocus
          margin="dense"
          id="topic"
          label="Topic"
          type="string"
          fullWidth
          defaultValue={props.modalTopic ? props.modalTopic : "no data"}
          onChange={event => props.setModalTopic(event.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}
