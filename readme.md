# Bear Bank - Demonstração de SQL Injection

## Visão Geral

Bear Bank é uma aplicação web educacional desenvolvida para demonstrar vulnerabilidades de SQL Injection e as práticas de segurança para preveni-las. Esta aplicação simula um sistema bancário simples e foi criada apenas para fins de aprendizado e não deve ser usada em ambiente de produção.

## Características

- Simulação de login de usuário
- Visualização de saldo e transações
- Realizar investimentos fictícios
- Demonstração de SQL Injection em modo vulnerável
- Implementação de práticas seguras em modo protegido

## Tecnologias Utilizadas

- Python 3.7+
- Flask (framework web)
- MySQL (banco de dados)
- HTML/CSS/Javascript (frontend básico)

## Instalação e Execução (Ubuntu)

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/Bear-Bank-DVWA.git
   cd bear-bank
   ```

2. Dê permissão de execução para o arquivo entrypoint.sh
   ```
   sudo chmod +x entrypoint.sh
   ```

3. No primeiro acesso é necessário construir os containers, portanto use o comando
   ```
   sudo docker-compose up --build
   ```

4. Caso já tenha criado os containers, apenas o seguinte comando é suficiente para inicializar a aplicação:
   ```
   sudo docker-compose up -d
   ```

## Instalação e Execução (Windows)
Para a execução no Windows é necessário ter instalado WSL, e o Docker Desktop, configurado com integração ao WSL e distribuição Ubuntu. Após isso basta seguir os passos de 1 a 4 descritos acima.


## Uso

1. Abra um navegador e acesse `http://127.0.0.1:5000/login`

2. Para explorar melhor as funcionalidades da aplicação acompanhe o Trabalho de Conclusão de Curso "Mitigação de Ataques SQL Injection em Aplicações Web MySQL: Uma abordagem prática com Prepared Statements, Filtragem de Dados e Stored Procedure".

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
