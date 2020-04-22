import React, { useState } from "react";
// import logo from "./logo.svg";
import "./App.css";
import Dashboard from "./components/Dashboard";
import GoogleLogin from "react-google-login";

function App() {
  const clientId =
    "518561222908-atvnmvl13p2uucktd3pggee9c3qrpk43.apps.googleusercontent.com";
  const notLoggedInMessage = "user not signed in";
  const [currentUser, setCurrentUser] = useState({
    error: notLoggedInMessage,
  });

  function responseGoogle(response) {
    setCurrentUser(response);
    getContent();
  }

  function responseGoogleSuccess(response) {
    console.log("SUCCESS");
    responseGoogle(response);
  }

  function responseGoogleFailure(response) {
    console.log("FAILURE");
    responseGoogle(response);
  }

  function getContent() {
    if (!("error" in currentUser)) {
      return (
        <Dashboard
          currentUser={currentUser}
          setCurrentUser={setCurrentUser}
          clientId={clientId}
          notLoggedInMessage={notLoggedInMessage}
        ></Dashboard>
      );
    } else {
      return (
        <div>
          {currentUser.error !== "user not signed in" && (
            <p>ERROR: {currentUser.error}</p>
          )}
          <p>You are not signed in. Click here to sign in.</p>
          <GoogleLogin
            clientId={clientId}
            onSuccess={responseGoogleSuccess}
            onFailure={responseGoogleFailure}
            cookiePolicy={"single_host_origin"}
          />
        </div>
      );
    }
  }

  return <div className="App">{getContent()}</div>;
}

export default App;
