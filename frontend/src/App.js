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

  var defaultheader = function () {
    return {
      method: null,
      mode: "cors",
      body: null,
      crossDomain: true,
      cache: "no-cache",
      async: false,
      timeout: 3000,
      headers: {
        "Content-Type": "application/json",
        Authorization: "",
        Accept: "*/*",
        "Access-Control-Allow-Headers": "*",
        "X-Requested-With": "XMLHttpRequest",
        "Access-Control-Allow-Origin": "*",
      },
    };
  };

  function getContacts(token) {
    const header = defaultheader();
    header.method = "GET";
    let url = "https://people.googleapis.com/v1/people/me/connections";

    header.headers["Authorization"] = "Bearer " + token;
    fetch(url, header)
      .then((response) => {
        setTimeout(() => {
          let a = 0;
        }, 0);
        return response.json();
      })
      .then((responseJson) => {
        console.log("responseJson=", responseJson);
      })
      .catch((error) => {
        console.log("An error occurred.Please try again", error);
      });
  }

  function responseGoogle(response) {
    setCurrentUser(response);
    getContent();
  }

  function responseGoogleSuccess(response) {
    console.log("SUCCESS");
    responseGoogle(response);

    var contacts = getContacts(currentUser.accessToken);
    console.log(contacts);
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
            scope="profile email https://www.googleapis.com/auth/contacts"
          />
        </div>
      );
    }
  }

  return <div className="App">{getContent()}</div>;
}

export default App;
