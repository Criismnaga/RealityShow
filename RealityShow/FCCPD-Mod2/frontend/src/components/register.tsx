// Register.tsx
import React, { useState } from 'react';
import axios from 'axios';

const API_URL = "http://api:8000";

// Função para enviar dados de cadastro para a API:
const registerUser = async (username: string, password: string, nome: string, email: string) => {
    try {
        const response = await axios.post(`${API_URL}/register`, {
            username,
            password,
            nome,
            email,
        });
        if (response.status === 200) {
            alert("Usuário cadastrado com sucesso!");
        }
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            if (error.response.status === 400) {
                alert("Username ou email já cadastrado.");
            } else {
                alert("Erro ao registrar o usuário.");
            }
        } else {
            alert("Erro desconhecido.");
        }
    }
};

const RegistrationForm: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");

    const handleSubmit = () => {
        if (username && password && nome && email) {
            registerUser(username, password, nome, email);
        } else {
            alert("Por favor, preencha todos os campos.");
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
            <h1>Cadastre-se no spin-off do BBB</h1>
            <div>
                <label>Username</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>
            <div>
                <label>Password</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <div>
                <label>Nome</label>
                <input
                    type="text"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                />
            </div>
            <div>
                <label>Email</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <button onClick={handleSubmit}>Registrar</button>
        </div>
    );
};

export default RegistrationForm;
