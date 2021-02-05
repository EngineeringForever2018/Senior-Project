import {useAuth0} from "@auth0/auth0-react";

export function serverUrl() {
  return process.env.REACT_APP_SERVER_URL;
}

export async function authenticateRequest(requestConfig, token) {
  requestConfig.headers = {
    'Authorization': `Bearer ${token}`
  }

  return requestConfig
}