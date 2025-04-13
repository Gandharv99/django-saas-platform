import { useAuth } from "../auth/AuthContext"

export default function Dashboard(){
    const { logout } = useAuth()

    return(
    <div className="p-10 text-center">
        <h1 className="text-3xl font-bold text-green-700 mb-6">Welcome to Dashboard 🎉</h1>
        <button
            onClick={logout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
            Logout
        </button>
    </div>
    )
}