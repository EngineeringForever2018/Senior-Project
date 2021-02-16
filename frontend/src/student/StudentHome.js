import './StudentHome.scss'
import {NavBar} from "../nav/NavBar";

import React, {useEffect, useState} from "react";

import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import axios from "axios";
import {createEssay, getAssignments, viewAssignment} from "../requests";

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
      getAssignments(token, classNumber).then((response) => {
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
      </div>
    </div>
  )
}