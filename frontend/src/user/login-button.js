import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

import { Button } from "@material-ui/core";
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();
  return (
    <Button
      color = 'primary'
      variant="contained" 
      startIcon = {<ArrowForwardIosIcon />}
      onClick={() => loginWithRedirect()}
    >
      Log In
    </Button>
  );
};

export default LoginButton;

