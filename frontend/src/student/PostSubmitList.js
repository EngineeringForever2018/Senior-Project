import './PostSubmitList.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignmentStudent, listSubmissionsStudent, getFile} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

//matirial-ui imports
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import Container from '@material-ui/core/Container';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
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

export function PostSubmitList() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()
  const classes = useStyles();

  const [currentFile, setCurrentFile] = useState()
  const [currentID, setCurrentID] = useState()
  const [submitList, setSubmitList] = useState();
  const [openCurrent, setOpenCurrent] = useState(true);

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

            <ListItem button onClick={() => {
              setCurrentID(assignment['id'])
              setCurrentFile(assignment['file'])
            }} className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={assignment['file']} />
            </ListItem>
          </li>)
        )
      })
    })
  }, [])

  const handleClickOpen = () => {
    setOpenCurrent(!openCurrent);
  };

  var boxSpace = 30;
  const boxCol = grey[300]

  return(
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <Container maxWidth="md">
      <Box height={boxSpace} />

      <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
        <Typography variant="h6">
          Assignment Info
        </Typography>
        <p className = "text"> title: {assignmentTitles.title}</p>
        <p className = "text"> description: {assignmentTitles.description}</p>
        <p className = "text"> due date: {assignmentTitles.due_date}</p>
        <p className = "text"> current ID:{currentID}</p>
        <p className = "text"> current file:{currentFile}</p>
      </Box>

      <Box height={boxSpace} />
        <Box mx="auto" bgcolor="background.paper" p={1}>
          <Box bgcolor={boxCol}>
            <ListItem button onClick={handleClickOpen}>
              <ListItemText primary="Current Assignments" />
              {openCurrent ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
          </Box>

          <List component="div" disablePadding>
            <Collapse in={openCurrent} timeout="auto" unmountOnExit>
              {submitList}
            </Collapse>
          </List>
        </Box>
      </Container>
    </div>
  )
}