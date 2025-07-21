// src/App.jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthContext } from './context/AuthContext'
import { useContext } from 'react'

import Navbar from './components/Navbar'

import Home from './pages/Home'
import TrainerDashboard from './pages/TrainerDashboard'
import StudentDashboard from './pages/StudentDashboard'
import Login from './pages/Login'
import Register from './pages/Register'
import Services from './pages/Services'
import Contact from './pages/Contact'
import ManageUser from './pages/ManageUser'
import CreateWorkout from './pages/CreateWorkout'
import EditWorkout from './pages/EditWorkout'
import AssignStudents from './pages/AssignStudents'
import StudentProgress from './pages/StudentProgress'

function PrivateRoute({ children }) {
  const { user } = useContext(AuthContext)
  return user ? children : <Navigate to="/login" />
}

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard/trainer" element={<TrainerDashboard />} />
        <Route path="/dashboard/student" element={<StudentDashboard />} />
        <Route path="/CreateWorkout" element={<CreateWorkout />} />
        <Route path="/EditWorkout" element={<EditWorkout />} />
        <Route path="/AssignStudents" element={<AssignStudents />} />
        <Route path="/StudentProgress" element={<StudentProgress />} />
        <Route path="/user/manage" element={<ManageUser />} />
        <Route path="/services" element={<Services />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </div>
  )
}

export default App


