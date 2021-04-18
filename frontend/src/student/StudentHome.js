import './StudentHome.scss'
import {NavBar} from "../nav/NavBar";

import React, {useEffect, useState} from "react";

import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import {getUserInfo, listAssignmentsStudent, joinClassroom} from "../requests";

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import Container from '@material-ui/core/Container';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
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
  grow: {
    flexGrow: 1,
  },
}));

export function StudentHome(props) {
  return (
    <div>
      <NavBar firstName={props.userData['first_name']} lastName={props.userData['last_name']}/>
      <Essay />
    </div>
  )
}

//load all essays
function Essay() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()
  const [essaysTitles, setEssaysTitles] = useState();
  const [classNumber, setClassNumber] = useState(1);
  const [openCurrent, setOpenCurrent] = useState(true);

  function handleSetClassNumber(e) {
    setClassNumber(e.target.value);
  }

  const handleClickOpen = () => {
    setOpenCurrent(!openCurrent);
  };

  //used for scroll down menu for classes
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listAssignmentsStudent(token, classNumber).then((response) => {
        setEssaysTitles(
          response.data.map((data) => <li>
            <ListItem button onClick={() => {
              history.push(`/student/classrooms/${classNumber}/assignments/${data['id']}`)}
            } className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={data['title']} />
            </ListItem>
          </li>)
        )
      })
    })
  }, [classNumber])

  const boxCol = grey[300]

  return (
    <div>
      <Container maxWidth="lg">
        <Box height={50} />
        <Typography variant="h3" align="center">
          Student Home
        </Typography>
        <Box height={50} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Select Classroom
          </Typography>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="age-native-simple">Class</InputLabel>
            <Select value={classNumber} onChange={handleSetClassNumber}>
              <option aria-label="None" value="" />
              <option value = {1}> Class 1 </option>
              <option value = {2}> Class 2 </option>
              <option value = {3}> Class 3 </option>
              <option value = {4}> Class 4 </option>
            </Select>
            <FormHelperText>input for class number</FormHelperText>
          </FormControl>
        </Box>
        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Box bgcolor={boxCol}>
          <ListItem button onClick={handleClickOpen}>
            <ListItemText primary="Current Assignments" />
            {openCurrent ? <ExpandLess /> : <ExpandMore />}
          </ListItem>
          </Box>
  
          <List component="div" disablePadding>
            <Collapse in={openCurrent} timeout="auto" unmountOnExit>
              {essaysTitles}
            </Collapse>
          </List>
        </Box>
  
        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Student Options:
          </Typography>
          <Button variant="contained" color="primary" href="/join-classroom">
            Join Classroom
          </Button>
        </Box>
      </Container>
    </div>
  )
}

//function to create assignment needs fixing for join classfoom
export function JoinClassroomForm(props) {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()

  const [id, setID] = useState()
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  function handleChange(event) {
    setID(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      joinClassroom(id, token).then((response) => {
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
          Join Classroom
          </Typography>
          <form className={classes.root} noValidate autoComplete="off">
            <TextField id="filled-basic" type="number" label="Classroom Number" variant="filled" onChange={handleChange}/>
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