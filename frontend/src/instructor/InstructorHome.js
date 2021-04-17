import './InstructorHome.scss'
import React, {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, listClassroom, createClassroom} from "../requests";

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

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

export function InstructorHome(props) {
  return (
    <div>
      <Classrooms/>
    </div>
  )
}

function Classrooms() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()

  const [classroomTitles, setClassroomTitles] = useState();
  const [openCurrent, setOpenCurrent] = useState(true);
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listClassroom(token).then((response) => {
        setClassroomTitles(
          response.data.map((data) => <li>
            <ListItem button onClick={() => {
              history.push(`/instructor/classrooms/${data['id']}`)}
            } className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={data['title']} />
            </ListItem>
          </li>)
        )
      })
      getUserInfo(token).then((response) => {
        setUserInfo(prevState => ({
          ...prevState,
          first_name: response.data.first_name,
          last_name: response.data.last_name          
        }));
      })
    })
  }, [])

  const handleClickOpen = () => {
    setOpenCurrent(!openCurrent);
  };

  const boxCol = grey[300]

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <Container maxWidth="md">
        <Box height={50} />
        <Typography variant="h3" align="center">
          Instructor Home
        </Typography>
        <Box height={50} />

        <Box mx="auto" bgcolor="background.paper" p={1}>
          <Box bgcolor={boxCol}>
            <ListItem button onClick={handleClickOpen}>
              <ListItemText primary="Classrooms" />
              {openCurrent ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
          </Box>
          <List component="div" disablePadding>
            <Collapse in={openCurrent} timeout="auto" unmountOnExit>
              {classroomTitles}
            </Collapse>
          </List>
        </Box>

        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Instructor Options:
          </Typography>
          
          <Button variant="contained" color="primary" href='/create-classroom'>
            Create Classroom
          </Button>
        </Box>
      </Container>
    </div>
  )
}

export function CreateClassroomForm() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()

  const [title, setTitle] = useState("");
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  function handleChange(event) {
    setTitle(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createClassroom(title, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getUserInfo(token).then((response) => {
        setUserInfo(prevState => ({
          ...prevState,
          first_name: response.data.first_name,
          last_name: response.data.last_name          
        }));
      })
    })
  }, [])

  return (
  <div>
    <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

    <Container maxWidth="md">
      <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
          Create Classroom
          </Typography>
          <form className={classes.root} noValidate autoComplete="off">
            <TextField id="filled-basic" label="Classroom Name" variant="filled" onChange={handleChange}/>
            <Box height={20} />
            <Button variant="contained" color="primary" onClick={handleSubmit}>
              Submit
            </Button>

            <Button variant="contained" color="primary" onClick={() => {
              history.push(`/`)
            }}>Return</Button>
      </form>
      </Box>
    </Container>
  </div>
  )
}