// import {useLocation} from 'react-router-dom';
import React from "react";
import './ReportScreen.scss'
import {useHistory, useLocation, useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import {getSubmissionReport} from "../requests";

function ReportScreen() {
  const {getAccessTokenSilently} = useAuth0()

  const location = useLocation()
  const history = useHistory()

  const {classroomID, assignmentID, id} = useParams()

  let report = undefined

  if (location.state !== undefined) {
    report = location.state.report
  }

  if (report === undefined) {
    getAccessTokenSilently().then((token) => {
      getSubmissionReport(classroomID, assignmentID, id, token).then((response) => {
        history.push(location.pathname, {report: response.data})
      }, (error) => console.log(error.response))
    })

    return (
      <div/>
    )
  } else {
    const authorshipProbability = report['authorship_probability']
    const flag = report['flag']


    if (flag) {
      return (
        <BadReportScreen authorshipProbability={authorshipProbability}/>
      )
    } else {
      return (
        <GoodReportScreen authorshipProbability={authorshipProbability}/>
      )
    }
  }
}

function BadReportScreen(props) {
  const authorshipProbability = props.authorshipProbability

  return (
    <div className="BadReportScreen">
      <p>Bad</p>
      <p>{authorshipProbability}</p>
    </div>
  )
}

function GoodReportScreen(props) {
  const authorshipProbability = props.authorshipProbability

  return (
    <div className="GoodReportScreen">
      <p>{authorshipProbability}</p>
    </div>
  )
}

export default ReportScreen;