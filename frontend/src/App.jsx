// src/App.jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthContext } from './context/AuthContext'
import { useContext } from 'react'

import Navbar from './components/Navbar'

import Home from './pages/Home'
//import TrainerDashboard from './pages/TrainerDashboard'
//import StudentDashboard from './pages/StudentDashboard'
import Login from './pages/Login'
import Register from './pages/Register'
import Services from './pages/Services'
import Contact from './pages/Contact'

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
        <Route path="/services" element={<Services />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </div>
  )
}

export default App


//        <Route path="/dashboard/trainer" element={<TrainerDashboard />} />
//        <Route path="/dashboard/student" element={<StudentDashboard />} />