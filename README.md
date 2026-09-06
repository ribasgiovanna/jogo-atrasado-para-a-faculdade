# 🎓 Corrida para a Faculdade

Jogo 2D de corrida infinita feito em **Python + Pygame**. Um estudante está atrasado
para a aula e precisa desviar dos obstáculos da cidade para chegar a tempo.
Alcançar **1000 pontos = aprovado**; perder as **3 vidas = reprovado**.

> Projeto acadêmico para praticar lógica de jogo e programação orientada a estados.

## 🎮 Telas

| Início | Vitória | Derrota |
|---|---|---|
| ![Tela inicial](imagens/obstaculos/tela_inicial.png) | ![Tela de vitória](imagens/obstaculos/tela_venceu.png) | ![Tela de derrota](imagens/obstaculos/tela_reprovado.png) |

_A fazer: incluir um GIF de gameplay real._

## ✨ O que o jogo tem

- **Máquina de estados** clara: menu → jogo → fim (vitória ou derrota) → menu
- **Física de pulo** com gravidade e força de salto
- **Obstáculos aleatórios** (cone, lixeira, relógio, trave) com intervalo que diminui
  conforme a pontuação sobe
- **Dificuldade progressiva**: a velocidade aumenta a cada 100 pontos, até um teto
- **3 vidas** com invencibilidade temporária e efeito de piscar após a colisão
- **HUD** com barra de progresso até a meta, pontuação, recorde e vidas
- **Recorde persistente** salvo em `recorde.txt` (mantido fora do versionamento)
- **Cenário com rolagem contínua**, sombras e telas de menu/pausa/fim com arte própria
- **Fallback**: se algum arquivo de imagem faltar, o jogo continua rodando com formas simples

## 🕹️ Controles

| Tecla | Ação |
|---|---|
| `Espaço` ou `↑` | Pular |
| `P` | Pausar / retomar |
| `Esc` | Voltar ao menu |

## 🛠️ Tecnologias

- Python 3
- Pygame

## 📁 Estrutura

```
.
├── main.py              # jogo completo: estados, física, colisão e renderização
└── imagens/
    ├── background.png   # cenário
    ├── source.png       # sprite do personagem
    └── obstaculos/      # obstáculos + telas de interface (início, pausa, vitória, derrota)
```

## ▶️ Como executar

```bash
pip install pygame
python main.py
```

O jogo abre em **tela cheia** (`pygame.FULLSCREEN | pygame.SCALED`). Use `Esc` para voltar
ao menu e feche a janela para encerrar.

## 👤 Autoria

Programação de autoria de **Giovanna Ribas dos Reis** — projeto acadêmico individual.

## 🧭 Próximos passos possíveis

- Incluir uma captura ou GIF de gameplay real neste README
- Modo em janela como alternativa à tela cheia
- Revisar o texto da arte da tela inicial (está escrito "PRESSTONE")

## 🤖 Transparência

- O código do jogo (`main.py`) é de autoria própria, sem geração por IA.
- Os assets visuais em `imagens/` (cenário, personagem e telas de interface) foram
  gerados por IA.
