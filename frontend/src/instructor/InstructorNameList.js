import './InstructorNameList.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, newViewClassroom, listStudents, removeStudentFromClass, getData} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

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

export function InstructorNameList() {
  const classes = useStyles();
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id} = useParams()

  const [currentStudent, setCurrentStudent] = useState(0)
  const [studentList, setStudentList] = useState()
  const [openCurrent, setOpenCurrent] = useState(true);
  const initialName = [{
    id:'',
    first_name: '',
    last_name:'',
  }]

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [classInfo, setClassinfo] = useState({
    title:'',
    students:''
  })

  const [studentArr, setStudentArr] = useState()
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listStudents(id, token).then((response) => {
        setStudentList(
          response.data.map((assignment) => <li>
            <ListItem button onClick={() => {
              setCurrentStudent(assignment['id'])}
            } className={classes.nested} >
              <ListItemIcon>
                <InsertDriveFile />
              </ListItemIcon>
              <ListItemText primary={assignment['id']} />
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
        setStudentArr(
          response.data.students.map((test) => <li>
            <ListItem button onClick={() => {setCurrentStudent(test['id'])}}>
              {test['first_name']}  {test['last_name']}
            </ListItem>
          </li>)
        )
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

      <Container maxWidth="md">
        <Box height={50} />
        <Typography variant="h3" align="center">
          Classroom Students List: {classInfo.title}
        </Typography>
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
              {studentArr}
            </Collapse>
          </List>
        </Box>

        <Box height={30} />
        <Box mx="auto" bgcolor="background.paper" borderRadius="borderRadius" p={1}>
          <Typography variant="h6">
            Instructor Options:
          </Typography>
          <Button variant="contained" color="primary" onClick={() => {
            getAccessTokenSilently().then((token) => {
              removeStudentFromClass(id, currentStudent, token).then(() => history.go(0), (error) => console.log(error.response))
            }, (error) => console.log(error))
            }}>Delete Student</Button>

            <Button variant="contained" color="primary" onClick={() => {
              history.push(`/instructor/classrooms/${id}`, {classroomID: id})
            }}>Return</Button>
          </Box>
      </Container>
    </div>
  )
}