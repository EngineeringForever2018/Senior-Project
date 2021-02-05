// import {useLocation} from 'react-router-dom';
import React from "react";
import './ReportScreen.scss'

function ReportScreen(props) {
  const { probabilityOfAuthorship, flag } = props.location.state;

  if (flag) {
    return (
      <BadReportScreen probabilityOfAuthorship={probabilityOfAuthorship}/>
    )
  } else {
    return (
      <GoodReportScreen probabilityOfAuthorship={probabilityOfAuthorship}/>
    )
  }
}

function BadReportScreen(props) {
  const probabilityOfAuthorship = props.probabilityOfAuthorship

  // @Noah: Write this HTML, and then the CSS for it in ReportScreen.scss
  return (
    <div className="BadReportScreen">
      <p>{probabilityOfAuthorship}</p>
    </div>
  )
}

function GoodReportScreen(props) {
  const probabilityOfAuthorship = props.probabilityOfAuthorship

  // @Noah: Write this HTML, and then the CSS for it in ReportScreen.scss
  return (
    <div className="GoodReportScreen">
      <p>{probabilityOfAuthorship}</p>
    </div>
  )
}

export default ReportScreen;