import './InstructorHome.scss'
import React, {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import {NavBar} from "../nav/NavBar";
import {getUserData, getClassroomList, createClassroom} from "../requests";

export function InstructorHome(props) {
  return (
    <div>
      <Classrooms/>
    </div>
  )
}

function Classrooms() {
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()

  const [classroomTitles, setClassroomTitles] = useState();
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getClassroomList(token).then((response) => {
        setClassroomTitles(
          response.data.map((data) => <li>
            <button className="list-btn" onClick={() => {
              history.push(`/instructor/classrooms/${data['id']}`)
            }}>
              {data['title']}
            </button>
          </li>)
        )
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

      <div className="Instructor-Classrooms">
        <div className="background">
          <div className="title">
            <p className="text">Instructor Home</p>
          </div>
          <div className="scroll">
            <ul className="list-titles">
              {classroomTitles}
            </ul>
          </div>
          <div className="options">
            <button onClick={() => {  history.push('/create-classroom')}}>
              Create Classroom
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export function CreateClassroomForm() {
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()

  const [title, setTitle] = useState("");
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  function handleChange(event) {
    setTitle(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createClassroom(title, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
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

    <div className="Instructor-Classroom-Create">
      <div className="form-background">
        <div className="form-title">
          <p className="form-text">Create Assignment</p>
        </div>

        <form onSubmit={handleSubmit}>
          <label>
            Title: <input type="text" value={title} onChange={handleChange}/>
          </label>
          <input type="submit" value="Submit"/>
        </form>
      </div>
    </div>
  </div>
  )
}