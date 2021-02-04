import axios from "axios";
import {authenticateRequest, serverUrl} from "./utils";

export async function getUserData(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/user`, requestConfig)
}

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

export async function getSubmissionReport(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}/report`,
    requestConfig)
}