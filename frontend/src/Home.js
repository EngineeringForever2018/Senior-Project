import {useAuth0} from "@auth0/auth0-react";
import {useHistory, useLocation} from "react-router-dom";
import axios from "axios";
import React from "react";
import {UnauthenticatedNavBar} from "./nav/NavBar";
import {InstructorHome} from "./instructor/InstructorHome";
import {StudentHome} from "./student/StudentHome";
import {getUserData} from "./requests";
import LogoutButton from "./user/logout-button";

export function Home() {
  const {isAuthenticated, getAccessTokenSilently} = useAuth0()

  const history = useHistory()
  const location = useLocation()

  if (isAuthenticated) {
    let userData = undefined;

    if (location.state !== undefined) {
      userData = location.state.userData
    }

    if (userData === undefined) {
      getAccessTokenSilently().then((token) => {
        getUserData(token).then((response) => {
          history.push('/', {userData: response.data})
        }, (error) => console.log(error.response))
      })
    } else {
      if (userData['user_type'] === 'student') {
        return <StudentHome userData={userData}/>
      } else {
        return <InstructorHome userData={userData}/>
      }
    }
  }

  return UnauthenticatedHome()
}

function UnauthenticatedHome() {
  return (
    <div>
      <UnauthenticatedNavBar/>
      <LogoutButton />
    </div>
  )
}

