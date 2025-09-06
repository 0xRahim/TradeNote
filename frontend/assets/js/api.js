// This file will contain all the API integration logic.

const API_BASE_URL = 'http://127.0.0.1:5000';

// Function to get the JWT token from localStorage
const getToken = () => {
    return localStorage.getItem('token');
};

// Function to set the JWT token in localStorage
const setToken = (token) => {
    localStorage.setItem('token', token);
};

// Function to handle user login
const login = async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${btoa(`${username}:${password}`)}`
        }
    });
    if (response.ok) {
        const data = await response.json();
        setToken(data.token);
        window.location.href = 'dashboard.html';
    } else {
        alert('Login failed');
    }
};

// Function to handle user registration
const register = async (username, password, avatar) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, avatar })
    });
    if (response.ok) {
        alert('Registration successful! Please log in.');
        window.location.reload();
    } else {
        const data = await response.json();
        alert(`Registration failed: ${data.message}`);
    }
};

const request = async (endpoint, method = 'GET', body = null) => {
    const headers = {
        'Authorization': `Bearer ${getToken()}`
    };
    if (body && !(body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const config = {
        method,
        headers
    };

    if (body) {
        config.body = (body instanceof FormData) ? body : JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
        window.location.href = 'index.html';
    }

    return response;
};

const getTrades = (params) => {
    let endpoint = '/trades/';
    if (params) {
        const query = new URLSearchParams(params).toString();
        endpoint += `?${query}`;
    }
    return request(endpoint);
};
const getTrade = (id) => request(`/trades/${id}`);
const createTrade = (tradeData) => request('/trades/', 'POST', tradeData);
const updateTrade = (id, tradeData) => request(`/trades/${id}`, 'PUT', tradeData);
const deleteTrade = (id) => request(`/trades/${id}`, 'DELETE');

const getNotes = (params) => {
    let endpoint = '/notes/';
    if (params) {
        const query = new URLSearchParams(params).toString();
        endpoint += `?${query}`;
    }
    return request(endpoint);
};
const getNote = (id) => request(`/notes/${id}`);
const createNote = (noteData) => request('/notes/', 'POST', noteData);
const updateNote = (id, noteData) => request(`/notes/${id}`, 'PUT', noteData);
const deleteNote = (id) => request(`/notes/${id}`, 'DELETE');

const getPlaybooks = () => request('/playbooks/');
const getPlaybook = (id) => request(`/playbooks/${id}`);
const createPlaybook = (playbookData) => request('/playbooks/', 'POST', playbookData);
const updatePlaybook = (id, playbookData) => request(`/playbooks/${id}`, 'PUT', playbookData);
const deletePlaybook = (id) => request(`/playbooks/${id}`, 'DELETE');

const getUser = () => request('/auth/user');
const uploadAvatar = (avatarData) => request('/auth/avatar', 'POST', avatarData);

const getEvents = () => request('/events');
