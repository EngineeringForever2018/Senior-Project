// import {useLocation} from 'react-router-dom';
import React, {useEffect, useState} from "react";
import './ReportScreen.scss'
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import {getClassroomStudent, getSubmission, getSubmissionReport, acceptSubmission} from "../requests";
import {NavBar} from "../nav/NavBar";

//display pdf
import { Viewer } from '@react-pdf-viewer/core';
import { Document, Page, pdfjs } from 'pdfjs-dist'
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry'

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
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

  const [file, setFile] = React.useState("");
  const [reportMessage, setReportMessage] = useState();

  let report = undefined
  let studentInfo = undefined

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
            {<Viewer fileUrl={URL.createObjectURL(image)}/>}
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

  if (location.state !== undefined) {
    report = location.state.report
    studentInfo = location.state.studentInfo
  }

  function handleUpload(event) {
    setFile(event.target.files[0]);
    event.preventDefault()
  }

  const acceptReport = () => {
    getAccessTokenSilently().then((token) => {
      acceptSubmission(classroomID, assignmentID, id, token).then((response) => {
        setReportMessage(`report ${report} submitted`)
      })
    })
  };

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
        <NavBar firstName={'Mary'} lastName={'Bary'}/>
        
        <Container maxWidth="md">
          <p> report undifined</p>
          <p> example report</p>
          <Box mx="auto" bgcolor="background.paper" p={1}>
            {file && <DisplayFile image={file} />}
            <CircularProgressWithLabel value={80} />

            <Button variant="contained" color="primary" onClick={() => {
              history.push(`/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions`)
            }}>return</Button>

            <Button variant="contained" color="primary" onClick={() => {
              acceptReport()
            }}>Accept Report</Button>

          </Box>

          {reportMessage}
        </Container>
        <input type="file" onChange={handleUpload} />
      </div>
    )
  } else {
    const authorshipProbability = report['authorship_probability']
    const studentFirstName = studentInfo['first_name']
    const studentLastName = studentInfo['last_name']

    const flag = report['flag']

    if (flag) {
      return (
        <BadReportScreen authorshipProbability={authorshipProbability} studentFirstName={studentFirstName}
                         studentLastName={studentLastName}/>
      )
    } else {
      return (
        <GoodReportScreen authorshipProbability={authorshipProbability} studentFirstName={studentFirstName}
                          studentLastName={studentLastName}/>
      )
    }
  }
}

function BadReportScreen(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName

  return (
    <div className="BadReportScreen">
      <NavBar firstName="Mary" lastName="Berry"/>
      <div className="panel">
        <div className="submission-info">
          <div className="student-info">
            <p className="student-info-txt">{`Name: ${studentFirstName} ${studentLastName}`}</p>
            <p className="student-info-txt">Potential reasons for discrepancy:</p>
            <ul className="discrepancy-reasons">
              <li><p className="student-info-txt">Large difference in sentence lengths.</p></li>
              <li><p className="student-info-txt">Sudden and large improvement in grammar.</p></li>
            </ul>
          </div>
          <p className="consistency-score">{`Consistency Score: ${authorshipProbability * 100}%`}</p>
          <div className="percentage-bar"/>
          <div className="additional-buttons">
            <button className="btn additional-stats-btn">Additional Statistics</button>
            <button className="btn accept-essay-btn">Add Essay to File</button>
          </div>
        </div>
        <div className="essay-display">
          <p className="student-info-txt">The essay will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}

function GoodReportScreen(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName

  return (
    <div className="GoodReportScreen">
      <NavBar firstName="Mary" lastName="Berry"/>
      <div className="panel">
        <div className="submission-info">
          <div className="student-info">
            <p className="student-info-txt">{`Name: ${studentFirstName} ${studentLastName}`}</p>
            <p className="student-info-txt">No issues here!</p>
          </div>
          <p className="consistency-score">{`Consistency Score: ${authorshipProbability * 100}%`}</p>
          <div className="percentage-bar"/>
          <div className="additional-buttons">
            <button className="btn additional-stats-btn">Additional Statistics</button>
            <button className="btn accept-essay-btn">Add Essay to File</button>
          </div>
        </div>
        <div className="essay-display">
          <p className="student-info-txt">The essay will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}

export default ReportScreen;