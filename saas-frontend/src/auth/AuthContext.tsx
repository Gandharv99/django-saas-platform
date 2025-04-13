import { createContext, useContext, useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"

interface AuthContextType {
    token: string | null
    login: (email: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [token, setToken] = useState<string | null>(localStorage.getItem("token"))
    const navigate = useNavigate()

    const login = async (email: string, password: string) => {
        const res = await axios.post("http://localhost:8000/api/login/", {
            email,
            password,
        })
        localStorage.setItem("token", res.data.access)
        setToken(res.data.access)
        navigate("/dashboard")
    }

    const logout = () => {
        localStorage.removeItem("token")
        setToken(null)
        navigate("/login")
    }

    useEffect(() => {
        if (token) {
            axios.defaults.headers.common["Authorization"] = `Bearer ${token}`
        }
    }, [token])

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
    const ctx = useContext(AuthContext)
    if (!ctx) throw new Error("useAuth must be used within an AuthProvider")
    return ctx
}