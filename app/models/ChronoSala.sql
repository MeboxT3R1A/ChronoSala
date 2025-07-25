-- app/models/ChronoSala.sql

-- Drop existing database and create a new one for a clean start (only for development!)
DROP DATABASE IF EXISTS chronosala;
CREATE DATABASE chronosala;
USE chronosala;

CREATE TABLE funcionario (
    email VARCHAR(60) PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    matricula CHAR(5) UNIQUE,
    -- ALTERADO: Aumenta o tamanho do campo senha para armazenar hashes de senha.
    -- Um hash bcrypt geralmente tem cerca de 60 caracteres. VARCHAR(255) é um bom tamanho seguro.
    senha VARCHAR(255) NOT NULL,
    funcao VARCHAR(25) NOT NULL
);

CREATE TABLE cep (
    nome VARCHAR(40) PRIMARY KEY,
    endereco VARCHAR(50) NOT NULL
);

CREATE TABLE cep_func (
    cep_func INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(60),
    nome VARCHAR(40),
    FOREIGN KEY (email)
        REFERENCES funcionario (email)
        ON DELETE CASCADE,
    FOREIGN KEY (nome)
        REFERENCES cep (nome)
);

CREATE TABLE sala (
    nome_sala VARCHAR(150) PRIMARY KEY NOT NULL,
    status_sala ENUM('reservado', 'disponivel','manutenção') DEFAULT 'disponivel'
);

CREATE TABLE cursos (
    id_cursos INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    segmento VARCHAR(150) NOT NULL
);

CREATE TABLE reserva (
    id_res INT PRIMARY KEY AUTO_INCREMENT,
    nome_sala VARCHAR(150),
    email VARCHAR(60),
    inicio TIME NOT NULL,
    termino TIME NOT NULL,
    data_res DATE NOT NULL,
    status_res ENUM('reservado', 'cancelado') DEFAULT 'reservado',
    status_chave ENUM('pendente', 'Chave retirada', 'Chave devolvida') DEFAULT 'pendente',
    CONSTRAINT chk_horario CHECK (inicio < termino),
    FOREIGN KEY (nome_sala)
        REFERENCES sala (nome_sala)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (email)
        REFERENCES funcionario (email)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE historico (
    id_historico INT PRIMARY KEY AUTO_INCREMENT,
    data_historico DATETIME NOT NULL,
    nome VARCHAR(40),
    email VARCHAR(60),
    id_res INT,
    nome_sala VARCHAR(150),
    id_cursos INT,
    FOREIGN KEY (id_cursos)
        REFERENCES cursos (id_cursos),
    CONSTRAINT fk_login FOREIGN KEY (email)
        REFERENCES funcionario (email)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (nome)
        REFERENCES cep (nome),
    FOREIGN KEY (id_res)
        REFERENCES reserva (id_res)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (nome_sala)
        REFERENCES sala (nome_sala)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE controle_chaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT,
    email_professor VARCHAR(60),
    data_entrega DATETIME,
    data_devolucao DATETIME,
    FOREIGN KEY (id_reserva)
        REFERENCES reserva (id_res)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (email_professor)
        REFERENCES funcionario (email)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Para inserir senhas, você DEVE HASHEAR.
-- Execute o Python para gerar os hashes:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))
-- print(generate_password_hash('coord123'))
-- print(generate_password_hash('prof123'))
-- Substitua os valores abaixo pelos hashes gerados.
-- Exemplo de hashes gerados (estes são apenas exemplos, GERE OS SEUS!):
-- admin123 -> pbkdf2:sha256:600000$hQ3Q0l2x$4b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c
-- coord132 -> pbkdf2:sha256:600000$yR4S1m3n$5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
-- prof123  -> pbkdf2:sha256:600000$zT5U2o4p$6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e

INSERT INTO funcionario (email, nome, matricula, senha, funcao) VALUES
('admin@gmail.com', 'Administrador Geral', '00001', 'scrypt:32768:8:1$E6ESwQWJH23UMolH$d3d25371f04af4dee3e743c62dc261864f462c7940591267b08b631c6ab156c6cd5f00ab7ea56591512ca8c132b007e77fa0672fad428fc7518219d60ea24176', 'Administrador'),
('coord@gmail.com', 'Coordenador TI', '10001', 'scrypt:32768:8:1$WXfS5bvu12Uk70Ge$d55b49d3ee638b3fa0933838b4c990e168eacf6017e0286cf93c2e49a97a7506d057a6944a00e509850a13757e56833432a3b500f8e41cee23dfd87660b97d68', 'Coordenador'),
('prof@gmail.com', 'Professor Matemática', '20001', 'scrypt:32768:8:1$ezZOEcidURQOFjhS$9dbca837c2ad7e98dd395ec0091017c1c038f7d125ca08c25d6f9fc18eb4d5f8363dd4fa6add783546143065e76cab415a18ef97fbc42801ecd8d29f5306892a', 'Instrutor');

-- 4. Mantendo as salas (com adição de capacidade)
INSERT INTO sala (nome_sala, status_sala) VALUES
('Lab Informática 1', 'disponivel'),
('Lab Informática 2', 'disponivel'),
('Sala Multiuso', 'disponivel'),
('Auditório Principal', 'disponivel'),
('Sala de Reuniões', 'disponivel'),
('Lab Robótica', 'manutenção');

-- 5. Mantendo os cursos (sem alterações)
INSERT INTO cursos (nome, segmento) VALUES
('Técnico em Informática', 'Técnico'),
('Técnico em Administração', 'Técnico'),
('Ensino Médio Regular', 'Básico'),
('Curso de Inglês', 'Idiomas'),
('Oficina de Teatro', 'Artes');

-- 6. Inserindo 3 reservas (sem estados)
INSERT INTO reserva (nome_sala, email, inicio, termino, data_res) VALUES
('Lab Informática 1', 'prof@gmail.com', '08:00:00', '10:00:00', '2023-11-15'),
('Auditório Principal', 'coord@gmail.com', '14:00:00', '16:00:00', '2023-11-16'),
('Sala Multiuso', 'prof@gmail.com', '10:00:00', '12:00:00', '2023-11-17');

-- 7. Inserindo histórico (mantido como "okk")
INSERT INTO historico (data_historico, email, id_res, nome_sala, id_cursos) VALUES
('2023-11-10 08:05:23', 'prof@gmail.com', 1, 'Lab Informática 1', 1),
('2023-11-11 14:30:10', 'coord@gmail.com', 2, 'Auditório Principal', 3),
('2023-11-12 10:15:45', 'prof@gmail.com', 3, 'Sala Multiuso', 5);

-- 8. Inserindo controle de chaves (mantido como "tudo bem")
INSERT INTO controle_chaves (id_reserva, email_professor, data_entrega, data_devolucao) VALUES
(1, 'prof@gmail.com', '2023-11-15 07:45:00', '2023-11-15 10:05:00'),
(2, 'coord@gmail.com', '2023-11-16 13:45:00', NULL),
(3, 'prof@gmail.com', '2023-11-17 09:50:00', '2023-11-17 12:10:00');