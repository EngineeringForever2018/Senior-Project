// import {useLocation} from 'react-router-dom';
import React, {useEffect, useState} from "react";
import {serverUrl} from "../utils";
import './ReportScreen.scss'
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import {getDetailedReport, getUserInfo, getClassroomStudent, getSubmission, getSubmissionReport, acceptSubmission} from "../requests";
import {NavBar} from "../nav/NavBar";
import DocViewer, {DocViewerRenderers} from "react-doc-viewer";

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
import grey from '@material-ui/core/colors/grey';
import red from '@material-ui/core/colors/red';

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

const badFlag = red[500]

function CircularProgressWithLabel(props) {
  if(props.flag) {
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
          <Typography variant="caption" component="div">{`${Math.round(
            props.value,
          )}%`}</Typography>
        </Box>
      </Box>
    );
  } else {
    return (
      <Box position="relative" display="inline-flex">
        <CircularProgress size = {200} variant="determinate" style={{'color': badFlag}} {...props} />
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
          <Typography variant="caption" component="div">{`${Math.round(
            props.value,
          )}%`}</Typography>
        </Box>
      </Box>
    );
  }
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
  let detailedPath = undefined
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
    detailedPath = location.state.detailedPath
    studentInfo = location.state.studentInfo
  }

  if (report === undefined) {
    getAccessTokenSilently().then((token) => {
      getSubmissionReport(classroomID, assignmentID, id, token).then((response) => {
        getSubmission(classroomID, assignmentID, id, token).then((submissionResponse) => {
          const studentID = submissionResponse.data['student']
            getClassroomStudent(classroomID, studentID, token).then((studentResponse) => {
            let detailed = `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}/detailed-report`
            history.push(location.pathname, {report: response.data, studentInfo: studentResponse.data, detailedPath: detailed})
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
                      studentLastName={studentLastName} detailedPath={detailedPath} authorshipFlag={flag}/>
    )
  }
}

function ReportScreenFlag(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName
  const authorshipFlag = props.authorshipFlag
  const detailedPath = props.detailedPath

  const classes = useStyles();

  const {getAccessTokenSilently} = useAuth0()

  const location = useLocation()
  const history = useHistory()

  const {classroomID, assignmentID, id} = useParams()

  const [file, setFile] = React.useState("");
  const [reportMessage, setReportMessage] = useState();

	// const DisplayFile = ({ image }) => {
  	//   if(image.type == "image/jpeg" ) {
  	//     return(
  	//       <div className = "StudentAssignments">
  	//         <img src={URL.createObjectURL(image)} className = "essayImage"/>
  	//       </div>
  	//     );
  	//   }
  	//   if(image.type == "application/pdf" ) {    
  	//     return(
  	//       <div className = "StudentAssignments"> 
  	//         <div className = "essayPDF">
  	//           {<Viewer fileUrl={URL.createObjectURL(image)} defaultScale={SpecialZoomLevel.PageFit}/>}
  	//         </div>
  	//       </div>
  	//     )
  	//   }
  	//   return(
  	//     <div>
  	//       not able to view file type
  	//     </div>
  	//   )
  	// };
  // const DisplayFile = () => {
  //   return(
  //     <div className = "StudentAssignments">
  //       {<Viewer fileUrl={URL.createObjectURL(detailedReport)} defaultScale={SpecialZoomLevel.PageFit}/>}
  //     </div>
  //   );
  // }
  const docs = [ { uri: detailedPath } ]

  const DisplayFlag = ({flag}) => {
    if(flag) {
      return(
        <Typography variant="h7">
          This is flagged as a good report.
        </Typography>
      )
    } else {
      return(
        <Typography variant="h7">
          This is flagged as a bad report.
        </Typography>
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

  const boxCol = grey[300]

  return (
    <div>
        <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
        <Container maxWidth="md">
          <Box height = {60}/>
          <Grid direction="row" container spacing={3} alignItems="center">
            <Grid item sm={6}>
              <Box height={500} width="100%" bgcolor="background.paper">
                <Container>
                  <Box height = {20}/>
                  <Typography variant="h5">
                    Report Details:
                  </Typography>
                  <Box height = {20}/>
                  <Typography variant="h7">
                    {`Student Name: ${studentFirstName} ${studentLastName}`}
                  </Typography>
                  <Box height = {20}/>
                  <DisplayFlag flag = {authorshipFlag} />
                </Container>

                <Box height = {260} />

                <Box size="auto" height={80} bgcolor={boxCol} p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
	                <a href={detailedPath}>Click to download detailed report</a>
                </Box>
                {/*<DocViewer documents={docs} config={{header: {disableFileName: true, retainURLParams: true}}} />*/}


              </Box>
            </Grid>

            <Grid item sm={6}>
              <Box height={500} display="flex" bgcolor="background.paper">
                <Grid direction="column" container alignItems="center" justify="space-between">
                  <Grid height={30} width="60%" >
                    <Box size="auto" p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                      <Typography variant="h5">
                        Report Results:
                      </Typography>
                      
                    </Box>
                  </Grid>

                  <Grid width="60%" >
                    <Box size="auto" p={1} display="flex" alignItems="center" justifyContent="center" m={1} p={1}>
                      <CircularProgressWithLabel value={authorshipProbability * 100} flag={authorshipFlag}/>
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
    </div>
  )
}

export default ReportScreen;
