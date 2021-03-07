import './PostSubmit.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserData, viewAssignment} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function PostSubmit() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

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

  //run to get assignment and user data on page load
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      viewAssignment( classroomID,id, token).then((response) => {
        setAssignmentTitles(prevState => ({
          ...prevState,
          id: response.data.id,
          classroom: response.data.classroom,
          title: response.data.title,
          description: response.data.description,
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

  return(
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
      <div className = "StudentPostSubmit">
        <div className = "background">
          <p className = "text"> title: {assignmentTitles.title}</p>
          <p className = "text"> description: {assignmentTitles.description}</p>
          <p className = "text"> due date: {assignmentTitles.due_date}</p>
        </div>
      </div>
    </div>
  )
}