-- SE QUISER RECRIAR O BANCO DO ZERO, DESCOMENTE ESTA LINHA:
-- DROP DATABASE IF EXISTS myteste;

CREATE DATABASE IF NOT EXISTS myteste;
USE myteste;

-- Tabela de salas
CREATE TABLE IF NOT EXISTS sala (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    status ENUM('disponivel', 'ocupada', 'manutencao') DEFAULT 'disponivel',
    imagem VARCHAR(255) NOT NULL
);

-- Dados iniciais de salas
INSERT INTO sala (nome, status, imagem) VALUES
('Laboratório 1', 'disponivel', 'laboratorio.png'),
('Sala 204', 'manutencao', 'sala_comum.png'),
('Sala 02', 'disponivel', 'sala.png'),
('Sala de Medicina', 'disponivel', 'medicina.png'),
('Inovadora', 'disponivel', 'inovadora.png'),
('Inovadora 1', 'disponivel', 'salainovadora.png'),
('Laboratório', 'disponivel', 'laboratorio.png');

-- Tabela de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT NOT NULL,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    responsavel VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sala_id) REFERENCES sala(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_data_hora (data_reserva, hora_inicio, hora_fim)
);
