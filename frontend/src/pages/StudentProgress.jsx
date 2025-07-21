// src/pages/StudentProgress.jsx
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

export default function StudentProgress() {
  const { student_id } = useParams()
  const [progress, setProgress] = useState([])

  useEffect(() => {
    api.get(`/progress/student/${student_id}`)
      .then((res) => setProgress(res.data))
      .catch(() => alert('Erro ao carregar progresso'))
  }, [student_id])

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Progresso do Estudante #{student_id}</h1>
      {progress.length === 0 ? (
        <p className="text-gray-500">Nenhum progresso registrado.</p>
      ) : (
        <ul className="space-y-2">
          {progress.map((p) => (
            <li
              key={p.id}
              className="border p-3 rounded shadow"
            >
              <p>
                Treino ID: <strong>{p.workout_id}</strong>
              </p>
              <p>Data: {p.date}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
