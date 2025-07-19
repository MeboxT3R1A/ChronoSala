create database chronosala;
use chronosala;

CREATE TABLE funcionario ( 
	email VARCHAR(60) PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    matricula CHAR(5) UNIQUE,
    senha VARCHAR(11) NOT NULL,
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

-- 1. Inserindo apenas coordenador, professor e administrador
INSERT INTO funcionario (email, nome, matricula, senha, funcao) VALUES
('admin@gmail.com', 'Administrador Geral', '00001', 'admin123', 'Administrador'),
('coord@gmail.com', 'Coordenador TI', '10001', 'coord123', 'Coordenador'),
('prof@gmail.com', 'Professor Matemática', '20001', 'prof123', 'Instrutor');

-- 4. Mantendo as salas (sem alterações)
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