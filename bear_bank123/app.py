from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from config import DB_CONFIG, DB_CONFIG_VULNERABLE
import re

app = Flask(__name__)
app.secret_key = 'bear_bank_secret_key'

# Função para conectar ao banco de dados
def get_db_connection(safe_mode=True):
    db_config = DB_CONFIG if safe_mode else DB_CONFIG_VULNERABLE
    conn = mysql.connector.connect(**db_config)
    return conn


@app.route('/')
def index():
    return render_template('index.html')


#import re

def filter_input(user_input: str) -> str:
    """
    Sanitiza a entrada do usuário para prevenir SQL Injection.
    
    -Remove caracteres especiais comuns em ataques SQL Injection.
    -Bloqueia palavras-chave suspeitas.
    -Remove comentários SQL e delimitadores de múltiplas consultas.
    """
    user_input = user_input.strip()

    forbidden_patterns = [
        r'(--|#)',  # Comentários SQL
        r'(/\*.*?\*/)',  # Comentários multi-linha
        r'(\bOR\b|\bAND\b)',  # Injeção booleana
        r'(\bUNION\b.*?\bSELECT\b)',  # UNION-based SQLi
        r'(\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bALTER\b)',  # Modificação de tabelas
        r'(\bEXEC\b|\bEXECUTE\b)',  # Execução remota de comandos
        r'(\bSLEEP\b|\bBENCHMARK\b)',  # Ataques baseados em tempo
        r'([\'\";])',  # Aspas e ponto-e-vírgula
    ]

    for pattern in forbidden_patterns:
        user_input = re.sub(pattern, '', user_input, flags=re.IGNORECASE)

    print(f"Input filtrado: {user_input}")
    return user_input

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        agencia = request.form.get('agency')
        conta = request.form.get('account')
        senha = request.form.get('password')

        # Configuração do safe_mode e armazenamento na sessão
        safe_mode = request.form.get('safe_mode', 'off') == 'on'
        session['safe_mode'] = safe_mode  # Armazena o estado do modo seguro na sessão

        use_prepared_statement = request.form.get('use_prepared_statement', 'off') == 'on'
        session['use_prepared_statement'] = use_prepared_statement  # Opcional: armazene também se quiser usar depois

        filter_input_enabled = request.form.get('filter_input', 'off') == 'on'
        
        if filter_input_enabled:
            agencia = filter_input(agencia)
            conta = filter_input(conta)
            senha = filter_input(senha)

        conn = get_db_connection(safe_mode)
        cursor = conn.cursor(dictionary=True)

        try:
            if not use_prepared_statement:
                query = f"""
                SELECT * FROM usuarios 
                WHERE agencia = '{agencia}' AND conta = '{conta}' AND senha = '{senha}'
                """
                cursor.execute(query)
                print(f"Query sem prepared statement - login {query}")
            else:
                query = """
                SELECT * FROM usuarios 
                WHERE agencia = %s AND conta = %s AND senha = %s
                """
                cursor.execute(query, (agencia, conta, senha))
                print(f"Query Prepared Statement - login {query}")

            user = cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

        if user:
            session['user_id'] = user['id_usuario']
            session['usuario'] = user['nome_completo']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('conta'))
        else:
            flash('Credenciais inválidas!', 'error')

    return render_template('login.html')


@app.route('/conta', methods=['GET', 'POST'])
def conta():
    if 'user_id' not in session:
        flash('Sessão expirada ou usuário não logado. Por favor, faça login novamente.', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    safe_mode = session.get('safe_mode', True)
    use_prepared_statement = session.get('use_prepared_statement', False)  # Obtém a opção de query parametrizada

    conn = get_db_connection(safe_mode)
    cursor = conn.cursor(dictionary=True)

    try:
        query_user = """
        SELECT nome_completo, agencia, conta, digito, saldo, investimento 
        FROM usuarios 
        WHERE id_usuario = %s
        """
        cursor.execute(query_user, (user_id,))
        user = cursor.fetchone()
        

        if not user:
            flash('Erro ao recuperar informações da conta.', 'error')
            return redirect(url_for('login'))

        date_filter = request.args.get('date')

        if date_filter:
            if safe_mode:
                cursor.callproc('sp_get_user_and_transactions', [user_id, date_filter or None])
                user_info = None
                transactions = []
                for result in cursor.stored_results():
                    if user_info is None:
                        user_info = result.fetchone()
                    else:
                        transactions.extend(result.fetchall())
                print(f"Query Stored Procedure - Transação {transactions}")
            else:
                if use_prepared_statement:
                    query_transactions = """
                    SELECT DISTINCT t.data_transacao AS date, 
                        titr.descricao AS transaction_type,
                        t.valor AS amount, 
                        t.origem AS origin,
                        t.destino AS destination
                    FROM transacoes t
                    JOIN tipos_transacoes titr ON t.tipo_transacao_id = titr.id_tipo
                    WHERE t.id_usuario = %s 
                    AND DATE(t.data_transacao) = %s
                    """
                    cursor.execute(query_transactions, (user_id, date_filter))
                    print(f"Query Prepared Statement - Transação {query_transactions}")
                else:
                    query_transactions = f"""
                    SELECT DISTINCT t.data_transacao AS date, 
                        titr.descricao AS transaction_type,
                        t.valor AS amount, 
                        t.origem AS origin,
                        t.destino AS destination
                    FROM transacoes t
                    JOIN tipos_transacoes titr ON t.tipo_transacao_id = titr.id_tipo
                    WHERE t.id_usuario = {user_id} 
                    AND DATE(t.data_transacao) = '{date_filter}'
                    """
                    cursor.execute(query_transactions)
                    print(f"Query vulnerável - Transação {query_transactions}")

                transactions = cursor.fetchall()
        else:
            query_transactions = """
            SELECT DISTINCT t.data_transacao AS date, 
                titr.descricao AS transaction_type,
                t.valor AS amount, 
                t.origem AS origin,
                t.destino AS destination
            FROM transacoes t
            JOIN tipos_transacoes titr ON t.tipo_transacao_id = titr.id_tipo
            WHERE t.id_usuario = %s 
            ORDER BY t.data_transacao DESC
            LIMIT 10
            """
            cursor.execute(query_transactions, (user_id,))
            transactions = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template('conta.html', user=user, transactions=transactions)


from decimal import Decimal # Importar a classe Decimal para lidar com valores monetários

@app.route('/investimento', methods=['GET', 'POST'])
def investimento():
    if 'user_id' not in session:
        flash('Sessão expirada ou usuário não logado. Por favor, faça login novamente.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    safe_mode = session.get('safe_mode', True)
    use_prepared = session.get('use_prepared_statement', False)  # Pegando o estado da sessão
    filter_input_enabled = session.get('filter_input_enabled', False)  # Recupera filtragem da sessão
    
    # Buscar informações do usuário
    conn = get_db_connection(safe_mode)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT saldo, investimento FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('Erro ao recuperar informações da conta.', 'error')
            return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()

    if request.method == 'POST':
        valor = request.form.get('valor', '').strip()  # Obter o valor bruto como string
        
        # Aplica filtragem se necessário
        if filter_input_enabled:
            valor = filter_input(valor)

        conn = get_db_connection(safe_mode)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT saldo, investimento FROM usuarios WHERE id_usuario = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                flash('Erro ao recuperar informações da conta.', 'error')
                return redirect(url_for('login'))
            
            saldo = float(user['saldo'])
            investimento = float(user['investimento'])

            if use_prepared:  # Modo seguro (prepared statements)
                print("Modo seguro (prepared statements) ativado.")
                try:
                    valor_numerico = float(valor)
                    if valor_numerico <= 0 or saldo < valor_numerico:
                        raise ValueError("Valor inválido ou saldo insuficiente.")
                    
                    novo_saldo = saldo - valor_numerico
                    novo_investimento = investimento + valor_numerico
                    
                    query = """
                    UPDATE usuarios 
                    SET saldo = %s, investimento = %s 
                    WHERE id_usuario = %s
                    """
                    valores = (Decimal(str(novo_saldo)), Decimal(str(novo_investimento)), user_id)

                    # Print da query formatada (representação aproximada)
                    print(f"Query preparada: {query}")
                    print(f"Valores: {valores}")

                    cursor.execute(query, valores)
                    
                except ValueError as e:
                    print("Query preaparada: Erro durante a execução: ", e)
                    flash(f'Erro: {e}', 'error')
                    return redirect(url_for('investimento'))
            else:  # Modo vulnerável (concatenação direta)
                print("Modo vulnerável (concatenação direta) ativado.")
                query = f"""
                UPDATE usuarios 
                SET saldo = saldo - {valor}, 
                    investimento = investimento + {valor}
                WHERE id_usuario = {user_id}
                """
                print(f"Query gerada: {query}")  
                
                cursor.execute(query)
            
            conn.commit()
            flash(f'Investimento realizado com sucesso!', 'success')
        except Exception as e:
            print(f"Erro durante a execução: {e}")  # Log de erros
            flash('Ocorreu um erro ao processar o investimento.', 'error')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('conta'))
    
    return render_template('investimento.html', user=user)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port= 5000, debug=True)
