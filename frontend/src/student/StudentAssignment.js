import './StudentAssignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignmentStudent, postSubmit} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

//display pdf
import { Viewer } from '@react-pdf-viewer/core';
import { Document, Page, pdfjs } from 'pdfjs-dist'
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry'
import '@react-pdf-viewer/core/lib/styles/index.css';

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

//open assignment
export function StudentAssignment() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

  var day = new Date().getDate(); //To get the Current Date
  var month = new Date().getMonth() + 1; //To get the Current Month
  var year = new Date().getFullYear(); //To get the Current Year
  var hours = new Date().getHours(); //To get the Current Hours

  //hooks used for date
  const [date, setDate] = useState(0)
  const [onTime, setOnTime] = useState("Not changed")
  const [timeLeft, setTimeLeft] = useState(0)
  const [unitLeft, setUnitLeft] = useState("Not changed")

  const [parseTime, setParseTime] = useState({
    year: '',
    month: '',
    day: '',
    hour: '',
    min: ''
  })

  const [assignmentTitles, setAssignmentTitles] = useState({
    id: '',
    classroom: '',
    title: '',
    discription: '',
    due_date: ''
  })
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [file, setFile] = React.useState("");

  //run to get assignment and user data on page load
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewAssignmentStudent( classroomID,id, token).then((response) => {
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
  }, [])

  //run to get assignment and user data on page load
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewAssignmentStudent( classroomID,id, token).then((response) => {
        setAssignmentTitles(prevState => ({
          ...prevState,
          id: response.data.id,
          classroom: response.data.classroom,
          title: response.data.title,
          description: response.data.description,
          due_date: response.data.due_date
        }));
        //changing date runs the useEffect to compare dates
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
    setParseTime(prevState => ({
      ...prevState,
      year: date[0],
      month: date[1],
      day: date[2],
    }));
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

  //code to upload file automaticly uploads after file put in
  function handleUpload(event) {
    setFile(event.target.files[0]);
    event.preventDefault()
  }

  //code to display file
  const DisplayFile = ({ image }) => {
    if(image.type == "image/jpeg" ) {
      return(
        <div className = "StudentAssignments">
          <img src={URL.createObjectURL(image)} className = "essayImage"/>
        </div>
      );
    }
    if(image.type == "application/pdf" ) {    
      return(
        <div className = "StudentAssignments"> 
          <div style={{ border: '1px solid rgba(0, 0, 0, 0.3)', height: "50em",}}>
            {<Viewer defaultScale={1} fileUrl={URL.createObjectURL(image)}/>}
          </div>
        </div>
      )
    }
    return(
      <div/>
    )
  };

  const DisplayStatus = () => {
    if(onTime == "overdue") {
      return(
        <Typography variant="h7">
          Assignment overdue by: {timeLeft} {unitLeft}
        </Typography>
      )
    } else {
      return(
        <Typography variant="h7">
          Time remaining: {timeLeft} - {unitLeft}
        </Typography>
      )
    }
  }

  const DisplayMonth = () => {
    var curMonth = parseTime.month
    if(curMonth == 1){
      return("January")
    } else if(curMonth == 2){
      return("February")
    } else if(curMonth == 3){
      return("March")
    } else if(curMonth == 4){
      return("April")
    } else if(curMonth == 5){
      return("May")
    } else if(curMonth == 6){
      return("June")
    } else if(curMonth == 7){
      return("July")
    } else if(curMonth == 8){
      return("August")
    } else if(curMonth == 9){
      return("September")
    } else if(curMonth == 10){
      return("October")
    } else if(curMonth == 11){
      return("November")
    } else if(curMonth == 12){
      return("December")
    } else {
      return("fail")
    }
  }

  function submitButton(event){
    console.log(file)
    getAccessTokenSilently().then((token) => {
      postSubmit(classroomID,id, file, token).then((response) => {
        history.push(`/student/classrooms/${classroomID}/assignments/${id}/submit`)
      }, (error) => console.log(error.response))
    })
    event.preventDefault()
  }

  var boxSpace = 30;

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <Container maxWidth="md">
        <Box height={boxSpace} />

        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Assignment Info
          </Typography>
          <Box height={30}>
            <Typography variant="h7"> title: {assignmentTitles.title}</Typography>
          </Box>
          <Box height={30}>
            <Typography variant="h7"> description: {assignmentTitles.description}</Typography>
          </Box>
          <Box height={30}>
            <DisplayStatus />
          </Box>
          <Box height={30}>
            <Typography variant="h7">
              due date: <DisplayMonth/>{" "}{parseTime.day}{" "}{parseTime.year}
            </Typography>
          </Box>
        </Box>

        <Box height={boxSpace} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Submit Assignment
          </Typography>
          <input type="file" onChange={handleUpload} />
          <p>Filename: {file.name}</p>
          <p>File type: {file.type}</p>
          {file && <DisplayFile image={file} />}
        </Box>

        <Box height={boxSpace} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Student Options:
          </Typography>
          <Button variant="contained" color="primary" onClick={submitButton}>
            Submit
          </Button>
  
          <Button variant="contained" color="primary" onClick={() => {
            history.push(`/`)
          }}>Return</Button>
  
          <Button variant="contained" color="primary" onClick={() => {  history.push(`/student/classrooms/${classroomID}/assignments/${id}/submitList`)}}>
            All assignments
          </Button>
        </Box>
      </Container>
    </div>
)
}