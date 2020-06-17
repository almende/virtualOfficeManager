/* eslint-disable no-script-url */
import React from "react";
import Dialog from "@material-ui/core/Dialog";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import CircularProgress from "@material-ui/core/CircularProgress";

export default function ShowAndTellEditItem(props) {
  const [presenterOpen, setPresenterOpen] = React.useState(false);
  const [options, setOptions] = React.useState([]);
  const loading = presenterOpen && options.length === 0;
  const handleCancel = () => {
    props.setOpen(false);
  };

  const handleSave = () => {
    props.setOpen(false);
    props.handleDialogSave();
  };

  function getDefaultPresenterOptionLabel(option) {
    var name = "";
    var email = "";

    if (typeof option === "string") {
      return option;
    }

    if ("names" in option) {
      name = option.names[0].displayName;
    }

    if ("emailAddresses" in option) {
      email = option.emailAddresses[0].value;
    }

    return name + " (" + email + ")";
  }

  function renderPresenterOption(option) {
    const item = (
      <React.Fragment>
        <Avatar
          alt={option.names ? option.names[0].displayName : ""}
          src={
            option.photos
              ? option.photos[0].url
              : "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Blank_square.svg/400px-Blank_square.svg.png"
          }
        />
        {getDefaultPresenterOptionLabel(option)}
      </React.Fragment>
    );

    return item;
  }

  React.useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }

    window.gapi.client.people.people.connections
      .list({
        resourceName: "people/me",
        personFields: "names,emailAddresses,coverPhotos,photos",
      })
      .then(function (response) {
        setOptions(response.result.connections);
      });

    // (async () => {
    //   const response = await fetch(
    //     "https://country.register.gov.uk/records.json?page-size=5000"
    //   );
    //   const countries = await response.json();

    //   if (active) {
    //     console.log(Object.keys(countries).map((key) => countries[key].item[0]))
    //     // setOptions(Object.keys(countries).map((key) => countries[key].item[0]));
    //   }
    // })();

    return () => {
      active = false;
    };
  }, [loading]);

  React.useEffect(() => {
    if (!presenterOpen) {
      setOptions([]);
    }
  }, [presenterOpen]);

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
        <Autocomplete
          id="presenter"
          autoFocus
          margin="dense"
          label="Presenter"
          type="string"
          fullWidth
          onChange={(event, value) =>
            props.setModalPresenter(getDefaultPresenterOptionLabel(value))
          }
          // defaultValue={props.modalPresenter ? props.modalPresenter : "no data"}
          value={props.modalPresenter || "no data"}
          open={presenterOpen}
          onOpen={() => {
            setPresenterOpen(true);
          }}
          onClose={() => {
            setPresenterOpen(false);
          }}
          getOptionSelected={(option, value) => option.name === value.name}
          getOptionLabel={(option) => getDefaultPresenterOptionLabel(option)}
          // renderOption={(option) => renderPresenterOption(option)}
          options={options}
          loading={loading}
          // renderInput={renderPresenterOption}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Asynchronous"
              variant="outlined"
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <React.Fragment>
                    {loading ? (
                      <CircularProgress color="inherit" size={20} />
                    ) : null}
                    {params.InputProps.endAdornment}
                  </React.Fragment>
                ),
              }}
            />
          )}
          renderOption={renderPresenterOption}
        />
        <TextField
          autoFocus
          margin="dense"
          id="topic"
          label="Topic"
          type="string"
          fullWidth
          defaultValue={props.modalTopic ? props.modalTopic : "no data"}
          onChange={(event) => props.setModalTopic(event.target.value)}
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
