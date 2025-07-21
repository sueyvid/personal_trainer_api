// src/pages/ManageUser.jsx
import { useEffect, useState } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function ManageUser() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [confirmPassword, setConfirmPassword] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    const payload = JSON.parse(atob(token.split('.')[1]))
    setForm((prev) => ({ ...prev, username: payload.sub }))
  }, [])

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleUpdate = async (e) => {
    e.preventDefault()
    try {
      await api.put('/users/me', form) // ✅ Corrigido
      alert('Usuário atualizado com sucesso!')
    } catch (err) {
      console.error(err)
      alert('Erro ao atualizar usuário')
    }
  }

  const handleDelete = async () => {
    const confirm = window.confirm('Tem certeza que deseja deletar sua conta?')
    if (!confirm) return

    try {
      await api.delete('/users/me', {
        data: { password: confirmPassword }, // ✅ Senha é obrigatória no corpo
      })
      alert('Conta deletada com sucesso!')
      localStorage.clear()
      navigate('/login')
    } catch (err) {
      console.error(err)
      alert(
        err.response?.data?.detail ||
          'Erro ao deletar conta (verifique a senha)'
      )
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-4 space-y-4 border rounded shadow">
      <h2 className="text-2xl font-bold text-center">Gerenciar Usuário</h2>

      <form onSubmit={handleUpdate} className="space-y-4">
        <input
          name="username"
          value={form.username}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          placeholder="Nome de usuário"
        />

        <input
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          className="w-full border p-2 rounded"
          placeholder="Nova senha"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded"
        >
          Atualizar
        </button>
      </form>

      <hr />

      <input
        type="password"
        placeholder="Confirmar senha para deletar"
        className="w-full border p-2 rounded"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />

      <button
        onClick={handleDelete}
        className="w-full bg-red-600 text-white p-2 rounded"
      >
        Deletar Conta
      </button>
    </div>
  )
}
