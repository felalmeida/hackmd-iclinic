# iClinic HackMD Chalenge

Implementar uma API REST [POST] /v2/prescriptions para inserir novas prescrições.

O serviço de prescrição deverá persistir no banco de dados somente os atributos recebidos no request;
Os serviços dependentes deverão ser consultados para compor os dados a serem enviados ao serviço de métricas;
Se o serviço de clínicas não responder, o request deverá seguir normalmente, pois o nome da clínica é o único atributo não obrigatório do serviço de métricas;
Os dados deverão ser integrados com o serviço de métricas, caso isso não ocorra (por qualquer motivo) deverá ser feito rollback e falhar o request;
A API REST deverá retornar um erro quando exceder o timeout e a quantidade de tentativas de algum serviço dependente;
Considere as informações abaixo para desenvolver o teste. Se tiver algum tipo de erro não mapeado fique a vontade para adicionar :)

----

## Comentários (Felipe Almeida)

Seguindo as instruções descritas neste [documento](https://hackmd.io/@pX9Js4-PQPyDJikx2c84JQ/SkrdPmct4?type=view#Servi%C3%A7os-dependentes), segue abaixo algumas considerações.

* Nas instruções (item 1) é informado que só deverá persistir em banco de dados as informações recebidas no request. Porém na minha solução, além destas informações eu guardei também a informação de timestamp do dado para conseguir realizar a lógica do TTL;
* É informado também (item 3 das instruções), que para o serviço de métricas não é obrigatório a informação dos atributos referente as clínicas, no meu código eu contemplei esta situação fazendo com que um erro no serviço de clínicas não interrompa o processo e também passando ao serviço de métricas um payload sem a informação da clínica (quando ocorrer essa situação). Porém o serviço de métricas retorna erro quando não é informado os atributos da clínica. De qualquer maneira mantive o código assim (conforme as instruções);
* É possível verificar também, que no "Response.body" existe um "id" que não está associado a nenhum dos requests que devem ser realizados, e também não existe nenhuma informação sobre este parâmetro nas instruções. Isso posto, o que eu fiz foi retornar um contador de requisições 'POST' recebidas neste id. Ele não possui nenhuma persistência e portanto caso o programa seja reiniciado ele voltará a contar a partir do 1;

### Execução
Este programa é dependente de uma instância de MongoDB, eu utilizei um contâiner docker executando a versão 4.0.11. Como este desenvolvimento é para fins educacionais/teste nenhuma camada de segurança foi utilizada.

```
As informações da sua instância (IP e Porta) deverão ser preenchidas na linha 20 do programa.
```

Após estas alterações basta executar o programa com o Python 3, atentando-se para as bibliotecas dependentes.