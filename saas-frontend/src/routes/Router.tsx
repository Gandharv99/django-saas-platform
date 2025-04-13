import { Routes, Route } from 'react-router-dom'
import Login from '../pages/Login'
import Dashboard from "../pages/Dashboard"

export default function AppRoutes() {
    return (
        <Routes>
            <Route path='/login' element={<Login />} />
            <Route path='/dashboard' element={<Dashboard />} />
        </Routes>
    )
}