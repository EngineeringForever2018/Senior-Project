
import axios from "axios";
import {authenticateRequest, serverUrl} from "./utils";

export async function getUserData(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/user`, requestConfig)
}
//instructor
export async function getClassrooms(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/instructor/classrooms`, requestConfig)
}

export async function createClassroom(title, token) {
  let requestConfig = {}

  const data = {
    'title': title
  }

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(`${serverUrl()}/instructor/classrooms`, data, requestConfig)
}

export async function deleteClassroom(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.delete(`${serverUrl()}/instructor/classrooms/${classroomID}`, requestConfig)
}

//student functions
export async function getAssignments(token, classNumber) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/student/classrooms/${classNumber}/assignments`, requestConfig)
}

export async function viewAssignment(assignmentID, classNumber , token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/student/classrooms/${classNumber}/assignments/1${assignmentID}`, requestConfig)
}

export async function createEssay(title, token) {
  let requestConfig = {}

  const data = {
    'title': title
  }

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(`${serverUrl()}/student/classrooms/10/assignments/1/submissions`, data, requestConfig)
}