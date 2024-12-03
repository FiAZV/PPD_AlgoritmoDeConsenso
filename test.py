# test.py

from main import Node
import time

def simulate_normal_operation(nodes):
    print("\n--- Início do Teste: Operação Normal ---")
    # Deixe o sistema operar normalmente por um período
    time.sleep(10)
    print("\n--- Fim do Teste: Operação Normal ---")

def simulate_node_failure_and_recovery(nodes):
    print("\n--- Início do Teste: Falha e Recuperação de Nó ---")
    # Falha de um nó não líder
    nodes[2].crash()
    time.sleep(10)
    # Recuperação do nó
    nodes[2].recover()
    time.sleep(10)
    print("\n--- Fim do Teste: Falha e Recuperação de Nó ---")

def simulate_leader_failure(nodes):
    print("\n--- Início do Teste: Falha do Líder ---")
    # Identifica o líder atual
    current_leader = None
    for node in nodes:
        if node.state == 'Leader':
            current_leader = node
            break

    if current_leader:
        print(f"\nFalha do líder atual: Nó {current_leader.node_id}")
        current_leader.crash()
    else:
        print("\nNenhum líder foi identificado para falha.")

    # Aguarda tempo suficiente para eleição de um novo líder
    time.sleep(10)

    # Recupera o nó que falhou
    if current_leader:
        current_leader.recover()

    time.sleep(10)
    print("\n--- Fim do Teste: Falha do Líder ---")

if __name__ == '__main__':
    nodes = []
    num_nodes = 5
    for i in range(num_nodes):
        node = Node(i, [])
        nodes.append(node)

    for node in nodes:
        node.nodes = nodes  # Atualiza a lista de nós

    for node in nodes:
        node.start()

    # Executa testes sequencialmente
    simulate_normal_operation(nodes)
    simulate_node_failure_and_recovery(nodes)
    simulate_leader_failure(nodes)

    # Manter o programa rodando
    while True:
        time.sleep(1)
