import './InstructorNameList.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewClassroom, listStudents, removeStudentFromClass} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function InstructorNameList() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id} = useParams()

  const [currentStudent, setCurrentStudent] = useState()
  const [studentList, setStudentList] = useState()
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [classInfo, setClassinfo] = useState({
    title:''
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listStudents(id, token).then((response) => {
        setStudentList(
          response.data.map((assignment) => <li>
            <button className="list-btn" onClick={() => {
              setCurrentStudent(assignment['id'])}
            }>
              {assignment['id']}
            </button>
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
      viewClassroom(id, token).then((response) => {
        setClassinfo(prevState => ({
          ...prevState,
          title: response.data.title,
        }));
      })
    })
  }, [])

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
        <div className="Instructor-NameList">
          <div className="background">
            <div className="title">
              <p className="text">Classroom Students List: {classInfo.title}</p>
            </div>

            <div className="scroll">
              <ul className="titles">
                {studentList}
              </ul>
            </div>

            <div className="options">

              <button onClick={() => {
                getAccessTokenSilently().then((token) => {
                  removeStudentFromClass(id, currentStudent, token).then(() => history.go(0), (error) => console.log(error.response))
                }, (error) => console.log(error))
              }}>Delete Student</button>

              <button onClick={() => {
                history.push(`/instructor/classrooms/${id}`, {classroomID: id})
              }}>Return</button>

            </div>
          </div>
        </div>
    </div>
  )
}