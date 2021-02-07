import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {createAssignment, createClassroom, deleteClassroom, getInstructorAssignments} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function Classroom() {
  const {getAccessTokenSilently} = useAuth0()

  const [assignmentTitles, setAssignmentTitles] = useState()

  const history = useHistory()

  const {id} = useParams()

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getInstructorAssignments(id, token).then((response) => {
        setAssignmentTitles(
          response.data.map((assignment) => <li>
            <button className="assignment-btn" onClick={() => {
              history.push(`/instructor/classrooms/${id}/assignments/${assignment['id']}`)
            }}>
              {assignment['title']}
            </button>
          </li>)
        )
      })
    })
  }, [])

  return (
    <div className="Classroom">
      <NavBar firstName="Mary" lastName="Berry"/>
      <ul className="assignment-titles">
        {assignmentTitles}
      </ul>
      <button className="btn create-assignment-btn" onClick={() => {
        history.push('/create-assignment', {classroomID: id})
      }}>
        Create Assignment
      </button>
      <button className="btn delete-classroom-btn" onClick={() => {
        getAccessTokenSilently().then((token) => {
          deleteClassroom(id, token).then(() => history.push('/'), (error) => console.log(error.response))
        }, (error) => console.log(error))
      }}>Delete</button>
    </div>
  )
}

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

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input type="text" value={title} onChange={handleTitleChange}/>
      </label>
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
      <input type="submit" value="Submit"/>
    </form>
  )
}