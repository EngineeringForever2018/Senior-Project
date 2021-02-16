import './Assignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserData, viewInstructorAssignment} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function Assignment() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

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

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewInstructorAssignment( classroomID,id, token).then((response) => {
        setAssignmentTitles(prevState => ({
          ...prevState,
          id: response.data.id,
          classroom: response.data.classroom,
          title: response.data.title,
          discription: response.data.discription,
          due_date: response.data.due_date
        }));
      })
      getUserData(token).then((response) => {
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
      <div className = "Assignments">
        <div className = "background">
          <div className = "background-title">
            Assignments
          </div>
          <p className = "text"> title: {assignmentTitles.title}</p>
          <p className = "text"> due date: {assignmentTitles.due_date}</p>
          <p className = "text"> discription: {assignmentTitles.discription}</p>
        </div>
      </div>
    </div>
  )
}