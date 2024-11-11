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
    idade INT,
    apelido_colegio VARCHAR(100),
    animal_representa TEXT,
    habilidade VARCHAR(255),
    estacao_ano TEXT,
    musica_preferida TEXT,
    status ENUM('Pendente', 'Aprovado', 'Rejeitado') DEFAULT 'Pendente',
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
);


INSERT INTO participantes (nome, email, grupo, instagram, seguidores) VALUES
('João Silva', 'joao.silva@email.com', 'Pipoca', '@joao_silva', 1200),
('Maria Oliveira', 'maria.oliveira@email.com', 'Camarote', '@maria_oliveira', 4500),
('Carlos Souza', 'carlos.souza@email.com', 'Não Selecionado',  '@carlos_souza', 800),
('Ana Santos', 'ana.santos@email.com', 'Pipoca', '@ana_santos', 1500),
('Pedro Lima', 'pedro.lima@email.com', 'Camarote', '@pedro_lima', 3000),
('Julia Pereira', 'julia.pereira@email.com', 'Não Selecionado', '@julia_pereira', 700);


INSERT INTO inscricoes (participante_id, idade, apelido_colegio, animal_representa, habilidade, estacao_ano, musica_preferida, status) VALUES
(1, 22, 'Jojo', 'Leão', 'Cantar', 'Verão', 'We Will Rock You', 'Aprovado'),
(2, 18, 'Mari', 'Gato', 'Dançar', 'Outono', 'Bad Romance', 'Pendente'),
(3, 19, 'Carlinhos', 'Cachorro', 'Cozinhar', 'Inverno', 'Stayin’ Alive', 'Rejeitado'),
(4, 20, 'Aninha', 'Girafa', 'Pintar', 'Primavera', 'Thriller', 'Pendente'),
(5, 21, 'Pedrinho', 'Tigre', 'Jogar futebol', 'Inverno', 'We Are The Champions', 'Aprovado'),
(6, 23, 'Julinha', 'Elefante', 'Nadar', 'Verão', 'I Want To Break Free', 'Rejeitado');


INSERT INTO logins (participante_id, username, senha) VALUES
(1, 'joao.silva', 'senhaJoao123'), 
(2, 'maria.oliveira', 'senhaMaria123'),  
(3, 'carlos.souza', 'senhaCarlos123'),
(4, 'ana.santos', 'senhaAna123'),
(5, 'pedro.lima', 'senhaPedro123'),
(6, 'julia.pereira', 'senhaJulia123');