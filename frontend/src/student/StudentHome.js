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
  const [classNumber, setClassNumber] = useState(10);
  const [currentAssignment, setCurrentAssignment] = useState();

  function handleSetClassNumber(e) {
    setClassNumber(e.target.value);
    console.log(classNumber)
    
    getAccessTokenSilently().then((token) => {
      getAssignments(token, classNumber).then((response) => {
        setEssaysTitles(
          response.data.map((data) => <li>
            <button onClick={() => {
              viewAssignment(data['id'], classNumber, token).then(() => history.push('/'), (error) => console.log(error.response))
            }}>
              {data['title']}
            </button>
          </li>)
        )
      })
    })
  }

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getAssignments(token, classNumber).then((response) => {
        setEssaysTitles(
          response.data.map((data) => <li>
            <button onClick={() => {
              viewAssignment(data['id'], classNumber, token).then(() => history.push('/'), (error) => console.log(error.response))
            }}>
              {data['title']}
            </button>
          </li>)
        )
      })
    })
  }, [])

  return (
    <div>
      <form>
        <div>
          <label>Class number input: </label>
          <select defaultValue={classNumber} onChange={handleSetClassNumber}>
            <option value = "1" > class 1 </option>
            <option value = "2"> class 2 </option>
            <option value = "3"> class 3 </option>
            <option value = "10"> class 10 </option>
          </select>
        </div>
      </form>
      <div>
        list of assignments
          {essaysTitles}
      </div>

      Submit assignment
      <button onClick={() => {
        history.push('/submit-essay')
      }}
        >Create Essay
      </button>
    </div>
  )
}

//handler for submit
export function CreateEssayForm() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState("");
  const {getAccessTokenSilently} = useAuth0();

  const history = useHistory()

  function handleChange(event) {
    setTitle(event.target.value);
    setFile(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createEssay(title, file, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input type="text" value={title} onChange={handleChange}/>
      </label>
      <div>
        Submit file:
        <input type="file" value={file}  onChange={handleChange}/>
      </div>
      <input type="submit" value="Submit"/>
    </form>
  )
}