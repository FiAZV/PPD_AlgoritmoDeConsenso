# main.py

import threading
import time
import random

class Node(threading.Thread):
    def __init__(self, node_id, nodes):
        threading.Thread.__init__(self)
        self.node_id = node_id
        self.nodes = nodes  # Lista de nós na rede
        self.state = 'Follower'
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.next_index = {}
        self.match_index = {}
        self.alive = True
        self.election_timeout = random.uniform(3.0, 5.0)
        self.last_heartbeat = time.time()

    def run(self):
        while True:
            if not self.alive:
                time.sleep(1)
                continue

            if self.state == 'Follower':
                self.follower()
            elif self.state == 'Candidate':
                self.candidate()
            elif self.state == 'Leader':
                self.leader()
            time.sleep(1)  # Ajuste para diminuir a velocidade de execução

    def follower(self):
        if time.time() - self.last_heartbeat >= self.election_timeout:
            print(f"\nNó {self.node_id}: Tempo de eleição expirado, tornando-se candidato.")
            self.state = 'Candidate'
        time.sleep(1)  # Reduz a frequência das verificações

    def candidate(self):
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1
        print(f"\nNó {self.node_id}: Iniciando eleição no termo {self.current_term}.")
        for node in self.nodes:
            if node.node_id != self.node_id and node.alive:
                vote_granted = node.request_vote(self.current_term, self.node_id)
                if vote_granted:
                    votes += 1

        if votes > len(self.nodes) // 2:
            print(f"Nó {self.node_id}: Eleito líder no termo {self.current_term} com {votes} votos.")
            self.state = 'Leader'
            for node in self.nodes:
                if node.node_id != self.node_id:
                    self.next_index[node.node_id] = len(self.log)
                    self.match_index[node.node_id] = 0
        else:
            print(f"Nó {self.node_id}: Eleição falhou no termo {self.current_term}.")
            self.state = 'Follower'
        self.last_heartbeat = time.time()
        time.sleep(1)  # Aguarda antes de iniciar outra ação

    def leader(self):
        self.send_heartbeats()
        time.sleep(1)  # Intervalo entre os heartbeats

    def send_heartbeats(self):
        print(f"\nNó {self.node_id}: Enviando batidas de coração.")
        for node in self.nodes:
            if node.node_id != self.node_id and node.alive:
                node.append_entries(self.current_term, self.node_id)
        self.last_heartbeat = time.time()

    def request_vote(self, term, candidate_id):
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.state = 'Follower'

        if self.voted_for is None or self.voted_for == candidate_id:
            self.voted_for = candidate_id
            print(f"Nó {self.node_id}: Votando em {candidate_id} no termo {term}.")
            return True
        else:
            print(f"Nó {self.node_id}: Recusou voto para {candidate_id} no termo {term}.")
            return False

    def append_entries(self, term, leader_id):
        if term >= self.current_term:
            if self.state != 'Follower':
                print(f"Nó {self.node_id}: Reconhecendo novo líder {leader_id} no termo {term}.")
            self.state = 'Follower'
            self.current_term = term
            self.last_heartbeat = time.time()
            print(f"Nó {self.node_id}: Recebeu batida de coração do líder {leader_id} no termo {term}.")
            return True
        else:
            print(f"Nó {self.node_id}: Rejeitou batida de coração do líder {leader_id} no termo {term}.")
            return False

    def crash(self):
        self.alive = False
        print(f"\nNó {self.node_id}: Falhou.")

    def recover(self):
        self.alive = True
        self.state = 'Follower'
        self.last_heartbeat = time.time()
        print(f"\nNó {self.node_id}: Recuperado e voltando como seguidor.")
