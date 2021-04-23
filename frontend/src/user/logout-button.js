import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "@material-ui/core";
import ExitToApp from '@material-ui/icons/ExitToApp';


const LogoutButton = () => {
  const { logout } = useAuth0();
  return (
    <Button
      color = 'primary'
      variant="contained" 
      startIcon = {<ExitToApp />}
      onClick={() =>logout({
        returnTo: window.location.origin,
      })}
    >
      Log Out
    </Button>
  );
};

export default LogoutButton;