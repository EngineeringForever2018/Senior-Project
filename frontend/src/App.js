import './App.scss';
import {Route,} from 'react-router-dom';
import {Switch} from 'react-router';
import React from "react";
import {Home} from "./Home";
import {CreateClassroomForm} from "./instructor/InstructorHome";
import {CreateEssayForm} from "./student/StudentHome";
import About from "./About";
import ReportScreen from "./instructor/ReportScreen";
import {Classroom, CreateAssignmentForm} from "./instructor/Classroom";
import {Assignment} from "./instructor/Assignment";

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
      <Route exact path="/create-assignment" component={CreateAssignmentForm}/>
      <Route exact path="/submit-essay" component={CreateEssayForm}/>
      <Route exact path="/about" component={About}/>
      <Route exact path="/instructor/classrooms/:id" component={Classroom}/>
      <Route exact path="/instructor/classrooms/:classroomID/assignments/:id" component={Assignment}/>
      <Route exact path="/instructor/classrooms/:classroomID/assignments/:assignmentID/submissions/:id/report"
             component={ReportScreen}/>
    </Switch>
  )
}

export default App;