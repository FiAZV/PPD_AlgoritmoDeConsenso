# Descrição do Projeto

Este projeto é uma implementação simplificada do algoritmo de consenso distribuído **Raft** em Python. O objetivo é simular um ambiente distribuído onde múltiplos nós (servidores) interagem para alcançar consenso, mesmo na presença de falhas. O algoritmo Raft é conhecido por sua clareza e facilidade de entendimento em comparação com outros algoritmos de consenso, como o Paxos.

A implementação inclui:

- **Nós do sistema**: Cada nó pode assumir o papel de **Líder**, **Candidato** ou **Seguidor**.
- **Processo de eleição de líderes**: Nós iniciam eleições para selecionar um líder responsável pela coordenação do cluster.
- **Batidas de coração (Heartbeats)**: O líder envia periodicamente batidas de coração para manter sua autoridade e informar os seguidores de que está ativo.
- **Simulação de falhas e recuperações**: O sistema permite simular falhas de nós e observar como o cluster reage e se recupera dessas falhas.
- **Logs detalhados**: Fornece informações detalhadas sobre o estado e as ações de cada nó, permitindo acompanhar cada fase do consenso.

## Instruções para Configurar o Ambiente e Executar o Código

### Pré-requisitos

- **Python 3.6** ou superior instalado no sistema.
- O código utiliza apenas bibliotecas padrão do Python:
  - `threading`
  - `time`
  - `random`

## Estrutura do Projeto

- `main.py`: Contém a classe `Node`, que implementa a lógica do algoritmo Raft.
- `test.py`: Contém os casos de teste que simulam diferentes cenários utilizando a classe `Node`.

## Passos para Executar

### Clone o Repositório

Clone o repositório para o seu ambiente local:

git clone https://github.com/FiAZV/PPD_AlgoritmoDeConsenso.git


---

### 5. Explicação de Cada Fase do Algoritmo na Implementação

#### 1. Estados dos Nós

Cada nó pode estar em um dos três estados:

- **Seguidor (Follower)**: Estado inicial. O nó aguarda batidas de coração do líder ou solicitações de voto de candidatos.
- **Candidato (Candidate)**: O nó se torna candidato quando o timeout de eleição expira sem receber batidas de coração.
- **Líder (Leader)**: O nó candidato se torna líder ao receber votos da maioria dos nós.

#### 2. Timeout de Eleição e Transição para Candidato

- **Arquivo**: `main.py`
- **Método**: `follower()`

**Descrição**:

- Cada nó seguidor define um `election_timeout` aleatório entre 3 e 5 segundos.
- Se o nó não receber uma batida de coração dentro desse período, ele assume que o líder falhou e se torna um candidato.

#### 3. Processo de Eleição

- **Arquivo**: `main.py`
- **Método**: `candidate()`

**Descrição**:

- O candidato incrementa seu termo atual e vota em si mesmo.
- Envia solicitações de voto para os outros nós.
- Cada nó pode conceder seu voto a apenas um candidato por termo.
- Se o candidato receber votos da maioria, ele se torna o líder.
- Caso contrário, retorna ao estado de seguidor e aguarda um novo timeout.

#### 4. Envio de Batidas de Coração (Heartbeats)

- **Arquivo**: `main.py`
- **Métodos**: `leader()`, `send_heartbeats()`

**Descrição**:

- O líder envia batidas de coração para todos os seguidores para manter sua liderança.
- As batidas de coração são enviadas em intervalos regulares para evitar que os seguidores iniciem novas eleições.

#### 5. Recebimento de Batidas de Coração

- **Arquivo**: `main.py`
- **Método**: `append_entries()`

**Descrição**:

- Quando um seguidor recebe uma batida de coração, ele atualiza seu `last_heartbeat` e permanece no estado de seguidor.
- Se o termo do líder for maior que o do seguidor, o seguidor atualiza seu `current_term`.

#### 6. Simulação de Falhas e Recuperações

- **Arquivo**: `test.py`
- **Funções**:
  - `simulate_normal_operation(nodes)`
  - `simulate_node_failure_and_recovery(nodes)`
  - `simulate_leader_failure(nodes)`

**Descrição**:

- As funções simulam diferentes cenários, incluindo operação normal, falha de nós não líderes e falha do líder.
- Permitem observar como o algoritmo reage a essas situações e mantém o consenso.

#### 7. Logs Detalhados

A implementação inclui mensagens detalhadas que informam:

- Quando um nó muda de estado.
- Início e resultado de eleições.
- Envio e recebimento de batidas de coração.
- Falhas e recuperações de nós.
- Concessão ou recusa de votos.

## Descrição de Possíveis Falhas Simuladas e Respostas do Sistema

### Falha de um Nó Não Líder

**Simulação**:

- No `test.py`, a função `simulate_node_failure_and_recovery(nodes)` simula a falha do nó com `node_id = 2`.
- Após um período, o nó é recuperado.

**Resposta do Sistema**:

- O cluster continua operando normalmente, pois o líder permanece ativo.
- Os seguidores restantes continuam recebendo batidas de coração.
- Quando o nó falho se recupera, ele retorna como seguidor e sincroniza com o líder.

### Falha do Líder

**Simulação**:

- A função `simulate_leader_failure(nodes)` identifica o líder atual e o simula como falho.
- Após um tempo, o líder original é recuperado.

**Resposta do Sistema**:

- Os seguidores detectam a ausência de batidas de coração e iniciam uma nova eleição após seus timeouts expirarem.
- Um novo líder é eleito se um candidato obtiver votos da maioria.
- Quando o líder original se recupera, ele reconhece o novo líder se o termo atual for maior ou igual ao seu.

### Timeout de Eleição

**Simulação**:

- Se um seguidor não recebe batidas de coração dentro do `election_timeout`, ele se torna candidato automaticamente.

**Resposta do Sistema**:

- Inicia-se um processo de eleição.
- Nós votam em candidatos com termos atualizados.
- Pode haver múltiplas eleições em caso de empates, até que um líder seja eleito.

### Recuperação de Nós

**Simulação**:

- Os métodos `crash()` e `recover()` da classe `Node` permitem simular falhas e recuperações.

**Resposta do Sistema**:

- Nós recuperados retornam como seguidores e atualizam seus termos e estados com base nas batidas de coração recebidas.
- O sistema mantém o consenso, e o líder coordena a integração dos nós recuperados.

## Observações Importantes

### Limitações da Implementação

- **Replicação de Logs**: Não há implementação de replicação de logs de comandos de clientes.
- **Persistência de Estado**: Os nós não persistem seus estados; portanto, informações são perdidas em falhas.
- **Partições de Rede**: Não há simulação de partições de rede ou atrasos na comunicação.

### Objetivo Educacional

- Esta implementação tem fins educacionais, visando ilustrar os conceitos básicos do algoritmo Raft.
- Não é adequada para uso em produção ou sistemas que requerem alta confiabilidade.
