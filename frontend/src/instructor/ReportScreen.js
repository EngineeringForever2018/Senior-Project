// import {useLocation} from 'react-router-dom';
import React from "react";
import './ReportScreen.scss'
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import {getClassroomStudent, getSubmission, getSubmissionReport} from "../requests";
import {NavBar} from "../nav/NavBar";

function ReportScreen() {
  const {getAccessTokenSilently} = useAuth0()

  const location = useLocation()
  const history = useHistory()

  const {classroomID, assignmentID, id} = useParams()

  let report = undefined
  let studentInfo = undefined

  if (location.state !== undefined) {
    report = location.state.report
    studentInfo = location.state.studentInfo
  }

  if (report === undefined) {
    getAccessTokenSilently().then((token) => {
      getSubmissionReport(classroomID, assignmentID, id, token).then((response) => {
        getSubmission(classroomID, assignmentID, id, token).then((submissionResponse) => {
          const studentID = submissionResponse.data['student']
          getClassroomStudent(classroomID, studentID, token).then((studentResponse) => {
            history.push(location.pathname, {report: response.data, studentInfo: studentResponse.data})
          }, (error) => console.log(error.response))
        }, (error) => console.log(error.response))
      }, (error) => console.log(error.response))
    })

    return (
      <div/>
    )
  } else {
    const authorshipProbability = report['authorship_probability']
    const studentFirstName = studentInfo['first_name']
    const studentLastName = studentInfo['last_name']

    const flag = report['flag']


    if (flag) {
      return (
        <BadReportScreen authorshipProbability={authorshipProbability} studentFirstName={studentFirstName}
                         studentLastName={studentLastName}/>
      )
    } else {
      return (
        <GoodReportScreen authorshipProbability={authorshipProbability} studentFirstName={studentFirstName}
                          studentLastName={studentLastName}/>
      )
    }
  }
}

function BadReportScreen(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName

  return (
    <div className="BadReportScreen">
      <NavBar firstName="Mary" lastName="Berry"/>
      <div className="panel">
        <div className="submission-info">
          <div className="student-info">
            <p className="student-info-txt">{`Name: ${studentFirstName} ${studentLastName}`}</p>
            <p className="student-info-txt">Potential reasons for discrepancy:</p>
            <ul className="discrepancy-reasons">
              <li><p className="student-info-txt">Large difference in sentence lengths.</p></li>
              <li><p className="student-info-txt">Sudden and large improvement in grammar.</p></li>
            </ul>
          </div>
          <p className="consistency-score">{`Consistency Score: ${authorshipProbability * 100}%`}</p>
          <div className="percentage-bar"/>
          <div className="additional-buttons">
            <button className="btn additional-stats-btn">Additional Statistics</button>
            <button className="btn accept-essay-btn">Add Essay to File</button>
          </div>
        </div>
        <div className="essay-display">
          <p className="student-info-txt">The essay will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}

function GoodReportScreen(props) {
  const authorshipProbability = props.authorshipProbability
  const studentFirstName = props.studentFirstName
  const studentLastName = props.studentLastName

  return (
    <div className="GoodReportScreen">
      <NavBar firstName="Mary" lastName="Berry"/>
      <div className="panel">
        <div className="submission-info">
          <div className="student-info">
            <p className="student-info-txt">{`Name: ${studentFirstName} ${studentLastName}`}</p>
            <p className="student-info-txt">No issues here!</p>
          </div>
          <p className="consistency-score">{`Consistency Score: ${authorshipProbability * 100}%`}</p>
          <div className="percentage-bar"/>
          <div className="additional-buttons">
            <button className="btn additional-stats-btn">Additional Statistics</button>
            <button className="btn accept-essay-btn">Add Essay to File</button>
          </div>
        </div>
        <div className="essay-display">
          <p className="student-info-txt">The essay will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}

export default ReportScreen;