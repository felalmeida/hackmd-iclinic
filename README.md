# iClinic HackMD Chalenge

Implementar uma API REST [POST] /v2/prescriptions para inserir novas prescrições.

O serviço de prescrição deverá persistir no banco de dados somente os atributos recebidos no request;
Os serviços dependentes deverão ser consultados para compor os dados a serem enviados ao serviço de métricas;
Se o serviço de clínicas não responder, o request deverá seguir normalmente, pois o nome da clínica é o único atributo não obrigatório do serviço de métricas;
Os dados deverão ser integrados com o serviço de métricas, caso isso não ocorra (por qualquer motivo) deverá ser feito rollback e falhar o request;
A API REST deverá retornar um erro quando exceder o timeout e a quantidade de tentativas de algum serviço dependente;
Considere as informações abaixo para desenvolver o teste. Se tiver algum tipo de erro não mapeado fique a vontade para adicionar :)
