Sistema de Gerenciamento de Renda

Sistema web auto-hospedado para controle financeiro pessoal, desenvolvido com foco em simplicidade, privacidade e gerenciamento local de dados.
A aplicação permite registrar rendas, despesas e acompanhar o saldo restante por período através de dashboards e gráficos interativos.

Recursos
Registro de entradas financeiras e gastos
Histórico completo de movimentações
Dashboard mensal com análise de:
renda total
gastos totais
saldo restante
Gráficos interativos utilizando Chart.js
Armazenamento local em JSON
Interface web leve e de fácil utilização
Funcionamento offline em ambiente local
Estrutura simples para expansão futura
Tecnologias Utilizadas
Python
Flask
HTML5
JavaScript
Chart.js
Objetivo do Projeto

O objetivo deste projeto é fornecer uma solução financeira leve e acessível para uso pessoal ou doméstico, priorizando:

privacidade dos dados
independência de serviços externos
facilidade de implantação local
baixo consumo de recursos
Estrutura do Projeto
/app.py          # Backend Flask
/index.html      # Interface principal
/dados.json      # Banco de dados local
/run.bat         # Inicialização rápida no Windows
Funcionalidades Futuras
Sistema de autenticação
Categorias de despesas
Exportação de relatórios
Metas financeiras
Backup automático
Suporte multiusuário
Tema escuro
API REST
Execução Local

Instale as dependências:

pip install flask

Inicie a aplicação:

python app.py

Depois acesse:

http://127.0.0.1:5000
Licença

Este projeto está licenciado sob a GNU AGPL v3.
