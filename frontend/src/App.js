import './App.scss';
import {Route,} from 'react-router-dom';
import {Switch} from 'react-router';
import React from "react";
import {Home} from "./Home";
import {CreateClassroomForm} from "./instructor/InstructorHome";
import About from "./About";
import ReportScreen from "./instructor/ReportScreen";

function App() {
  return (
    <Main/>
  );
}

function Main() {
  return (
    <Switch>
      <Route exact path="/" component={Home}/>
      <Route exact path="/create-classroom" component={CreateClassroomForm}/>
      <Route exact path="/about" component={About}/>
      <Route exact path="/instructor/classrooms/:classroomID/assignments/:assignmentID/submissions/:id/report"
             component={ReportScreen}/>
    </Switch>
  )
}

export default App;
