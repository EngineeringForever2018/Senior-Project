import './InstructorClassrooms.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewClassroom, listAssignments, createAssignment, deleteClassroom, updateClassroom} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function InstructorClassroom() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {id} = useParams()

  const [assignmentTitles, setAssignmentTitles] = useState()
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [classInfo, setClassinfo] = useState({
    title:''
  })

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listAssignments(id, token).then((response) => {
        setAssignmentTitles(
          response.data.map((assignment) => <li>
            <button className="list-btn" onClick={() => {
              history.push(`/instructor/classrooms/${id}/assignments/${assignment['id']}`)
            }}>
              {assignment['title']}
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

        <div className="Instructor-Assignment">
          <div className="background">
            <div className="title">
              <p className="text">Classroom: {classInfo.title}</p>
            </div>

            <div className="scroll">
              <ul className="titles">
                {assignmentTitles}
              </ul>
            </div>

            <div className="options">

              <button onClick={() => {
                history.push(`/update-classroom`, {classID: id})
              }}>Update Classroom</button>

              <button onClick={() => {
                history.push(`/instructor/classrooms/${id}/students`, {classroomID: id})
              }}>List Students</button>

              <button onClick={() => {
                getAccessTokenSilently().then((token) => {
                deleteClassroom(id, token).then(() => history.push('/'), (error) => console.log(error.response))
                }, (error) => console.log(error))
              }}>Delete</button>

              <button onClick={() => {
                history.push(`/create-assignment`, {classroomID: id})
              }}>Create Assignment</button>

            </div>
          </div>
        </div>
    </div>
  )
}

//form to update classroom
export function UpdateClassroomForm() {
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()
  const location = useLocation()
  const id = location.state.classID

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
      updateClassroom(title, id, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getUserInfo(token).then((response) => {
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
          <p className="form-text">Update Classroom</p>
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

//function to create assignment
export function CreateAssignmentForm(props) {
  const location = useLocation()
  const id = location.state.classroomID

  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [dueYear, setDueYear] = useState("")
  const [dueMonth, setDueMonth] = useState("")
  const [dueDay, setDueDay] = useState("")
  const [dueHour, setDueHour] = useState("")
  const [dueMinute, setDueMinute] = useState("")
  const {getAccessTokenSilently} = useAuth0()

  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  const history = useHistory()

  function handleTitleChange(event) {
    setTitle(event.target.value);
  }

  function handleDescriptionChange(event) {
    setDescription(event.target.value)
  }

  function handleDueYearChange(event) {
    setDueYear(event.target.value)
  }

  function handleDueMonthChange(event) {
    setDueMonth(event.target.value)
  }

  function handleDueDayChange(event) {
    setDueDay(event.target.value)
  }

  function handleDueHourChange(event) {
    setDueHour(event.target.value)
  }

  function handleDueMinuteChange(event) {
    setDueMinute(event.target.value)
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createAssignment(id, title, description, {
        'year': parseInt(dueYear),
        'month': parseInt(dueMonth),
        'day': parseInt(dueDay),
        'hour': parseInt(dueHour),
        'minute': parseInt(dueMinute)
      }, token).then((response) => {
        history.push(`/instructor/classrooms/${id}`)
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getUserInfo(token).then((response) => {
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

      <div className="Instructor-Assignment-Create">
        <div className="form-background">
          <div className="form-title">
            <p className="form-text">Create Assignment</p>
          </div>

          <form onSubmit={handleSubmit}>
            <label>
              Title:
              <input type="text" value={title} onChange={handleTitleChange}/>
            </label>
            <div/>
            <label>
              Description:
              <input type="text" value={description} onChange={handleDescriptionChange}/>
            </label>
            <p>Due Date:</p>
            <label>
              Year:
              <input type="text" value={dueYear} onChange={handleDueYearChange}/>
            </label>
            <label>
              Month:
              <input type="text" value={dueMonth} onChange={handleDueMonthChange}/>
            </label>
            <label>
              Day:
              <input type="text" value={dueDay} onChange={handleDueDayChange}/>
            </label>
            <label>
              Hour:
             <input type="text" value={dueHour} onChange={handleDueHourChange}/>
            </label>
            <label>
              Minute:
              <input type="text" value={dueMinute} onChange={handleDueMinuteChange}/>
            </label>
            <div>
              <input type="submit" value="Submit"/>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}