import "./NavBar.scss"
import bell from "../images/bell.svg"
import defaultAvatar from "../images/default_avatar.svg"
import React, {useEffect, useState} from "react";
import LoginButton from "../user/login-button";
import LogoutButton from "../user/logout-button";
import {useHistory} from "react-router-dom";

//matirial-ui imports
import { fade, makeStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import { AppBar, Button } from '@material-ui/core';
import Badge from '@material-ui/core/Badge';
import { Typography } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';


import Mail from '@material-ui/icons/Mail';
import AccountCircle from '@material-ui/icons/AccountCircle';

const useStyles = makeStyles((theme) => ({
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  },
  sectionDesktop: {
    display: 'none',
    [theme.breakpoints.up('md')]: {
      display: 'flex',
    },
  },
}));

function NavBar(props) {
  const history = useHistory()
  const classes = useStyles();
  const [mail, setMail] = useState(0)

  return (
    <div>
      <AppBar position = "static">
        <Toolbar variant="dense">
         <Button variant="contained" color="primary" onClick={() => {
            history.push(`/`)
          }}>Home</Button>

          <Typography className={classes.title} variant="h6" noWrap>
            Authorship Verification for Plagiarism Detection(AVPD)
          </Typography>

          <div className={classes.grow} />
          
          <Typography className={classes.title} variant="h6" noWrap>
            {`${props.firstName} ${props.lastName}`}
          </Typography>

          <AccountCircle />

          <div className={classes.sectionDesktop}>
            <IconButton color="inherit">
              <Badge badgeContent={mail} color="secondary">
                <Mail />
              </Badge>
            </IconButton>
            <LogoutButton/>
          </div>

        </Toolbar>
      </AppBar>
    </div>
  );
}

function UnauthenticatedNavBar() {
  const classes = useStyles();

  return (
    <div>
      <AppBar position = "static">
        <Toolbar variant="dense">
          <Typography className={classes.title} variant="h6" noWrap>
            Authorship Verification for Plagiarism Detection(AVPD)
          </Typography>

          <div className={classes.grow} />

          <div className={classes.sectionDesktop}>
            <LoginButton/>
          </div>

        </Toolbar>
      </AppBar>
    </div>
  )
}

export {NavBar, UnauthenticatedNavBar};