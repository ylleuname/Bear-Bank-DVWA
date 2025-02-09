import mysql.connector
from config import DB_CONFIG_VULNERABLE

def init_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG_VULNERABLE['host'],
        user=DB_CONFIG_VULNERABLE['user'],
        password=DB_CONFIG_VULNERABLE['password'],
    )
    cursor = conn.cursor()

    # Criar o banco de dados se não existir
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG_VULNERABLE['database']}")
    cursor.execute(f"USE {DB_CONFIG_VULNERABLE['database']}")

    # Criar tabelas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        agencia VARCHAR(10) NOT NULL,
        conta VARCHAR(10) NOT NULL,
        digito CHAR(1) NOT NULL,
        senha VARCHAR(255) NOT NULL, -- Armazenar hash da senha
        nome_completo VARCHAR(50) NOT NULL,
        cpf VARCHAR(11) UNIQUE NOT NULL,
        telefone VARCHAR(15),
        email VARCHAR(50) UNIQUE,
        endereco_rua VARCHAR(100),
        endereco_numero VARCHAR(10),
        endereco_cidade VARCHAR(50),
        endereco_estado CHAR(2),
        saldo DECIMAL(10, 2) DEFAULT 0.00, -- Novo campo: saldo
        investimento DECIMAL(10, 2) DEFAULT 0.00 -- Novo campo: investimento
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_transacoes (
        id_tipo INT AUTO_INCREMENT PRIMARY KEY,
        tipo VARCHAR(1) NOT NULL, -- 'R' ou 'E'
        descricao VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id_transacao INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        data_transacao DATETIME NOT NULL,
        tipo_transacao_id INT NOT NULL,
        valor DECIMAL(10, 2) NOT NULL,
        origem VARCHAR(255),
        destino VARCHAR(255),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY (tipo_transacao_id) REFERENCES tipos_transacoes(id_tipo)
    )
    """)

    # Inserir tipos de transações
    cursor.execute("""
    INSERT IGNORE INTO tipos_transacoes (id_tipo, tipo, descricao)
    VALUES 
    (1, 'R', 'Recebida'),
    (2, 'E', 'Enviada')
    """)

    # Inserir dados fictícios de usuários (com saldo e investimento)
    cursor.execute("""
    INSERT IGNORE INTO usuarios 
    (agencia, conta, digito, senha, nome_completo, cpf, telefone, email, endereco_rua, endereco_numero, endereco_cidade, endereco_estado, saldo, investimento) 
    VALUES
    ('1234', '56789', '0', 'senha123', 'João Silva', '12345678901', '61999999999', 'joao@exemplo.com', 'Rua das Flores', '123', 'Brasília', 'DF', 1000.00, 500.00),
    ('1234', '54123', '1', 'senha456', 'Maria Santos', '98765432100', '61888888888', 'maria@exemplo.com', 'Av. Paulista', '456', 'São Paulo', 'SP', 2000.00, 1000.00)
    """)

    # Inserir dados fictícios de transações
    cursor.execute("""
    INSERT IGNORE INTO transacoes 
    (id_usuario, data_transacao, tipo_transacao_id, valor, origem, destino) 
    VALUES
    (1, '2024-11-25 10:00:00', 1, 1000.00, 'José', 'João Silva'),
    (2, '2024-11-25 11:30:00', 1, 250.00, 'Supermercado', 'Maria Santos'),
    (1, '2024-10-15 09:45:00', 1, 500.00, 'Caixa Eletrônico', 'João Silva'),
    (1, '2024-11-15 08:50:00', 1, 200.00, 'Beatriz Lima', 'João Silva'),    
    (1, '2024-10-20 11:00:00', 2, 120.00, 'João Silva', 'Companhia Elétrica'),
    (1, '2024-11-05 13:30:00', 2, 300.00, 'João Silva', 'Restaurante'),
    (1, '2024-11-10 14:15:00', 2, 50.00, 'João Silva', 'Ana Costa'),
    (2, '2024-11-18 10:10:00', 2, 75.00, 'Maria Santos', 'Posto de Gasolina'),
    (2, '2024-11-20 12:40:00', 2, 90.00, 'Maria Santos', 'Provedor de Internet'),
    (2, '2024-11-22 16:05:00', 2, 400.00, 'Maria Santos', 'Aluguel'),
    (2, '2024-11-23 19:30:00', 2, 100.00, 'Maria Santos', 'Fernanda Ribeiro'),
    (2, '2024-11-24 21:15:00', 2, 220.00, 'Maria Santos', 'Loja de Presentes')          
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
