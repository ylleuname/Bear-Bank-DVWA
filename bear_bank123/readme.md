# Bear Bank - Demonstração de SQL Injection

## Visão Geral

Bear Bank é uma aplicação web educacional desenvolvida para demonstrar vulnerabilidades de SQL Injection e as práticas de segurança para preveni-las. Esta aplicação simula um sistema bancário simples e foi criada apenas para fins de aprendizado e não deve ser usada em ambiente de produção.

## Características

- Simulação de login de usuário
- Visualização de saldo e transações
- Demonstração de SQL Injection em modo vulnerável
- Implementação de práticas seguras em modo protegido

## Tecnologias Utilizadas

- Python 3.7+
- Flask (framework web)
- MySQL (banco de dados)
- HTML/CSS (frontend básico)

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/bear-bank.git
   cd bear-bank
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o MySQL:
   - Instale o MySQL se ainda não estiver instalado
   - Crie um banco de dados chamado `bear_bank`
   - Atualize o arquivo `config.py` com suas credenciais do MySQL

5. Inicialize o banco de dados:
   ```
   python init_db.py
   ```

## Uso

1. Inicie a aplicação:
   ```
   python app.py
   ```

2. Abra um navegador e acesse `http://localhost:5000`

3. Use as seguintes credenciais para testar:
   - Conta: 1234567890, Senha: password123
   - Conta: 0987654321, Senha: securepass

4. Para testar SQL Injection, ative o modo vulnerável na página de login e tente usar `' OR '1'='1` como senha.

## Advertência de Segurança

Esta aplicação contém vulnerabilidades intencionais e não deve ser usada em um ambiente de produção ou exposta à internet pública. Ela foi projetada apenas para fins educacionais em um ambiente controlado.

## Propósito Educacional

O objetivo principal desta aplicação é demonstrar:
1. Como as vulnerabilidades de SQL Injection podem ser exploradas
2. O impacto potencial de tais vulnerabilidades
3. Como implementar práticas seguras para prevenir SQL Injection

## Contribuição

Contribuições para melhorar este projeto educacional são bem-vindas. Por favor, abra uma issue para discutir mudanças propostas antes de submeter um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

## Disclaimer

Os autores deste projeto não são responsáveis por qualquer uso indevido ou danos causados pela utilização desta aplicação. Este software é fornecido "como está", sem garantias de qualquer tipo.