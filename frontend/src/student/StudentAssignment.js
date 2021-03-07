import './StudentAssignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserData, viewAssignment, SubmitEssay} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

//open assignment
export function StudentAssignment() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

  const [assignmentTitles, setAssignmentTitles] = useState({
    id: '',
    classroom: '',
    title: '',
    discription: '',
    due_date: ''
  })
  const [userInfo, setUserInfo] = useState({
    first_name:'',
    last_name:''
  })
  const [file, setFile] = React.useState("");

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

  //code to upload file automaticly uploads after file put in
  function handleUpload(event) {
    setFile(event.target.files[0]);
    event.preventDefault()
  }

  const ImageThumb = ({ image }) => {
    return <img src={URL.createObjectURL(image)} alt={image.name}  className = "essayImage"/>;
  };

  function submitButton(event){
    getAccessTokenSilently().then((token) => {
      SubmitEssay(classroomID,id, file, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    history.push(`/student/classrooms/${classroomID}/assignments/${id}/submit`)

    event.preventDefault()
  }

  return (
      <div>
        <NavBar firstName={userInfo.first_name} lastName={userInfo.last_name}/>
        <div className = "StudentAssignments">
          <div className = "background">
            <p className = "text"> title: {assignmentTitles.title}</p>
            <p className = "text"> description: {assignmentTitles.description}</p>
            <p className = "text"> due date: {assignmentTitles.due_date}</p>

            <input type="file" onChange={handleUpload} />
            <p>Filename: {file.name}</p>
            <p>File type: {file.type}</p>
            {file && <ImageThumb image={file} />}

            <div/>
            <button onClick={submitButton}>
              submit
            </button>

          </div>
        </div>
      </div>
  )
}