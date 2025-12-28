import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { FaPlus, FaTrash, FaCheck, FaUndo, FaSignOutAlt } from 'react-icons/fa';

const Dashboard = () => {
    const { user, logout, token } = useAuth();
    const [tasks, setTasks] = useState([]);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [loading, setLoading] = useState(true);

    const api = axios.create({
        baseURL: '/api',
        headers: { Authorization: `Bearer ${token}` }
    });

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const res = await api.get('/tasks');
            setTasks(res.data);
        } catch (error) {
            console.error("Error fetching tasks", error);
        } finally {
            setLoading(false);
        }
    };

    const addTask = async (e) => {
        e.preventDefault();
        if (!newTaskTitle.trim()) return;
        try {
            const res = await api.post('/tasks', { title: newTaskTitle });
            setTasks([res.data, ...tasks]);
            setNewTaskTitle('');
        } catch (error) {
            console.error("Error adding task", error);
        }
    };

    const updateStatus = async (task, newStatus) => {
        try {
            const res = await api.put(`/tasks/${task.id}`, { status: newStatus });
            setTasks(tasks.map(t => t.id === task.id ? res.data : t));
        } catch (error) {
            console.error("Error updating task", error);
        }
    };

    const deleteTask = async (taskId) => {
        if (!confirm('Are you sure?')) return;
        try {
            await api.delete(`/tasks/${taskId}`);
            setTasks(tasks.filter(t => t.id !== taskId));
        } catch (error) {
            console.error("Error deleting task", error);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'done': return 'bg-green-100 text-green-800 border-green-200';
            case 'in_progress': return 'bg-blue-100 text-blue-800 border-blue-200';
            default: return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <nav className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center">
                            <h1 className="text-xl font-bold text-gray-800">Task Manager</h1>
                        </div>
                        <div className="flex items-center space-x-4">
                            <span className="text-gray-600">Welcome, {user?.name}</span>
                            <button onClick={logout} className="text-gray-500 hover:text-red-600 flex items-center transition-colors">
                                <FaSignOutAlt className="mr-1" /> Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-4xl mx-auto py-10 px-4">

                {/* Add Task Form */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                    <h2 className="text-lg font-semibold mb-4 text-gray-700">Add New Task</h2>
                    <form onSubmit={addTask} className="flex gap-4">
                        <input
                            type="text"
                            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                            placeholder="What needs to be done?"
                            value={newTaskTitle}
                            onChange={(e) => setNewTaskTitle(e.target.value)}
                        />
                        <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center transition-colors shadow-sm font-medium">
                            <FaPlus className="mr-2" /> Add
                        </button>
                    </form>
                </div>

                {/* Task List */}
                <div className="space-y-4">
                    {tasks.map(task => (
                        <div key={task.id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between hover:shadow-md transition-shadow">
                            <div className="flex items-center gap-4 flex-1">
                                <div className="flex flex-col gap-2">
                                    <span className={`text-lg font-medium ${task.status === 'done' ? 'line-through text-gray-400' : 'text-gray-800'}`}>
                                        {task.title}
                                    </span>
                                    <span className="text-xs text-gray-400">
                                        Created: {new Date(task.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>

                            <div className="flex items-center gap-4">
                                <select
                                    value={task.status}
                                    onChange={(e) => updateStatus(task, e.target.value)}
                                    className={`text-sm font-medium px-3 py-1 rounded-full border border-opacity-50 focus:outline-none cursor-pointer ${getStatusColor(task.status)}`}
                                >
                                    <option value="pending">Pending</option>
                                    <option value="in_progress">In Progress</option>
                                    <option value="done">Done</option>
                                </select>

                                <button
                                    onClick={() => deleteTask(task.id)}
                                    className="text-gray-400 hover:text-red-500 p-2 rounded-full hover:bg-red-50 transition-colors"
                                    title="Delete Task"
                                >
                                    <FaTrash />
                                </button>
                            </div>
                        </div>
                    ))}
                    {tasks.length === 0 && (
                        <div className="text-center text-gray-500 py-16 bg-white rounded-xl border border-gray-100">
                            <p className="text-lg">No tasks yet.</p>
                            <p className="text-sm mt-2">Add one above to get started!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
