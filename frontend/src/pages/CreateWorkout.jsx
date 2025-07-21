// src/pages/CreateWorkout.jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function CreateWorkout() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', description: '', start_date: '', end_date: '' })

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/workouts/', form)
      alert('Treino criado com sucesso!')
      navigate('/dashboard/trainer')
    } catch (err) {
      alert('Erro ao criar treino')
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10">
      <h1 className="text-2xl font-bold">Criar Novo Treino</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mt-4">
        <input
          type="text"
          className="w-full border p-2 rounded"
          placeholder="Nome"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <textarea
          className="w-full border p-2 rounded"
          placeholder="Descrição"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          required
        />
        <input
          type="date"
          className="w-full border p-2 rounded"
          value={form.start_date}
          onChange={(e) => setForm({ ...form, start_date: e.target.value })}
          required
        />
        <input
          type="date"
          className="w-full border p-2 rounded"
          value={form.end_date}
          onChange={(e) => setForm({ ...form, end_date: e.target.value })}
          required
        />
        <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Criar
        </button>
      </form>
    </div>
  )
}
