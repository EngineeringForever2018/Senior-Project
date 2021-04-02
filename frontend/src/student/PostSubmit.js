import './PostSubmit.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignmentStudent, listSubmissionsStudent, viewSubmissionStudent} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

//matirial-ui imports
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
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import InsertDriveFile from '@material-ui/icons/InsertDriveFile';

export function PostSubmit() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

  const [submitList, setSubmitList] = useState()
  const [submitID, setSubmitID] = useState()
  const [submitDate, setSubmitDate] = useState()
  const [submitFile, setSubmitFile] = useState()
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
      listSubmissionsStudent(classroomID, id, token).then((response) => {
        setSubmitList(
          response.data.map((assignment) => <li>
            {setSubmitID(assignment['id'])}
            {setSubmitDate(assignment['date'])}
            {setSubmitFile(assignment['file'])}
          </li>)
        )
      })
    })
  }, [])

  return(
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
      <Container maxWidth="md">
        <p className = "text"> Assignment information</p>
        <p className = "text"> title: {assignmentTitles.title}</p>
        <p className = "text"> description: {assignmentTitles.description}</p>
        <p className = "text"> due date: {assignmentTitles.due_date}</p>
        <p className = "text"> submission information</p>
        <p className = "text"> current ID:{submitID}</p>
        <p className = "text"> current ID:{submitDate}</p>
        <p className = "text"> current ID:{submitFile}</p>

        <Button variant="contained" color="primary" onClick={() => {  history.push(`/student/classrooms/${classroomID}/assignments/${id}/submitList`)}}>
          All assignments
        </Button>
      </Container>
    </div>
  )
}