# Print Post Processes

Automação de Processos Internos com Interface Gráfica para Registro em Cartório

## Descrição

Esta aplicação, desenvolvida com interface gráfica, automatiza o processo de extração, transformação e envio de dados de clientes para registro em cartório de notas. Ela permite a seleção de arquivos em formato `.xlsx` ou `.csv`, realiza a formatação necessária e gera arquivos `.txt` conforme o layout exigido para o envio ao cartório.

Após o retorno do cartório, a aplicação também automatiza a atualização da base de dados do cliente, inserindo os dados de registro recebidos. Caso a base original não contenha os campos necessários, eles são adicionados automaticamente ao final do arquivo.

O sistema organiza todos os arquivos gerados de forma estruturada, separando-os por cliente, mês e data do processamento, além de manter uma cópia do arquivo de retorno para verificações futuras.

Além disso, para um cliente específico, a aplicação possui uma funcionalidade extra de separação dos dados entre cliente e subcliente, gerando arquivos separados em `.xlsx` para ações como envios de e-mail ou correspondências.

A aplicação também oferece visualização prévia dos arquivos de entrada e saída e mantém um log completo do processamento, incluindo links diretos para os diretórios onde os arquivos foram salvos.