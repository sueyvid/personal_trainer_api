// src/pages/AssignStudents.jsx
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function AssignStudents() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [students, setStudents] = useState([])
  const [selected, setSelected] = useState([])

  useEffect(() => {
    api.get('/users/students') // Supondo que haja essa rota
      .then((res) => setStudents(res.data))
      .catch(() => alert('Erro ao carregar estudantes'))
  }, [])

  const toggleStudent = (studentId) => {
    setSelected((prev) =>
      prev.includes(studentId) ? prev.filter((id) => id !== studentId) : [...prev, studentId]
    )
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.patch(`/workouts/${id}/assign`, { student_ids: selected })
      alert('Estudantes vinculados com sucesso!')
      navigate(`/workouts/${id}`)
    } catch {
      alert('Erro ao vincular estudantes')
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Vincular Estudantes ao Treino #{id}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <ul className="space-y-2">
          {students.map((student) => (
            <li key={student.id} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={selected.includes(student.id)}
                onChange={() => toggleStudent(student.id)}
              />
              <label>{student.name || `Estudante #${student.id}`}</label>
            </li>
          ))}
        </ul>
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Confirmar Vinculação
        </button>
      </form>
    </div>
  )
}