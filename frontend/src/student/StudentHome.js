import './StudentHome.scss'
import {NavBar} from "../nav/NavBar";

import React, {useEffect, useState} from "react";

import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import {getUserInfo, listAssignmentsStudent, joinClassroom} from "../requests";

export function StudentHome(props) {
  return (
    <div>
      <NavBar firstName={props.userData['first_name']} lastName={props.userData['last_name']}/>
      <Essay />
    </div>
  )
}

//load all essays
function Essay() {
  const {getAccessTokenSilently} = useAuth0();
  const history = useHistory()
  const [essaysTitles, setEssaysTitles] = useState();
  const [classNumber, setClassNumber] = useState(1);

  function handleSetClassNumber(e) {
    setClassNumber(e.target.value);
  }

  //used for scroll down menu for classes
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      listAssignmentsStudent(token, classNumber).then((response) => {
        setEssaysTitles(
          response.data.map((data) => <li>
            <button className="assignment-btn" onClick={() => {
              history.push(`/student/classrooms/${classNumber}/assignments/${data['id']}`)
            }}>
              {data['title']}
            </button>
          </li>)
        )
      })
    })
  }, [classNumber])

  return (
    <div className = "Assignments">
      <div className = "background">
        <div className = "Text">
          {/*no command for student to get classes to temporary hard code */}
          <label>Class number input: </label>
          <select defaultValue={classNumber} onChange={handleSetClassNumber}>
            <option value = "1" > class 1 </option>
            <option value = "2"> class 2 </option>
            <option value = "3"> class 3 </option>
            <option value = "10"> class 10 </option>
          </select>
        </div>

        <div className="assignment-title">
          <div className="assignment-background">
            <p className="assignment-text">list of assignments</p>
          </div>
          <div className="assignment-scroll">
            <ul className="assignment-name">
              {essaysTitles}
            </ul>
          </div>
        </div>

        <div>
        <button onClick={() => {  history.push('/join-classroom')}}>
          Join Classroom
        </button>

        </div>
      </div>
    </div>
  )
}

//function to create assignment
export function JoinClassroomForm(props) {
  const {getAccessTokenSilently} = useAuth0()

  const [id, setID] = useState()
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })

  const history = useHistory()

  function handleIDChange(event) {
    setID(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      joinClassroom(id, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }
  
  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getUserInfo(id , token).then((response) => {
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
            <p className="form-text">Join Classroom</p>
          </div>

          <form onSubmit={handleSubmit}>
            <label>
              classNumber: 
              <input type="number" value={id} onChange={handleIDChange}/>
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