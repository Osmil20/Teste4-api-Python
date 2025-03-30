API de Operadoras de Planos de Saúde
Esta API fornece informações sobre operadoras de planos de saúde, permitindo consultas e busca por dados específicos armazenados em um arquivo CSV. Ela foi construída utilizando Flask para a criação da API REST e Pandas para manipulação de dados.

Funcionalidades
/operadoras: Retorna uma lista de todas as operadoras registradas.

/operadora/<cnpj>: Busca informações de uma operadora específica pelo seu CNPJ.

/search?q=<query>: Permite a busca de operadoras com base no nome fantasia, realizando uma pesquisa case-insensitive.
