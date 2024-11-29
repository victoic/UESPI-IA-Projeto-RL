# Projeto de IA - Aprendizagem Não-supervisionada

Esse projeto apresenta uma competição entre dois times de 3 agentes. Agentes podem realizar 10 ações diferentes:

0. Mover para a direita
1. Mover para a baixo-direita
2. Mover para baixo
3. Mover para a baixo-esquerda
4. Mover para a esquerda
5. Mover para a cima-esquerda
6. Mover para cima
7. Mover para a cima-direita
8. Atacar (causa sua força em dano nos seus 8-vizinhos)
9. Esperar (não fazer nada)

Modelos devem ser treinados para sair o índice de uma dessas ações (0-9).

**Exemplo de chamada - (treinamento)**: `python main.py -t -t0m="meu_modulo" -t0c="minha_classe" -t1m="random_ai" -t1c="DumbAI" -mw=20 -mh=20`

**Exemplo de chamada - (apresentação)**: `python main.py -p -t0m="meu_modulo" -t0c="minha_classe" -t1m="random_ai" -t1c="DumbAI" -mw=20 -mh=20`

**Exemplo de chamada - (teste)**: `python main.py -e -t0m="meu_modulo" -t0c="minha_classe" -t1m="random_ai" -t1c="DumbAI" -mw=20 -mh=20`
No teste, a execução (sem apresentação) será repetida 10.000 e as porcentagens de vitórias, derrotas e empates serão exibidas na tela.

Caso um modelo necessite de acesso a uma chave para o carregamento (usando torch.load), use o argumento **-k0** (ou **-k1**) para especificar a string da chave que deseja acessar.

## Resultados 2024.2

Os valores de vitórias, empates e derrotas são relacionados a 10.000 repetições contra um adiversário RandomAI. Seguindo o seguinte comando:

`python main.py -e -t0m="meu_modulo" -t0c="minha_classe" -t1m="random_ai" -t1c="DumbAI" -mw=20 -mh=20`

Detalhamentos sobre o torneio são encontrados abaixo.

| Aluno     | Modelo  | Pontos (Torneio) | Vitórias | Empates | Derrotas |
| --------- | ------- | ---------------- | -------- | ------- | -------- |
| Willian   | DDQN    | 12               | 64,85%   | 30,53%  | 4,62%    |
| Marcos    | Genetic     | 3            | 42,34%   | 33,95%  | 23,71%   |
| Cintia    | DuelingDQN | 0             | 33,73%   | 33,72%  | 32,55%   |

### Torneio

O torneio seguiu uma série de testes entre modelos com melhores de 5 e respeitando todas as combinações possíveis de testes. Vitórias representam 3 pontos, empates representam 1 ponto e derrotas 0 pontos. As seguintes partidas foram jogadas:

| Modelo 0        | Modelo 1 | Vitórias |
| -------------   | ------   | ------   |
| DuelingQNetwork | **RandomAI** | 2x3 |
| **DDQN**        | RandomAI | 5x0 |
| Genetic	      | RandomAI | 1x1 |
| **DumbAI**          | RandomAI | 5x0 |
| DuelingQNetwork | **DumbAI**   | 0x5 |
| Genetic         | **DumbAI**   | 0x5 |
| **DDQN**            | DumbAI   | 3x1 |
| DuelingQNetwork | **Genetic**  | 0x3 |
| **DDQN**            | Genetic  | 2x0 |
| DuelingQNetwork | **DDQN**     | 0x5 |

A tabela abaixo apresenta os resultados do torneiro em classificação.

| Classificação | Modelo      | Pontos |
| ------------- | ------      | ------ |
| 1º            | DDQN        | 12     |
| 2º            | DumbAI      | 9      |
| 3º            | RandomAI    | 4      |
| 4º            | Genetic     | 3      |
| 5º            | DuelingQNet | 0      |