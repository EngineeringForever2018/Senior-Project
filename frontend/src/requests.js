import axios from "axios";
import {authenticateRequest, serverUrl} from "./utils";

//Instructor requests
//classroom calls
export async function createClassroom(title, token) {
  let requestConfig = {}

  const data = {
    'title': title
  }

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(`${serverUrl()}/instructor/classrooms`, data, requestConfig)
}

export async function listClassroom(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/instructor/classrooms`, requestConfig)
}

export async function getSubmission(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}`,
    requestConfig)
}

export async function getSubmissionReport(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}/report`,
    requestConfig)
}

export async function getClassroomStudent(classroomID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/classrooms/${classroomID}/students/${id}`,
    requestConfig)
}

export async function viewClassroom(Classid, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/instructor/classrooms/${Classid}`, requestConfig)
}

export async function updateClassroom(title, id, token) {
  let requestConfig = {}

  const data = {
    'title': title
  }

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.put(`${serverUrl()}/instructor/classrooms/${id}`, data, requestConfig)
}

export async function deleteClassroom(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.delete(`${serverUrl()}/instructor/classrooms/${classroomID}`, requestConfig)
}

//assignment calls
export async function createAssignment(classroomID, title, description, dueDate, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  const data = {
    'title': title,
    'description': description,
    'due_date': dueDate,
  }

  return axios.post(`${serverUrl()}/instructor/classrooms/${classroomID}/assignments`, data, requestConfig)
}

export async function listAssignments(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments`,
    requestConfig)
}

export async function viewAssignment(classNumber, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classNumber}/assignments/${assignmentID}`, requestConfig
  )
}

export async function updateAssignment(classroomID, assignmentID, title, description, dueDate, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  const data = {
    'title': title,
    'description': description,
    'due_date': dueDate,
  }

  return axios.put(`${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}`, data, requestConfig)
}

export async function deleteAssignment(classroomID, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.delete(`${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}`, requestConfig)
}

//submitions calls
export async function listSubmissions(classroomID, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions`,
    requestConfig)
}

export async function viewSubmission(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}`,
    requestConfig)
}

export async function viewReport(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}/report`,
    requestConfig)
}

//accept submission post

//comments requests

//instructor and student requests
//classroom students
export async function joinClassroom(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(`${serverUrl()}/classrooms/${classroomID}/students`, requestConfig)
}

export async function listStudents(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/classrooms/${classroomID}/students`,
    requestConfig)
}

export async function viewStudent(classroomID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/classrooms/${classroomID}/students/${id}`,
    requestConfig)
}

export async function removeStudentFromClass(classroomID, studentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.delete(`${serverUrl()}/classrooms/${classroomID}/students/${studentID}`, requestConfig)
}

//get user info
export async function getUserInfo(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/user`, requestConfig)
}

//Student requests
//assignment calls
export async function listAssignmentsStudent(token, classNumber) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/student/classrooms/${classNumber}/assignments`, requestConfig)
}

export async function viewAssignmentStudent(classNumber, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/student/classrooms/${classNumber}/assignments/${assignmentID}`, requestConfig
  )
}

//Submissions calls
export async function postSubmit(classNumber, assignmentID, file, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  const formData = new FormData();
  formData.append('file', file);

  return axios.post(
    `${serverUrl()}/student/classrooms/${classNumber}/assignments/${assignmentID}/submissions`, formData, requestConfig
  )
}

export async function listSubmissionsStudent(classroomID, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/student/classrooms/${classroomID}/assignments/${assignmentID}/submissions`,
    requestConfig)
}

export async function viewSubmissionStudent(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/student/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}`,
    requestConfig)
}

//Other requests
//get image
export async function getFile(fileName, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}${fileName}`, requestConfig)
}
