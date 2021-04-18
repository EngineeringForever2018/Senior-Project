import './InstructorAssignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, deleteAssignment, updateAssignment, viewAssignment} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import moment from 'moment';

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
  KeyboardDatePicker,
} from '@material-ui/pickers';
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

export function InstructorAssignment() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

  const [assignmentTitles, setAssignmentTitles] = useState({
    id: '',
    classroom: '',
    title: '',
    description: '',
    due_date: ''
  })
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  var day = new Date().getDate(); //To get the Current Date
  var month = new Date().getMonth() + 1; //To get the Current Month
  var year = new Date().getFullYear(); //To get the Current Year
  var hours = new Date().getHours(); //To get the Current Hours

  //hooks used for date
  const [date, setDate] = useState(0)
  const [onTime, setOnTime] = useState("Not changed")
  const [timeLeft, setTimeLeft] = useState(0)
  const [unitLeft, setUnitLeft] = useState("Not changed")

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewAssignment( classroomID,id, token).then((response) => {
        setAssignmentTitles(prevState => ({
          ...prevState,
          id: response.data.id,
          classroom: response.data.classroom,
          title: response.data.title,
          description: response.data.description,
          due_date: response.data.due_date
        }));
        setDate(date + 1)
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

    //use effect to compare assignment time to current time down to hour
    useEffect(() => {
      var time = (assignmentTitles.due_date).split("T")
      var date = (time[0]).split("-")
      var today = time[1]
      
      if(parseInt(date[0], 10) < parseInt(year)) {
        setOnTime("overdue")
        setUnitLeft("year")
        setTimeLeft(parseInt(year) - parseInt(date[0], 10))
      }
      if(parseInt(date[0], 10) > parseInt(year)) {
        setOnTime("due")
        setUnitLeft("year")
        setTimeLeft(parseInt(date[0], 10) - parseInt(year))
      }
      if(parseInt(date[0], 10) == parseInt(year)) {
        if(parseInt(date[1], 10) < parseInt(month)) {
          setOnTime("overdue")
          setUnitLeft("month")
          setTimeLeft(parseInt(month) - parseInt(date[1], 10))
        }
        if(parseInt(date[1], 10) > parseInt(month)) {
          setOnTime("due")
          setUnitLeft("month")
          setTimeLeft(parseInt(date[1], 10) - parseInt(month))
        }
        if(parseInt(date[1], 10) == parseInt(month)) {
          if(parseInt(date[2], 10) < parseInt(day)) {
            setOnTime("overdue")
            setUnitLeft("day")
            setTimeLeft(parseInt(day) - parseInt(date[2], 10))
          }
          if(parseInt(date[2], 10) > parseInt(day)) {
            setOnTime("due")
            setUnitLeft("day")
            setTimeLeft(parseInt(date[2], 10) - parseInt(day))
          }
        }
        if(parseInt(date[2], 10) == parseInt(day)) {
          if(parseInt(today, 10) < parseInt(hours)) {
            setOnTime("overdue")
            setUnitLeft("hours")
            setTimeLeft(parseInt(hours) - parseInt(today, 10))          
          }
          if(parseInt(today, 10) > parseInt(hours)) {
            setOnTime("due")
            setUnitLeft("hours")
            setTimeLeft(parseInt(today, 10) - parseInt(hours))
          }
        }
      }
    }, [date])

    const DisplayStatus = () => {
      if(onTime == "overdue") {
        return(
          <p className = "text"> Assignment finished from: {timeLeft} {unitLeft}</p>
        )
      } else {
        return(
          <p className = "text"> Time remaining: {timeLeft} - {unitLeft}</p>
        )
      }
    }

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <Container maxWidth="md">
        <Box height={50} />
        <Typography variant="h3" align="center">
        Assignment Info
        </Typography>
        <Box height={50} />
          <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <p className = "text"> title: {assignmentTitles.title}</p>
          <p className = "text"> due date: {assignmentTitles.due_date}</p>
          <DisplayStatus />
          <p className = "text"> description: {assignmentTitles.description}</p>
        </Box>

        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Instructor Options:
          </Typography>
          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/instructor/classrooms/${classroomID}/assignments/${id}/submissions`)
          }}>List Submissions</Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            history.push('/update-assignment', 
            {classroomID: assignmentTitles.id,
            assignmentID: assignmentTitles.classroom})
          }}>Update Assignment</Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            getAccessTokenSilently().then((token) => {
            deleteAssignment(classroomID, id, token).then(() =>
            history.push('/instructor/classrooms/1'), (error) => console.log(error.response))
            }, (error) => console.log(error))
          }}>Delete Assignment</Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/instructor/classrooms/${classroomID}`, {classroomID: id})
          }}>Return</Button>
        </Box>
      </Container>
    </div>
  )
}

export function UpdateAssignmentForm(props) {
  const classes = useStyles();
  const location = useLocation()
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()

  const Cid = location.state.classroomID
  const Aid = location.state.assignmentID

  var day = new Date().getDate(); //To get the Current Date
  var month = new Date().getMonth() + 1; //To get the Current Month
  var year = new Date().getFullYear(); //To get the Current Year

  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  const [selectedDate, setSelectedDate] = useState(new Date(`${year}-01-${day}T24:00:00`));
  const [assignmentTitles, setAssignmentTitles] = useState({
    id: '',
    classroom: '',
    title: '',
    description: '',
    due_date: ''
  })
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewAssignment( Cid, Aid, token).then((response) => {
        setAssignmentTitles(prevState => ({
          ...prevState,
          id: response.data.id,
          classroom: response.data.classroom,
          title: response.data.title,
          description: response.data.description,
          due_date: response.data.due_date
        }));
      })
      getUserInfo(token).then((response) => {
        setUserInfo(prevState => ({
          ...prevState,
          first_name: response.data.first_name,
          last_name: response.data.last_name          
        }));
      })
    })
    setTitle(assignmentTitles.title)
    setDescription(assignmentTitles.description)
    if(month < 10){
      setSelectedDate(`${year}-0${month}-${day}T24:00:00`)
    } else {
      setSelectedDate(`${year}-${month}-${day}T24:00:00`)
    }
  }, [])

  function handleTitleChange(event) {
    setTitle(event.target.value);
  }

  function handleDescriptionChange(event) {
    setDescription(event.target.value)
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      updateAssignment(Cid, Aid, title, description, {
        'year': parseInt(moment(selectedDate).format('YYYY')),
        'month': parseInt(moment(selectedDate).format('MM')),
        'day': parseInt(moment(selectedDate).format('DD')),
        'hour': parseInt(moment(selectedDate).format('HH')),
        'minute': parseInt(moment(selectedDate).format('mm'))
      }, token).then((response) => {
        history.push(`/instructor/classrooms/${Aid}/assignments/${Cid}`)
      }, (error) => console.log(error.response))
    })
    event.preventDefault()
  }

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
              history.push(`/instructor/classrooms/${Aid}/assignments/${Cid}`)
            }}>Return</Button>
          </form>
        </Box>
      </Container>
      </MuiPickersUtilsProvider>
    </div>
  )
}