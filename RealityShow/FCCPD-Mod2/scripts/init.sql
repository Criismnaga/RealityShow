USE fccpd;

CREATE TABLE IF NOT EXISTS participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    grupo ENUM('Pipoca', 'Camarote', 'Não Selecionado') DEFAULT 'Não Selecionado',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inscricoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    data_inscricao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Alterado para TIMESTAMP
    formulario JSON NOT NULL,  -- Confirme que o MySQL 8.0 está em uso
    status ENUM('Pendente', 'Aprovado', 'Rejeitado') DEFAULT 'Pendente',
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);

INSERT INTO participantes (nome, email, grupo) VALUES
('João Silva', 'joao.silva@email.com', 'Pipoca'),
('Maria Oliveira', 'maria.oliveira@email.com', 'Camarote'),
('Carlos Souza', 'carlos.souza@email.com', 'Não Selecionado');

INSERT INTO inscricoes (participante_id, formulario, status) VALUES
(1, '{"idade": 25, "cidade": "São Paulo", "profissao": "Engenheiro"}', 'Aprovado'),
(2, '{"idade": 30, "cidade": "Rio de Janeiro", "profissao": "Atriz"}', 'Pendente'),
(3, '{"idade": 22, "cidade": "Belo Horizonte", "profissao": "Estudante"}', 'Rejeitado');
