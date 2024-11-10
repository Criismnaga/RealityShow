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
    -- formulario JSON NOT NULL,
    idade INT,
    apelido_colegio VARCHAR(100),
    animal_representa TEXT,
    habilidade VARCHAR(255),
    estacao_ano TEXT,
    musica_preferida TEXT,
    status ENUM('Pendente', 'Aprovado', 'Rejeitado') DEFAULT 'Pendente'
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);


INSERT INTO participantes (nome, email, grupo, instagram, seguidores) VALUES
('João Silva', 'joao.silva@email.com', 'Pipoca', '@joao_silva', 1200),
('Maria Oliveira', 'maria.oliveira@email.com', 'Camarote', '@maria_oliveira', 4500),
('Carlos Souza', 'carlos.souza@email.com', 'Não Selecionado',  '@carlos_souza', 800);

-- segunda tabela: INSERT INTO inscricoes (participante_id, formulario, status, idade_coluna, apelido_colegio, animal_rep, habilidade, estacao_ano, superpoder, talento_danca, musica_entrada, travessura, bordao) VALUES
-- (1, '{"idade": 25, "cidade": "São Paulo", "profissao": "Engenheiro"}', 'Aprovado', 22, 'Jojo', 'Leão', 'Cantar', 'Verão', 'Voar', 'Excelente', 'We Will Rock You', 'Fazer um show no palco', 'Eu sou o rei!'),
-- (2, '{"idade": 30, "cidade": "Rio de Janeiro", "profissao": "Atriz"}', 'Pendente', 18, 'Mari', 'Gato', 'Dançar', 'Outono', 'Teleportar', 'Boa', 'Bad Romance', 'Ficar invisível para os professores', 'Cá estou!'),
-- (3, '{"idade": 22, "cidade": "Belo Horizonte", "profissao": "Estudante"}', 'Rejeitado', 19, 'Carlinhos', 'Cachorro', 'Cozinhar', 'Inverno', 'Invisibilidade', 'Regular', 'Stayin’ Alive', 'Trocar o quadro do professor', 'Vou dominar o mundo!');

INSERT INTO inscricoes (participante_id, idade, apelido_colegio, animal_representa, habilidade, estacao_ano, musica_preferida, status) VALUES
(1, 22, 'Jojo', 'Leão', 'Cantar', 'Verão', 'We Will Rock You', 'Aprovado'),
(2, 18, 'Mari', 'Gato', 'Dançar', 'Outono', 'Bad Romance', 'Pendente'),
(3, 19, 'Carlinhos', 'Cachorro', 'Cozinhar', 'Inverno', 'Stayin’ Alive', 'Rejeitado');


INSERT INTO logins (participante_id, username, senha) VALUES
(1, 'joao.silva', 'senhaJoao123'), 
(2, 'maria.oliveira', 'senhaMaria123'),  
(3, 'carlos.souza', 'senhaCarlos123');