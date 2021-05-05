import './InstructorClassrooms.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, listAssignments, createAssignment, deleteClassroom, updateClassroom, newViewClassroom, getData} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import moment from 'moment';

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
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
  KeyboardDatePicker,
} from '@material-ui/pickers';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import InsertDriveFile from '@material-ui/icons/InsertDriveFile';
import DateFnsUtils from '@date-io/date-fns';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export function InstructorClassroom() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id} = useParams()

  const [assignmentTitles, setAssignmentTitles] = useState()
  const [openCurrent, setOpenCurrent] = useState(true);

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [classInfo, setClassinfo] = useState({
    title:'',
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listAssignments(id, token).then((response) => {
        setAssignmentTitles(
          response.data.map((assignment) => <li>
            <ListItem button onClick={() => {
              history.push(`/instructor/classrooms/${id}/assignments/${assignment['id']}`)}
            } className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={assignment['title']} />
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
      newViewClassroom(id, token).then((response) => {
        setClassinfo(prevState => ({
          ...prevState,
          title: response.data.title,
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
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Container maxWidth="md">

        <Box height={50} />
        <Typography variant="h3" align="center">
          Classroom: {classInfo.title}
        </Typography>
        <Box height={50} />
        
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Classroom information:
          </Typography>
          <Typography variant="h7">
            Classroom ID: {id}
          </Typography>
          <Box height = {10}/>
        </Box>
        <Box height={50} />

        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Box bgcolor={boxCol}>
            <ListItem button onClick={handleClickOpen}>
              <ListItemText primary="Classrooms" />
              {openCurrent ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
          </Box>

          <List component="div" disablePadding>
            <Collapse in={openCurrent} timeout="auto" unmountOnExit>
              {assignmentTitles}
            </Collapse>
          </List>
        </Box>
        
        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Instructor Options:
          </Typography>

          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/create-assignment`, {classroomID: id})
          }}>Create Assignment</Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/instructor/classrooms/${id}/students`, {classroomID: id})
          }}>List Students</Button>

          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/update-classroom`, {classID: id})
          }}>Update Classroom</Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            getAccessTokenSilently().then((token) => {
              deleteClassroom(id, token).then(() => history.push('/'), (error) => console.log(error.response))
            }, (error) => console.log(error))
          }}>Delete Classroom</Button>        
  
          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/`)
          }}>Return</Button>

          <Box height = {20}/>
        </Box>

      </Container>
      </MuiPickersUtilsProvider>
    </div>
  )
}

//form to update classroom
export function UpdateClassroomForm() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()
  const location = useLocation()
  const id = location.state.classID

  const [title, setTitle] = useState("");
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  const [classInfo, setClassinfo] = useState({
    title:'',
  })


  function handleChange(event) {
    setTitle(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      updateClassroom(title, id, token).then((response) => {
        history.push(`/instructor/classrooms/${id}`)
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
      newViewClassroom(id, token).then((response) => {
        setClassinfo(prevState => ({
          ...prevState,
          title: response.data.title,
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
          Update Classroom
        </Typography>
        <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
          <TextField id="filled-basic" label="Classroom Name" variant="filled" onChange={handleChange}/>
          <Box height={10} />
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Submit
          </Button>

          <Button variant="contained" color="primary" onClick={() => {
              history.push(`/instructor/classrooms/${id}`)
            }}>Return</Button>
        </form>
      </Box>
    </Container>
  </div>
  )
}

//function to create assignment
export function CreateAssignmentForm(props) {
  const classes = useStyles();
  const location = useLocation()
  const id = location.state.classroomID
  const {getAccessTokenSilently} = useAuth0()

  var day = new Date().getDate(); //To get the Current Date
  var month = new Date().getMonth() + 1; //To get the Current Month
  var year = new Date().getFullYear(); //To get the Current Year

  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [selectedDate, setSelectedDate] = useState(new Date(`${year}-01-${day}T24:00:00`));

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  const history = useHistory()

  function handleTitleChange(event) {
    setTitle(event.target.value);
  }

  function handleDescriptionChange(event) {
    setDescription(event.target.value)
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createAssignment(id, title, description, {
        'year': parseInt(moment(selectedDate).format('YYYY')),
        'month': parseInt(moment(selectedDate).format('MM')),
        'day': parseInt(moment(selectedDate).format('DD')),
        'hour': parseInt(moment(selectedDate).format('HH')),
        'minute': parseInt(moment(selectedDate).format('mm'))
      }, token).then((response) => {
        history.push(`/instructor/classrooms/${id}`)
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
    if(month < 10){
      setSelectedDate(`${year}-0${month}-${day}T24:00:00`)
    } else {
      setSelectedDate(`${year}-${month}-${day}T24:00:00`)
    }
  }, [])

  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Container maxWidth="md">
      <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
          Create Assignment
          </Typography>
          <form className={classes.root} noValidate autoComplete="off">
            <TextField id="filled-basic" label="Title" variant="filled" onChange={handleTitleChange}/>
            <TextField id="filled-basic"  label="Description" variant="filled" onChange={handleDescriptionChange}/>
            <div/>
            <KeyboardDatePicker
              label="Date picker dialog"
              format="MM/dd/yyyy"
              value={selectedDate}
              onChange={handleDateChange}
              KeyboardButtonProps={{
                'aria-label': 'change date',
              }}
            />
            <KeyboardTimePicker
              margin="normal"
              label="Time picker"
              value={selectedDate}
              onChange={handleDateChange}
              KeyboardButtonProps={{
                'aria-label': 'change time',
              }}
        />
            <div/>
            <Button variant="contained" color="primary" onClick={handleSubmit}>
              Submit
            </Button>

            <Button variant="contained" color="primary" onClick={() => {
              history.push(`/instructor/classrooms/${id}`)
            }}>Return</Button>
          </form>
        </Box>
      </Container>
      </MuiPickersUtilsProvider>
    </div>
  )
}