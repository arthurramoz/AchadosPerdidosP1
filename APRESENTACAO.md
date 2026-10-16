# 🎤 Roteiro de Apresentação e Guia de Arguição - Achados e Perdidos
### Disciplina: Programação Orientada a Objetos (POO) - Prova 1

> **Tempo total de apresentação da equipe:** 8 minutos cronometrados  
> **Tempo de perguntas da banca/professor:** 4 minutos  
> **Regra fundamental:** Todos os integrantes devem falar. A arguição é individual!

---

## ⏱️ Divisão do Tempo (8 Minutos)

| Bloco | Tempo | Tema | Quem Fala |
|---|---|---|---|
| **Bloco 1** | **1 min** (0:00 - 1:00) | **O Domínio:** Que sistema é esse e para quem serve | **Arthur** |
| **Bloco 2** | **2 min** (1:00 - 3:00) | **Diagrama de Classes:** Modelagem, encapsulamento e associações | **Arthur** |
| **Bloco 3** | **3 min** (3:00 - 6:00) | **API ao Vivo no `/docs`:** Demonstração prática dos endpoints, casos de erro (409 e 422) | **Bianca** |
| **Bloco 4** | **2 min** (6:00 - 8:00) | **Herança e Polimorfismo no Código:** Hierarquia, uso de `super()` e eliminação de `if` | **Bianca** (ou em conjunto) |

---

## 🗣️ Fala Passo a Passo de Cada Integrante

### 🟢 Bloco 1: O Domínio (0:00 a 1:00) — Arthur
> *"Bom dia/boa noite, professor e colegas.  
> O nosso tema sorteado foi o **Sistema de Achados e Perdidos**.  
> O objetivo desse sistema é gerenciar com segurança o fluxo de objetos esquecidos ou encontrados em um campus universitário ou espaço público.  
> Ele atende a dois públicos essenciais:  
> 1. O **Cidadão ou Aluno**, que perdeu um item e deseja consultar o acervo disponível para reivindicar o que lhe pertence;  
> 2. O **Funcionário ou Atendente**, responsável por registrar novos itens achados, validar a titularidade e lavrar o termo formal de devolução.  
> 
> Para garantir manutenibilidade e seguir o padrão adotado na disciplina com o KiOferta, estruturamos a aplicação estritamente em **4 camadas MVC com FastAPI**: `data` com mocks puros, `models` com o domínio e regras isoladas, `controllers` com a orquestração dos casos de uso, e `routes` com a interface HTTP."*

---

### 🟢 Bloco 2: O Diagrama de Classes (1:00 a 3:00) — Arthur
> *(Mostre o diagrama Mermaid na tela ou no README)*  
> *"Nossa modelagem possui exatamente **5 classes**, respeitando a regra de 3 a 5 classes sem complexidade desnecessária:  
> 
> 1. **`Item` (Entidade Principal):** Representa o objeto físico encontrado. Possui atributos protegidos como `_id`, `_nome`, `_categoria`, `_local_encontrado` e `_status` (que inicia como `'guardado'`).  
> 2. **`Usuario` (Classe Base Abstrata):** Protege `_id`, `_nome`, `_cpf` e `_senha`. Reparem que **não existe `mostrar_senha()` nem `alterar_id()`**. A conferência é feita internamente por `conferir_senha(senha)`.  
> 3. **`Cidadao` e `Funcionario` (Hierarquia de Herança em 2 Níveis):**  
>    - `Cidadao` herda de `Usuario` e possui a constante de classe `LIMITE_REIVINDICACOES = 3`.  
>    - `Funcionario` herda de `Cidadao`, amplia o limite para `LIMITE_REIVINDICACOES = 20` e estende as permissões administrativas chamando `super().obter_permissoes()`.  
> 4. **`Devolucao` (Entidade de Ligação):** Registra o evento de entrega. Ela associa um `Item` e um `Usuario` através de `_item_id` e `_usuario_id`, guardando a data e a observação da entrega.  
> 
> Todos os atributos são protegidos por convenção com sublinhado (`_`), os construtores chamam os métodos `alterar_` para que os objetos já nasçam validados, e qualquer dado inconsistente dispara `raise ValueError` diretamente na model."*

---

### 🟢 Bloco 3: Demonstração da API ao Vivo no `/docs` (3:00 a 6:00) — Bianca
> *(Abra o navegador em `http://127.0.0.1:8000/docs`)*  
> 
> 1. **Listar Itens Disponíveis (`GET /api/itens/disponiveis`):**  
>    - Execute o endpoint.  
>    - Fala: *"Aqui vemos todos os itens que ainda estão sob custódia (`status: 'guardado'`). A model filtra internamente sem expor atributos privados."*  
> 
> 2. **Cadastrar Novo Item Achado (`POST /api/itens`):**  
>    - Payload de teste:
>      ```json
>      {
>        "nome": "Calculadora Financeira",
>        "categoria": "Eletrônicos",
>        "local_encontrado": "Auditório Central"
>      }
>      ```
>    - Execute e mostre o retorno **HTTP 201 Created**.  
>    - Fala: *"O item foi criado com ID gerado dinamicamente e status inicial 'guardado'."*  
> 
> 3. **Demonstrar Caso de Erro de Validação da Model (`HTTP 422`):**  
>    - Altere o `nome` para `"   "` (espaços vazios).  
>    - Execute e mostre o retorno **HTTP 422**: `{"detail": "nome do item não pode ser vazio"}`.  
>    - Fala: *"A rota capturou o `ValueError` disparado dentro do `alterar_nome` da model e o traduziu para o código HTTP 422. A rota não valida nada por conta própria."*  
> 
> 4. **Registrar Devolução com Sucesso (`POST /api/devolucoes`):**  
>    - Payload:
>      ```json
>      {
>        "item_id": 1,
>        "usuario_id": 1,
>        "observacao": "Dono apresentou comprovante e retirou na portaria."
>      }
>      ```
>    - Execute e mostre o retorno **HTTP 201 Created**.  
> 
> 5. **Demonstrar Conflito de Estado de Negócio (`HTTP 409 Conflict`):**  
>    - Clique em **Execute** novamente com o **mesmo payload** (tentando devolver o Item 1 de novo).  
>    - Mostre o retorno **HTTP 409 Conflict**: `{"detail": "o item informado já foi devolvido anteriormente"}`.  
>    - Fala: *"O sistema impede devolução em duplicidade retornando HTTP 409, pois o estado atual do item agora é 'devolvido'."*  
> 
> 6. **Login Polimórfico (`POST /api/auth/login`):**  
>    - Teste com `{"nome": "Arthur Ramos", "senha": "art123"}` -> Retorna `perfil: "Cidadao"` e permissões restritas.  
>    - Teste com `{"nome": "Diana Silveira", "senha": "diana123"}` -> Retorna `perfil: "Funcionario"` com `cadastrar_item: true` e `registrar_devolucao: true`."*

---

### 🟢 Bloco 4: Onde está a Herança e o Polimorfismo (6:00 a 8:00) — Bianca (ou Arthur)
> *(Mostre o arquivo `app/models/usuario.py` na IDE)*  
> *"Aqui no código em `app/models/usuario.py` vemos os pilares aplicados na prática:  
> 
> 1. **A Herança:**  
>    - `Cidadao` herda de `Usuario`.  
>    - `Funcionario` herda de `Cidadao` (2 níveis de herança).  
> 
> 2. **O uso de `super()` para estender comportamento:**  
>    - Vejam o método `obter_permissoes()` dentro de `Funcionario`:  
>      ```python
>      def obter_permissoes(self):
>          permissoes = super().obter_permissoes()
>          permissoes['cadastrar_item'] = True
>          permissoes['registrar_devolucao'] = True
>          return permissoes
>      ```  
>    - `Funcionario` não duplica as permissões de base do cidadão; ele chama `super().obter_permissoes()` e apenas adiciona as permissões administrativas. Se tirássemos o `super()`, quebraríamos a extensão e teríamos repetição desnecessária de código (ferindo o princípio DRY).  
> 
> 3. **A Constante de Classe Polimórfica:**  
>    - `Cidadao.LIMITE_REIVINDICACOES = 3` e `Funcionario.LIMITE_REIVINDICACOES = 20`.  
>    - O controller checa o limite simplesmente chamando `usuario.obter_limite_reivindicacoes()`. **Não existe nenhum `if tipo == 'Cidadao'` em nenhum lugar do projeto.**  
> 
> 4. **Mapeamento via Dicionário (`catalogo_perfis`):**  
>    - No método `carregar_usuarios()`, usamos um dicionário mapeando a string do mock para a respectiva classe (`{'cidadao': Cidadao, 'funcionario': Funcionario}`). O mock instancia a classe correta dinamicamente, mantendo o código aberto para novas classes sem alterar lógica condicional."*

---

## 🎯 Guia de Respostas para as 10 Perguntas da Arguição

O professor pode chamar **qualquer integrante individualmente** para responder uma das perguntas abaixo. Decorar ou entender essas respostas garante nota máxima:

### 1. Por que vocês escolheram essas classes, e não outras?
> **Resposta:**  
> *"Porque elas modelam com precisão cirúrgica o domínio de Achados e Perdidos sem excesso de classes: `Item` representa a coisa física achada; `Usuario` (com as especializações `Cidadao` e `Funcionario`) representa as pessoas envolvidas com diferentes papéis e limites; e `Devolucao` é o registro de transação que conecta um item entregue ao usuário que o retirou."*

### 2. Onde está a herança? Por que ela se justifica aqui?
> **Resposta:**  
> *"Está na hierarquia `Usuario` $\rightarrow$ `Cidadao` $\rightarrow$ `Funcionario` em `app/models/usuario.py`. Ela se justifica porque Funcionários e Cidadãos compartilham identidade básica (ID, nome, CPF, conferência de senha e possibilidade de resgatar itens), mas possuem regras de negócio, limites de itens e permissões operacionais distintas."*

### 3. Mostre um método que usa `super()` e explique o que acontece se tirá-lo.
> **Resposta:**  
> *(Aponte para a linha do método `obter_permissoes()` na classe `Funcionario`)*  
> *"Se tirarmos o `super()`, a classe `Funcionario` deixará de reaproveitar o dicionário base de permissões herdado de `Usuario`/`Cidadao`. Teríamos que reescrever todas as chaves manualmente, duplicando código e correndo o risco de esquecer permissões caso a classe base seja atualizada no futuro."*

### 4. Onde está o polimorfismo? Que `if` ele evitou?
> **Resposta:**  
> *"O polimorfismo está na chamada `usuario.obter_permissoes()` e `usuario.obter_limite_reivindicacoes()` no controller. Ele evitou condicionais do tipo:*  
> `if usuario.mostrar_perfil() == 'Cidadao': limite = 3`  
> `elif usuario.mostrar_perfil() == 'Funcionario': limite = 20`  
> *Com polimorfismo, o controller apenas pede a informação ao objeto e cada classe responde conforma sua própria definição."*

### 5. Por que essa constante está na classe filha e não num `if` no controller?
> **Resposta:**  
> *"Porque o limite de itens que uma pessoa pode retirar é uma regra de negócio intrínseca ao papel/perfil dela (pertence à Model). Se colocássemos no controller em forma de `if`, estaríamos vazando regra de negócio para a camada de orquestração e violando o princípio do encapsulamento e do MVC."*

### 6. Se eu criar uma quarta subclasse, quantos arquivos vocês mexeriam?
> **Resposta:**  
> *"Mexeríamos apenas em **2 arquivos**:  
> 1. Em `app/models/usuario.py`, para declarar a nova classe (ex: `class Administrador(Funcionario):`) e adicionar a nova chave no dicionário `catalogo_perfis`;  
> 2. Em `app/data/usuarios_mock.py`, caso queiramos incluir um registro mockado com o novo perfil.  
> **Não mexeríamos em nenhum controller e em nenhuma rota**, comprovando o baixo acoplamento e o Princípio Aberto/Fechado (OCP)."*

### 7. Por que esta regra está na model e não no controller?
> **Resposta:**  
> *"Porque as invariantes de validação de estado (como 'nome não pode ser vazio', 'CPF deve ter 11 dígitos' e 'item não pode ser devolvido duas vezes') definem a integridade do domínio. A model é a dona do seu próprio estado e a única responsável por garantir que um objeto nunca exista em estado inválido."*

### 8. A model importa alguma coisa do FastAPI? Por que isso importa?
> **Resposta:**  
> *"Não! A camada `models` não possui nenhum import do FastAPI nem de HTTPException. Isso importa porque o domínio deve ser completamente agnóstico à infraestrutura web. Se amanhã decidirmos transformar esse sistema em uma aplicação de terminal CLI ou migrar para Django ou Flask, as models continuam funcionando sem mudar uma única linha."*

### 9. Se os mocks virassem banco de dados, quais arquivos mudariam?
> **Resposta:**  
> *"Mudaria apenas a função de carregamento na camada `models` (por exemplo `carregar_itens()` passaria a fazer uma consulta SQL/ORM em vez de ler o dicionário da pasta `data/`). Nenhum controller e nenhuma rota precisaria ser alterada, pois os controllers interagem apenas com a interface pública dos métodos da model."*

### 10. Qual é o tipo de relacionamento entre essas duas classes, e por quê?
> **Resposta:**  
> - **Entre `Item` e `Devolucao`:** Associação direcionada de $1$ para $0..*$. Uma devolução conhece o ID do item que foi devolvido, e um item pode estar associado a um registro de devolução.  
> - **Entre `Usuario` e `Devolucao`:** Associação direcionada de $1$ para $0..*$. A devolução registra quem foi o cidadão que retirou o objeto.  
> - **Entre `Usuario`, `Cidadao` e `Funcionario`:** Relacionamento de Generalização/Herança (*"é um"*), onde `Cidadao` é um `Usuario` e `Funcionario` é um `Cidadao` com privilégios adicionais.
