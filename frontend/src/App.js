import './App.scss';
import {Route,} from 'react-router-dom';
import {Switch} from 'react-router';
import React from "react";
import {Home} from "./Home";
import {CreateClassroomForm} from "./instructor/InstructorHome";
import {CreateEssayForm} from "./student/StudentHome";
import About from "./About";

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
      <Route exact path="/submit-essay" component={CreateEssayForm}/>
      <Route exact path="/about" component={About}/>
    </Switch>
  )
}

export default App;