// src/pages/TrainerDashboard.jsx
import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function TrainerDashboard() {
  const [authorized, setAuthorized] = useState(null)
  const [workouts, setWorkouts] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const role = localStorage.getItem('role')
    if (role === 'trainer') {
      setAuthorized(true)
    } else {
      setAuthorized(false)
    }
  }, [])

  useEffect(() => {
    if (authorized) {
      api
        .get('/workouts/')
        .then((res) => setWorkouts(res.data))
        .catch((err) => {
          console.error(err)
          alert('Erro ao carregar treinos')
        })
    }
  }, [authorized])

  const handleDelete = async (id) => {
    const confirm = window.confirm('Tem certeza que deseja deletar este treino?')
    if (!confirm) return

    try {
      await api.delete(`/workouts/${id}`)
      setWorkouts((prev) => prev.filter((w) => w.id !== id))
      alert('Treino deletado com sucesso!')
    } catch (err) {
      console.error(err)
      alert('Erro ao deletar treino')
    }
  }

  if (authorized === null) return <p className="text-center mt-10">Carregando...</p>

  if (!authorized) {
    return (
      <div className="text-center mt-10 text-red-600">
        <h2 className="text-xl font-bold">Acesso negado</h2>
        <p>Você não tem permissão para acessar esta página.</p>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto mt-10 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-blue-700">Dashboard do Treinador</h1>
        <Link
          to="/CreateWorkout"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          + Novo Treino
        </Link>
      </div>

      {workouts.length === 0 ? (
        <p className="text-center text-gray-500">Nenhum treino criado.</p>
      ) : (
        workouts.map((workout) => (
          <div
            key={workout.id}
            className="border rounded p-4 shadow space-y-2"
          >
            <h2 className="text-xl font-bold">{workout.name}</h2>
            <p>{workout.description}</p>
            <p className="text-sm text-gray-500">
              {workout.start_date} até {workout.end_date}
            </p>

            <div className="flex flex-wrap gap-2 mt-2">
              <Link
                to={`/AssignStudents`}
                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
              >
                Atribuir treino à aluno
              </Link>
              <Link
                to={`/EditWorkout`}
                className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
              >
                Editar
              </Link>
              <button
                onClick={() => handleDelete(workout.id)}
                className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
              >
                Apagar
              </button>
            </div>
          </div>
        ))
      )}

      <div className="mt-10">
        <h2 className="text-xl font-bold">Progresso dos Estudantes</h2>
        <Link
          to="/progress/student/1"
          className="text-blue-600 underline"
        >
          Ver progresso de um aluno
        </Link>
      </div>
    </div>
  )
}
