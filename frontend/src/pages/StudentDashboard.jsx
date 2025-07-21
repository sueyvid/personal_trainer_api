// src/pages/StudentDashboard.jsx
import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import { format } from 'date-fns'

export default function StudentDashboard() {
  const [authorized, setAuthorized] = useState(null)
  const [workouts, setWorkouts] = useState([])
  const [progress, setProgress] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const today = format(new Date(), 'yyyy-MM-dd')

  useEffect(() => {
    const role = localStorage.getItem('role')
    if (role === 'student') {
      setAuthorized(true)
    } else {
      setAuthorized(false)
    }
  }, [])

  useEffect(() => {
    if (authorized === true) {
      const fetchData = async () => {
        try {
          const [workoutRes, progressRes] = await Promise.all([
            api.get('/workouts/me'),
            api.get('/progress/me'),
          ])
          setWorkouts(workoutRes.data)
          setProgress(progressRes.data)
        } catch (err) {
          console.error(err)
          alert('Erro ao carregar dados do aluno')
        } finally {
          setLoading(false)
        }
      }

      fetchData()
    }
  }, [authorized])

  const hasDoneWorkoutToday = (workoutId) =>
    progress.some(
      (entry) => entry.workout_id === workoutId && entry.date === today
    )

  const handleMarkProgress = async (workoutId) => {
    try {
      const res = await api.post('/progress', {
        workout_id: workoutId,
        date: today,
      })
      setProgress((prev) => [...prev, res.data])
      alert('Progresso registrado com sucesso!')
    } catch (err) {
      console.error(err)
      alert('Erro ao registrar progresso')
    }
  }

  if (authorized === null || loading) return <p className="text-center mt-10">Carregando...</p>

  if (!authorized) {
    return (
      <div className="text-center mt-10 text-red-600">
        <h2 className="text-xl font-bold">Acesso negado</h2>
        <p>Você não tem permissão para acessar esta página.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-3xl font-bold text-blue-700 text-center">
        Meus Treinos
      </h1>

      <div className="text-right">
        <Link
          to="/user/manage"
          className="inline-block bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition"
        >
          Gerenciar Conta
        </Link>
      </div>

      {workouts.length === 0 ? (
        <p className="text-center text-gray-500">Nenhum treino atribuído.</p>
      ) : (
        workouts.map((workout) => (
          <div
            key={workout.id}
            className="border rounded-lg p-4 shadow space-y-2"
          >
            <h2 className="text-xl font-bold">{workout.name}</h2>
            <p className="text-gray-700">{workout.description}</p>
            <p className="text-sm text-gray-500">
              De {workout.start_date} até {workout.end_date}
            </p>

            {hasDoneWorkoutToday(workout.id) ? (
              <span className="inline-block text-green-600 font-semibold">
                ✅ Treino realizado hoje
              </span>
            ) : (
              <button
                onClick={() => handleMarkProgress(workout.id)}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
              >
                Marcar como feito hoje
              </button>
            )}
          </div>
        ))
      )}

      <div className="mt-10">
        <h2 className="text-2xl font-bold text-blue-600 mb-4">Meu Progresso</h2>
        {progress.length === 0 ? (
          <p className="text-gray-500">Nenhum progresso registrado ainda.</p>
        ) : (
          <ul className="space-y-2">
            {progress.map((entry) => (
              <li key={entry.id} className="text-sm text-gray-700">
                🏋️‍♂️ Treino #{entry.workout_id} feito em {entry.date}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
