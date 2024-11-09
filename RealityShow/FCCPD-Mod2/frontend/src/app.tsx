// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/register';
import UserData from './components/userData';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<h1>Página Inicial</h1>} /> {/* Hi Lorena */}
        <Route path="/register" element={<RegistrationForm />} /> {/* Página de Registro */}
        <Route path="/user-data" element={<UserData />} /> {/* Página para exibir os DADOS do usuário */}
      </Routes>
    </Router>
  );
};

export default App;
