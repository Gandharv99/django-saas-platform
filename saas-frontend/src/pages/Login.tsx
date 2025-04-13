import { useState } from "react"
import {useAuth } from "../auth/AuthContext"

export default function Login() {
    const {login} = useAuth()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try{
            await login(email, password)
        } catch (err) {
            setError("Invalid credentials")
        }
    }

    return (
        <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Login</h2>
            {error && <p className="text-red-600">{error}</p>}
            <form onSubmit={handleSubmit} className="space-y-4">
                <input className="w-full border p-2"
                    placeholder="Email"
                    type="email" 
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                />
                <input className="w-full border p-2"
                    placeholder="Password"
                    type="password" 
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded">
                    Login
                </button>
            </form>
        </div>
    )
}