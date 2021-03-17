import './PostSubmit.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignmentStudent, listSubmissionsStudent, viewSubmissionStudent} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

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
      <div className = "StudentPostSubmit">
        <div className = "background">
          <p className = "text"> assignment information</p>
          <p className = "text"> title: {assignmentTitles.title}</p>
          <p className = "text"> description: {assignmentTitles.description}</p>
          <p className = "text"> due date: {assignmentTitles.due_date}</p>
          <p className = "text"> submission information</p>
          <p className = "text"> current ID:{submitID}</p>
          <p className = "text"> current ID:{submitDate}</p>
          <p className = "text"> current ID:{submitFile}</p>
          <button onClick={() => {  history.push(`/student/classrooms/${classroomID}/assignments/${id}/submitList`)}}>
            All assignment
          </button>
        </div>
      </div>
    </div>
  )
}