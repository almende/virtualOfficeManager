import React, { useState, useEffect } from "react";
// import logo from "./logo.svg";
import "./App.css";
import Dashboard from "./components/Dashboard";
import Button from "@material-ui/core/Button";
// import { google } from "googleapis";

function App() {
  const clientId =
    "518561222908-ff4s6tej2ev3diklm30lrpfnaftv7kat.apps.googleusercontent.com";
  const notLoggedInMessage = "user not signed in";
  const [signedIn, setSignedIn] = useState(false);

  const onAuthChange = (isSignedIn) => {
    setSignedIn(isSignedIn);
  };

  useEffect(() => {
    const params = {
      clientId: clientId,
      scope: "https://www.googleapis.com/auth/contacts",
      apiKey: "AIzaSyD3uim3mnA75qTJzhtgT6DSTegwMHk7dA0",
      discoveryDocs: [
        "https://www.googleapis.com/discovery/v1/apis/people/v1/rest",
      ],
    };

    window.onLoadCallback = window.gapi.load("client:auth2", () => {
      window.gapi.client.init(params).then((response) => {
        onAuthChange(window.gapi.auth2.getAuthInstance().isSignedIn.get());
        window.gapi.auth2.getAuthInstance().isSignedIn.listen(onAuthChange);
      });
    });
  }, []);

  function onSignInButtonClick() {
    window.gapi.auth2.getAuthInstance().signIn();
  }

  function getContent() {
    if (signedIn) {
      return <Dashboard></Dashboard>;
    } else {
      return (
        <div>
          <p>You are not signed in. Click here to sign in.</p>
          <Button id="loginButton" onClick={onSignInButtonClick}>
            Login with Google
          </Button>
        </div>
      );
    }
  }

  return <div className="App">{getContent()}</div>;
}

export default App;
