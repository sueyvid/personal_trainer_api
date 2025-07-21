// src/pages/WorkoutDetails.jsx
import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../services/api'

export default function WorkoutDetails() {
  const { id } = useParams()
  const [exercises, setExercises] = useState([])
  const [form, setForm] = useState({ name: '', description: '', reps: '' })

  useEffect(() => {
    api.get(`/exercises/workout/${id}`).then((res) => setExercises(res.data))
  }, [id])

  const handleCreateExercise = async (e) => {
    e.preventDefault()
    try {
      await api.post('/exercises/', { ...form, workout_id: Number(id) })
      const res = await api.get(`/exercises/workout/${id}`)
      setExercises(res.data)
      setForm({ name: '', description: '', reps: '' })
    } catch (err) {
      alert('Erro ao criar exercício')
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Detalhes do Treino #{id}</h1>

      <Link
        to={`/workouts/${id}/assign`}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
      >
        Vincular Alunos
      </Link>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Exercícios</h2>
        {exercises.length === 0 ? (
          <p className="text-gray-500">Nenhum exercício encontrado.</p>
        ) : (
          <ul className="space-y-2">
            {exercises.map((ex) => (
              <li key={ex.id} className="border p-2 rounded shadow">
                <strong>{ex.name}</strong> - {ex.description} ({ex.reps} reps)
              </li>
            ))}
          </ul>
        )}
      </div>

      <form onSubmit={handleCreateExercise} className="space-y-2">
        <h3 className="text-lg font-bold">Adicionar Exercício</h3>
        <input
          type="text"
          placeholder="Nome"
          className="w-full border p-2 rounded"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <textarea
          placeholder="Descrição"
          className="w-full border p-2 rounded"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Repetições"
          className="w-full border p-2 rounded"
          value={form.reps}
          onChange={(e) => setForm({ ...form, reps: e.target.value })}
          required
        />
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Criar Exercício
        </button>
      </form>
    </div>
  )
}