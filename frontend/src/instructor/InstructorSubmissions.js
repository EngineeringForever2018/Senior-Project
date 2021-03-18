import './InstructorSubmissions.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignment, listSubmissions} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function InstructorSubmissionsList() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id, classroomID} = useParams()
  
  const [currentStudent, setCurrentStudent] = useState()
  const [submissionList, setSubmissionList] = useState()
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
            <button className="list-btn" onClick={() => {history.push(`/instructor/classrooms/${classroomID}/assignments/${id}/submissions/${assignment['id']}/report`)}
            }>
              {assignment['id']}
            </button>
          </li>)
        )
      })
    })

  }, [])

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
        <div className="Instructor-SubmissionsList">
          <div className="background">
            <div className="title">
              <p className="text">List of assignment submissions: {assignmentInfo.title} ; current Student: {currentStudent}</p>
            </div>

            <div className="scroll">
              <ul className="titles">
                {submissionList}
              </ul>
            </div>

            <div className="options">

            </div>
          </div>
        </div>
    </div>
  )
}
