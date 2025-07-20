import { useState } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const [form, setForm] = useState({ username: '', password: '', role: 'student' })
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/auth/register', form)
      alert('Registro realizado com sucesso! Faça login para continuar.')
      navigate('/login')
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao registrar')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-4 space-y-4">
      <h2 className="text-2xl font-bold">Registrar</h2>

      <input
        name="username"
        placeholder="Usuário"
        onChange={handleChange}
        required
        className="w-full border p-2 rounded"
      />
      <input
        name="password"
        type="password"
        placeholder="Senha"
        onChange={handleChange}
        required
        className="w-full border p-2 rounded"
      />

      <select
        name="role"
        onChange={handleChange}
        className="w-full border p-2 rounded"
        required
      >
        <option value="student">Aluno</option>
        <option value="trainer">Treinador</option>
      </select>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white p-2 rounded"
      >
        Registrar
      </button>
    </form>
  )
}
