// UserData.tsx
import React, { useEffect, useState } from 'react';

const UserData: React.FC = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://api:8000/")
      .then(response => {
        if (!response.ok) {
          throw new Error("Erro ao buscar dados da API");
        }
        return response.json();
      })
      .then(data => setData(data))
      .catch(error => console.error("Erro:", error));
  }, []);

  return (
    <div>
      <h1>Dados do Usuário</h1>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Carregando...</p>
      )}
    </div>
  );
};

export default UserData;
