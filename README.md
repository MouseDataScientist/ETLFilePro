# Print Post Processes

Automação de Processos Internos com Interface Gráfica para Registro em Cartório

## Descrição

Esta aplicação, desenvolvida com interface gráfica, automatiza o processo de extração, transformação e envio de dados de clientes para registro em cartório de notas. Ela permite a seleção de arquivos em formato `.xlsx` ou `.csv`, realiza a formatação necessária e gera arquivos `.txt` conforme o layout exigido para o envio ao cartório.

Após o retorno do cartório, a aplicação também automatiza a atualização da base de dados do cliente, inserindo os dados de registro recebidos. Caso a base original não contenha os campos necessários, eles são adicionados automaticamente ao final do arquivo.

O sistema organiza todos os arquivos gerados de forma estruturada, separando-os por cliente, mês e data do processamento, além de manter uma cópia do arquivo de retorno para verificações futuras.

Além disso, para um cliente específico, a aplicação possui uma funcionalidade extra de separação dos dados entre cliente e subcliente, gerando arquivos separados em `.xlsx` para ações como envios de e-mail ou correspondências.

A aplicação também oferece visualização prévia dos arquivos de entrada e saída e mantém um log completo do processamento, incluindo links diretos para os diretórios onde os arquivos foram salvos.

## Instalação

Clone o repositório:

git clone https://github.com/MouseDataScientist/print_post_processes.git

Instale as dependências:

pip install -r requirements.txt

Execute a aplicação:

python main.py

## Uso

Abra a aplicação.

Selecione o arquivo do cliente em .xlsx ou .csv.

Execute o processamento para gerar o arquivo .txt conforme o layout esperado pelo cartório.

Após o retorno do cartório, selecione o arquivo de retorno e atualize automaticamente a base de dados do cliente.

Utilize a visualização dos arquivos e o log de processamento para conferência e acesso rápido aos diretórios.

## Tecnologias Utilizadas

Python

Tkinter (interface gráfica)

Pandas (manipulação de dados)

Openpyxl (manipulação de arquivos Excel)

OS (organização de diretórios)

## Funcionalidades

Seleção e leitura de arquivos .xlsx ou .csv do cliente.

Extração e transformação dos dados para o layout de envio ao cartório em .txt separado por tabulação.

Atualização automática da base do cliente com dados de retorno do cartório.

Criação de novos campos na base do cliente, quando necessário.

Organização automática dos arquivos em diretórios por cliente, mês e data.

Salvamento do arquivo de retorno do cartório para verificações futuras.

Separação de dados de cliente e subcliente em arquivos .xlsx separados.

Visualização prévia dos arquivos de entrada e saída.

Log de processamento com link direto para os diretórios dos arquivos gerados.