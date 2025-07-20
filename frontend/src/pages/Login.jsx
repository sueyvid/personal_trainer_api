// src/pages/Login.jsx
import { useState } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' })
  const navigate = useNavigate()

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await api.post('/auth/login', form)
      const { access_token } = response.data

      // Decodificar o JWT para extrair o papel (role)
      const payload = JSON.parse(atob(access_token.split('.')[1]))
      const role = payload.role

      // Salvar no localStorage
      localStorage.setItem('token', access_token)
      localStorage.setItem('role', role)

      // Redirecionar conforme o papel
      if (role === 'trainer') {
        navigate('/dashboard/trainer')
      } else {
        navigate('/dashboard/student')
      }
    } catch (err) {
      console.error(err)
      alert('Usuário ou senha inválidos')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-4 space-y-4">
      <h2 className="text-2xl font-bold">Login</h2>

      <input
        name="username"
        type="text"
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

      <button
        type="submit"
        className="w-full bg-blue-600 text-white p-2 rounded"
      >
        Entrar
      </button>
    </form>
  )
}
