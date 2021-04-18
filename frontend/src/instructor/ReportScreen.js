// import {useLocation} from 'react-router-dom';
import React, {useEffect, useState} from "react";
import './ReportScreen.scss'
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import {getUserInfo, getClassroomStudent, getSubmission, getSubmissionReport, acceptSubmission} from "../requests";
import {NavBar} from "../nav/NavBar";

//display pdf
import { Viewer,SpecialZoomLevel } from '@react-pdf-viewer/core';
import { Document, Page, pdfjs } from 'pdfjs-dist'
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry'
import '@react-pdf-viewer/core/lib/styles/index.css';

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

function CircularProgressWithLabel(props) {
  return (
    <Box position="relative" display="inline-flex">
      <CircularProgress size = {200} variant="determinate" {...props} />
      <Box
        top={0}
        left={0}
        bottom={0}
        right={0}
        position="absolute"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Typography variant="caption" component="div" color="textSecondary">{`${Math.round(
          props.value,
        )}%`}</Typography>
      </Box>
    </Box>
  );
}

function ReportScreen() {
  const classes = useStyles();

  const {getAccessTokenSilently} = useAuth0()

  const location = useLocation()
  const history = useHistory()

  const {classroomID, assignmentID, id} = useParams()

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  let report = undefined
  let studentInfo = undefined

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

  //run code
  if (location.state !== undefined) {
    report = location.state.report
    studentInfo = location.state.studentInfo
  }

  if (report === undefined) {
    getAccessTokenSilently().then((token) => {
      getSubmissionReport(classroomID, assignmentID, id, token).then((response) => {
        getSubmission(classroomID, assignmentID, id, token).then((submissionResponse) => {
          const studentID = submissionResponse.data['student']
          getClassroomStudent(classroomID, studentID, token).then((studentResponse) => {
            history.push(location.pathname, {report: response.data, studentInfo: studentResponse.data})
          }, (error) => console.log(error.response))
        }, (error) => console.log(error.response))
      }, (error) => console.log(error.response))
    })

    return (
      <div>
        <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
        
        Report Screen Loading...
      </div>
    )
  } else {
    const authorshipProbability = report['authorship_probability']
    const studentFirstName = studentInfo['first_name']
    const studentLastName = studentInfo['last_name']

    const flag = report['flag']

    console.log(flag)
    
    return (
      <ReportScreenFlag authorshipProbability={authorshipProbability} studentFirstName={studentFirstName}
                      studentLastName={studentLastName} authorshipFlag={flag}/>
    )
  }
}

function ReportScreenFlag(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName
  const authorshipFlag = props.authorshipFlag

  const classes = useStyles();

  const {getAccessTokenSilently} = useAuth0()

  const location = useLocation()
  const history = useHistory()

  const {classroomID, assignmentID, id} = useParams()

  const [file, setFile] = React.useState("");
  const [reportMessage, setReportMessage] = useState();

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
          <div className = "essayPDF">
            {<Viewer fileUrl={URL.createObjectURL(image)} defaultScale={SpecialZoomLevel.PageFit}/>}
          </div>
        </div>
      )
    }
    return(
      <div>
        not able to view file type
      </div>
    )
  };

  const DisplayFlag = ({flag}) => {
    if(flag) {
      return(
        "this is a good report"
      )
    } else {
      return(
        "this is a bad report"
      )
    }
  }

  function handleUpload(event) {
    setFile(event.target.files[0]);
    event.preventDefault()
  }

  const acceptReport = () => {
    getAccessTokenSilently().then((token) => {
      acceptSubmission(classroomID, assignmentID, id, token).then((response) => {
        setReportMessage(`report submitted`)
      })
    })
  };

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

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
          <p>{`Name: ${studentFirstName} ${studentLastName}`}</p>
          <Grid direction="row" container spacing={3} alignItems="center">
            <Grid item sm={6}>
              <Box height={500} width="100%" bgcolor="background.paper">
                <Box size="auto" height={45} p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                  Display Report
                </Box>
                {file && <DisplayFile image={file} />}
              </Box>
            </Grid>

            <Grid item sm={6}>
              <Box height={500} display="flex" bgcolor="background.paper">
                <Grid direction="column" container alignItems="center" justify="space-between">
                  <Grid height={30} width="60%" >
                    <Box size="auto" p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                      Report Results
                      <DisplayFile flag ={authorshipFlag}/>
                    </Box>
                  </Grid>

                  <Grid width="60%" >
                    <Box size="auto" p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                      <CircularProgressWithLabel value={authorshipProbability * 100} />
                    </Box>
                  </Grid>

                  <Grid height={30} width="60%" >
                    <Box size="auto" p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                      <Button variant="contained" color="primary" onClick={() => {
                        history.push(`/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions`)
                      }}>return</Button>

                      <Button variant="contained" color="primary" onClick={() => {
                        acceptReport()
                      }}>Accept Report</Button>
                    </Box>
                  </Grid>
                </Grid>


              </Box>
            </Grid>
          </Grid>

          {reportMessage}
        </Container>
        <input type="file" onChange={handleUpload} />
    </div>
  )
}

export default ReportScreen;