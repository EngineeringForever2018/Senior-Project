import './StudentAssignment.scss'
import React, {useEffect, useState} from "react";
import {NavBar} from "../nav/NavBar";
import {getUserInfo, viewAssignmentStudent, postSubmit} from "../requests";
import {useHistory, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";

//open assignment
export function StudentAssignment() {
  const {getAccessTokenSilently} = useAuth0()
  const history = useHistory()
  const {classroomID, id} = useParams()

  var date = new Date().getDate(); //To get the Current Date
  var month = new Date().getMonth() + 1; //To get the Current Month
  var year = new Date().getFullYear(); //To get the Current Year
  var hours = new Date().getHours(); //To get the Current Hours

  const [onTime, setOnTime] = useState("Over Due")
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
      viewAssignmentStudent( classroomID,id, token).then((response) => {
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

  useEffect(() => {
    var date = (assignmentTitles.due_date).split("-")
    console.log(parseInt(date[0], 10))
    if(parseInt(date[0], 10) > year) {
      setOnTime("on time over year")
    } else if (parseInt(date[0], 10) == year) {
      if(parseInt(date[1], 10) <= month) {
        setOnTime("not on time month")
      }
      if(parseInt(date[2], 10) <= date) {
        setOnTime("not on time day")
      }
    }
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
    console.log(file)
    getAccessTokenSilently().then((token) => {
      postSubmit(classroomID,id, file, token).then((response) => {
        history.push(`/student/classrooms/${classroomID}/assignments/${id}/submit`)
      }, (error) => console.log(error.response))
    })
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