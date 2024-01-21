import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000";

async function createTodo() {
    const title = 'Sample Title';
    const description = 'Sample Description';
    try {
        const response = await axios.post(`${BASE_URL}/todos/`, { title, description });
        console.log("Todo added successfully");
    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function deleteTodo() {
    const todoId = 1; // Replace with the desired Todo ID
    try {
        const response = await axios.delete(`${BASE_URL}/todos/${todoId}`);
        console.log("Todo deleted successfully");
    } catch (error) {
        console.error("Error:", error.message);
    }
}