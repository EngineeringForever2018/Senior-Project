import './InstructorSubmissions.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignment, listSubmissions} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

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

export function InstructorSubmissionsList() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id, classroomID} = useParams()
  
  const [submissionList, setSubmissionList] = useState()
  const [openCurrent, setOpenCurrent] = useState(true);

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [assignmentInfo, setAssignmentinfo] = useState({
    title:''
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
      viewAssignment(classroomID, id, token).then((response) => {
        setAssignmentinfo(prevState => ({
          ...prevState,
          title: response.data.title,
        }));
      })
      listSubmissions(classroomID, id, token).then((response) => {
        setSubmissionList(
          response.data.map((assignment) => <li>
            <ListItem button onClick={() => {
              history.push(`/instructor/classrooms/${classroomID}/assignments/${id}/submissions/${assignment['id']}/report`)}
            } className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={assignment['id']} />
            </ListItem>
          </li>)
        )
      })
    })

  }, [])

  const handleClickOpen = () => {
    setOpenCurrent(!openCurrent);
  };

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <Container maxWidth="md">
        <p className="text">{assignmentInfo.title}</p>
        <Box mx="auto" bgcolor="background.paper" p={1}>
          <ListItem button onClick={handleClickOpen}>
            <ListItemText primary={`List of assignment submissions`}/>
            {openCurrent ? <ExpandLess /> : <ExpandMore />}
          </ListItem>

          <List component="div" disablePadding>
            <Collapse in={openCurrent} timeout="auto" unmountOnExit>
              {submissionList}
            </Collapse>
          </List>
        </Box>
      </Container>
    </div>
  )
}
