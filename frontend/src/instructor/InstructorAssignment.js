import './InstructorAssignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, deleteAssignment, updateAssignment, viewAssignment} from "../requests";
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

export function InstructorAssignment() {
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

      <div className = "Instructor-Assignment-Info">
        <div className="background">
          <div className="title">
            <p className="text">Assignment Info</p>
          </div>

          <div className="body-text">
            <p className = "text"> title: {assignmentTitles.title}</p>
            <p className = "text"> due date: {assignmentTitles.due_date}</p>
            <p className = "text"> description: {assignmentTitles.description}</p>
          </div>

          <div className="options-test">

            <button onClick={() => {
              history.push(`/instructor/classrooms/${classroomID}/assignments/${id}/submissions`)
            }}>List Submissions</button>

            <button onClick={() => {
              getAccessTokenSilently().then((token) => {
              deleteAssignment(classroomID, id, token).then(() =>
              history.push('/instructor/classroom/1'), (error) => console.log(error.response))
              }, (error) => console.log(error))
            }}>Delete</button>

            <button onClick={() => {
              history.push('/update-assignment', 
              {classroomID: assignmentTitles.id,
              assignmentID: assignmentTitles.classroom})
            }}>Update Assignment</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export function UpdateAssignmentForm(props) {
  const location = useLocation()

  const Cid = location.state.classroomID
  const Aid = location.state.assignmentID

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
      viewAssignment( Cid, Aid, token).then((response) => {
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
    })
    setTitle(assignmentTitles.title)
    setDescription(assignmentTitles.description)
  }, [])

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
      updateAssignment(Cid, Aid, title, description, {
        'year': parseInt(dueYear),
        'month': parseInt(dueMonth),
        'day': parseInt(dueDay),
        'hour': parseInt(dueHour),
        'minute': parseInt(dueMinute)
      }, token).then((response) => {
        history.push(`/instructor/classrooms/${Aid}/assignments/${Cid}`)
      }, (error) => console.log(error.response))
    })
    event.preventDefault()
  }

  return (
    <div>
      <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>

      <div className="Instructor-Assignment-Update">
        <div className="form-background">
          <div className="form-title">
            <p className="form-text">Update Assignment</p>
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