import {useAuth0} from "@auth0/auth0-react";
import {useHistory, useLocation} from "react-router-dom";
import React from "react";
import {UnauthenticatedNavBar} from "./nav/NavBar";
import {InstructorHome} from "./instructor/InstructorHome";
import {StudentHome} from "./student/StudentHome";
import {getUserInfo} from "./requests";
import LogoutButton from "./user/logout-button";

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import grey from '@material-ui/core/colors/grey';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import InsertDriveFile from '@material-ui/icons/InsertDriveFile';

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
        getUserInfo(token).then((response) => {
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
      <Container maxWidth="md">
        <Box height = {100}/>
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h3" align="center">
            Authorship Verification for Plagiarism Detection(AVPD)
          </Typography>
        </Box>
      
      </Container>
      <LogoutButton />
    </div>
  )
}

