USE fccpd;

CREATE TABLE IF NOT EXISTS participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    grupo ENUM('Pipoca', 'Camarote', 'Não Selecionado') DEFAULT 'Não Selecionado',
    instagram VARCHAR(100),
    seguidores INT DEFAULT 0, 
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inscricoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    data_inscricao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    formulario JSON NOT NULL,
    status ENUM('Pendente', 'Aprovado', 'Rejeitado') DEFAULT 'Pendente',
    idade_coluna INT,
    apelido_colegio VARCHAR(100),
    animal_rep TEXT,
    habilidade VARCHAR(255),
    estacao_ano TEXT,
    superpoder VARCHAR(100),
    talento_danca VARCHAR(100),
    musica_entrada VARCHAR(255),
    travessura TEXT,
    bordao VARCHAR(255),
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);


INSERT INTO participantes (nome, email, grupo) VALUES
('João Silva', 'joao.silva@email.com', 'Pipoca', '@joao_silva', 1200),
('Maria Oliveira', 'maria.oliveira@email.com', 'Camarote', '@maria_oliveira', 4500),
('Carlos Souza', 'carlos.souza@email.com', 'Não Selecionado',  '@carlos_souza', 800);

INSERT INTO inscricoes (participante_id, formulario, status) VALUES
(1, '{"idade": 25, "cidade": "São Paulo", "profissao": "Engenheiro", "animal_rep": "Leão", "habilidade": "Cantar", "superpoder": "Voar", "bordao": "Eu sou o rei!"}', 'Aprovado'),
(2, '{"idade": 30, "cidade": "Rio de Janeiro", "profissao": "Atriz", "animal_rep": "Gato", "habilidade": "Dançar", "superpoder": "Teleportar", "bordao": "Cá estou!"}', 'Pendente'),
(3, '{"idade": 22, "cidade": "Belo Horizonte", "profissao": "Estudante", "animal_rep": "Cachorro", "habilidade": "Cozinhar", "superpoder": "Invisibilidade", "bordao": "Vou dominar o mundo!"}', 'Rejeitado');

INSERT INTO logins (participante_id, username, senha) VALUES
(1, 'joao.silva', 'senhaJoao123'), 
(2, 'maria.oliveira', 'senhaMaria123'),  
(3, 'carlos.souza', 'senhaCarlos123');