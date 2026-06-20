
import pygame
import sys
import random
import os

pygame.init()

LARGURA = 800
ALTURA  = 600

tela    = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN| pygame.SCALED)
pygame.display.set_caption("Corrida para a Faculdade")

relogio = pygame.time.Clock()
FPS     = 60

BRANCO      = (255, 255, 255)
CINZA_CLARO = (220, 220, 220)
VERMELHO    = (215, 55,  55 )
AMARELO     = (255, 215, 0  )

fonte_titulo  = pygame.font.SysFont("Arial", 52, bold=True)
fonte_media   = pygame.font.SysFont("Arial", 32)
fonte_pequena = pygame.font.SysFont("Arial", 22)

_NOME_MONO       = "consolas,couriernew,lucidaconsole,monospace"
fonte_px_titulo  = pygame.font.SysFont(_NOME_MONO, 22, bold=True)
fonte_px_sub     = pygame.font.SysFont(_NOME_MONO, 15, bold=True)
fonte_px_corpo   = pygame.font.SysFont(_NOME_MONO, 13, bold=True)
fonte_px_dica    = pygame.font.SysFont(_NOME_MONO, 12, bold=True)
fonte_px_carimbo = pygame.font.SysFont(_NOME_MONO, 16, bold=True)


def _texto_pixel(fonte, texto, cor, centro, escala=3, cor_contorno=(18, 20, 32),
                 so_sombra=False):
    base   = fonte.render(texto, False, cor)
    w, h   = base.get_size()
    grande = pygame.transform.scale(base, (w * escala, h * escala))
    rect   = grande.get_rect(center=(int(centro[0]), int(centro[1])))
    contorno = pygame.transform.scale(
        fonte.render(texto, False, cor_contorno), (w * escala, h * escala))
    if so_sombra:
        tela.blit(contorno, (rect.x + escala, rect.y + escala))
    else:
        for dx in (-escala, 0, escala):
            for dy in (-escala, 0, escala):
                if dx or dy:
                    tela.blit(contorno, (rect.x + dx, rect.y + dy))
    tela.blit(grande, rect)
    return rect


def _painel_pixel(x, y, w, h, cor_fundo, cor_borda, cor_clara, cor_escura):
    g = 5
    pygame.draw.rect(tela, (12, 14, 24), (x - 2 * g, y - 2 * g, w + 4 * g, h + 4 * g))
    pygame.draw.rect(tela, cor_borda,    (x - g,     y - g,     w + 2 * g, h + 2 * g))
    pygame.draw.rect(tela, cor_fundo,    (x, y, w, h))
    pygame.draw.rect(tela, cor_clara,    (x, y, w, g))
    pygame.draw.rect(tela, cor_clara,    (x, y, g, h))
    pygame.draw.rect(tela, cor_escura,   (x, y + h - g, w, g))
    pygame.draw.rect(tela, cor_escura,   (x + w - g, y, g, h))
    for bx, by in [(x + 2 * g, y + 2 * g), (x + w - 3 * g, y + 2 * g),
                   (x + 2 * g, y + h - 3 * g), (x + w - 3 * g, y + h - 3 * g)]:
        pygame.draw.rect(tela, cor_escura, (bx, by, g, g))
        pygame.draw.rect(tela, cor_clara,  (bx, by, g, g), 1)


def _pixel_brilho(cx, cy, cor, g=3):
    pygame.draw.rect(tela, cor, (cx - g // 2, cy - 2 * g, max(1, g), 4 * g))
    pygame.draw.rect(tela, cor, (cx - 2 * g, cy - g // 2, 4 * g, max(1, g)))


def _desenhar_carimbo(cx, cy, vitoria):
    g = 5
    lado = 60
    x = cx - lado // 2
    y = cy - lado // 2
    if vitoria:
        corpo, claro, escuro, txt = (235, 185, 40), (255, 225, 120), (180, 130, 20), "A+"
    else:
        corpo, claro, escuro, txt = (205, 60, 60), (240, 110, 110), (150, 32, 32), "F"
    pygame.draw.rect(tela, (16, 16, 24), (x - g, y - g, lado + 2 * g, lado + 2 * g))
    pygame.draw.rect(tela, corpo,  (x, y, lado, lado))
    pygame.draw.rect(tela, claro,  (x, y, lado, g))
    pygame.draw.rect(tela, claro,  (x, y, g, lado))
    pygame.draw.rect(tela, escuro, (x, y + lado - g, lado, g))
    pygame.draw.rect(tela, escuro, (x + lado - g, y, g, lado))
    _texto_pixel(fonte_px_carimbo, txt, BRANCO, (cx, cy + 1), escala=3)


def _recortar_e_escalar(superficie, altura_alvo):
    rect = superficie.get_bounding_rect()
    if rect.width == 0 or rect.height == 0:
        return superficie
    recorte  = superficie.subsurface(rect).copy()
    escala   = altura_alvo / recorte.get_height()
    nova_larg = max(1, int(recorte.get_width() * escala))
    return pygame.transform.smoothscale(recorte, (nova_larg, altura_alvo))


PERSONAGEM = None
_caminho_personagem = os.path.join("imagens", "source.png")
if os.path.exists(_caminho_personagem):
    try:
        PERSONAGEM = _recortar_e_escalar(
            pygame.image.load(_caminho_personagem).convert_alpha(), 92)
    except Exception:
        PERSONAGEM = None

IMAGEM_FUNDO = None
_caminho_fundo = os.path.join("imagens", "background.png")
if os.path.exists(_caminho_fundo):
    try:
        IMAGEM_FUNDO = pygame.transform.scale(
            pygame.image.load(_caminho_fundo).convert(), (LARGURA, ALTURA))
    except Exception:
        IMAGEM_FUNDO = None

OBSTACULOS_IMG = []
for _nome_obs, _altura_obs in [("cone.png", 54), ("lixeira.png", 60),
                               ("relogio.png", 48), ("trave.png", 52)]:
    _caminho_obs = os.path.join("imagens", "obstaculos", _nome_obs)
    if not os.path.exists(_caminho_obs):
        continue
    try:
        _surf = _recortar_e_escalar(
            pygame.image.load(_caminho_obs).convert_alpha(), _altura_obs)
        OBSTACULOS_IMG.append({
            "surface": _surf,
            "largura": _surf.get_width(),
            "altura":  _surf.get_height(),
        })
    except Exception:
        pass

TELA_INICIAL_IMG = None
TELA_PAUSADA_IMG = None
TELA_REPROVADO_IMG = None
TELA_VENCEU_IMG = None

_arquivos_interface = {
    "tela_inicial": os.path.join("imagens", "obstaculos", "tela_inicial.png"),
    "tela_pausada": os.path.join("imagens", "obstaculos", "tela_pausada.png"),
    "tela_reprovado": os.path.join("imagens", "obstaculos", "tela_reprovado.png"),
    "tela_venceu": os.path.join("imagens", "obstaculos", "tela_venceu.png"),
}

if os.path.exists(_arquivos_interface["tela_inicial"]):
    TELA_INICIAL_IMG = pygame.transform.scale(
        pygame.image.load(_arquivos_interface["tela_inicial"]).convert_alpha(),
        (LARGURA, ALTURA),
    )
if os.path.exists(_arquivos_interface["tela_pausada"]):
    TELA_PAUSADA_IMG = pygame.transform.scale(
        pygame.image.load(_arquivos_interface["tela_pausada"]).convert_alpha(),
        (LARGURA, ALTURA),
    )
if os.path.exists(_arquivos_interface["tela_reprovado"]):
    TELA_REPROVADO_IMG = pygame.transform.scale(
        pygame.image.load(_arquivos_interface["tela_reprovado"]).convert_alpha(),
        (LARGURA, ALTURA),
    )
if os.path.exists(_arquivos_interface["tela_venceu"]):
    TELA_VENCEU_IMG = pygame.transform.scale(
        pygame.image.load(_arquivos_interface["tela_venceu"]).convert_alpha(),
        (LARGURA, ALTURA),
    )

# ajustes do jogo
CHAO_Y                = ALTURA - 110
GRAVIDADE             = 0.55
FORCA_PULO            = -14
VELOCIDADE_BASE       = 5
PONTUACAO_VITORIA     = 1000
TEMPO_INVENCIVEL      = 90
INTERVALO_OBS_INICIAL = 100
INTERVALO_OBS_MINIMO  = 48
ARQUIVO_RECORDE       = "recorde.txt"


def ler_recorde():
    try:
        with open(ARQUIVO_RECORDE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return 0


def salvar_recorde(pontuacao):
    if pontuacao > ler_recorde():
        with open(ARQUIVO_RECORDE, "w", encoding="utf-8") as f:
            f.write(str(pontuacao))
        return True
    return False


def criar_jogador():
    return {
        "x": 120, "y": CHAO_Y - 62,
        "largura": 36, "altura": 62,
        "velocidade_y": 0, "no_chao": True,
        "vidas": 3, "frames_invencivel": 0,
    }


def pular(jogador):
    if jogador["no_chao"]:
        jogador["velocidade_y"] = FORCA_PULO
        jogador["no_chao"]      = False


def atualizar_jogador(jogador):
    jogador["velocidade_y"] += GRAVIDADE
    jogador["y"]            += jogador["velocidade_y"]
    y_max = CHAO_Y - jogador["altura"]
    if jogador["y"] >= y_max:
        jogador["y"]            = y_max
        jogador["velocidade_y"] = 0
        jogador["no_chao"]      = True
    if jogador["frames_invencivel"] > 0:
        jogador["frames_invencivel"] -= 1


def _sombra_objeto(cx, largura):
    w = int(largura * 1.15)
    h = 9
    sombra = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 70), (0, 0, w, h))
    tela.blit(sombra, (cx - w // 2, CHAO_Y - h + 2))


def desenhar_jogador(jogador):
    if jogador["frames_invencivel"] > 0 and jogador["frames_invencivel"] % 8 < 4:
        return
    sw, sh = PERSONAGEM.get_size()
    cx = int(jogador["x"] + jogador["largura"] // 2)
    _sombra_objeto(cx, jogador["largura"] + 12)
    blit_x = cx - sw // 2
    blit_y = int(jogador["y"] + jogador["altura"] - sh)
    tela.blit(PERSONAGEM, (blit_x, blit_y))


def criar_obstaculo(velocidade):
    base = random.choice(OBSTACULOS_IMG)
    return {
        "x": LARGURA + 30, "y": CHAO_Y - base["altura"],
        "largura": base["largura"], "altura": base["altura"],
        "surface": base["surface"], "velocidade": velocidade,
    }


def atualizar_obstaculos(obstaculos, pontuacao):
    vel = min(VELOCIDADE_BASE + pontuacao // 100, 12)
    for obs in obstaculos:
        obs["velocidade"] = vel
        obs["x"] -= obs["velocidade"]
    for i in range(len(obstaculos) - 1, -1, -1):
        if obstaculos[i]["x"] + obstaculos[i]["largura"] < 0:
            obstaculos.pop(i)


def desenhar_obstaculos(obstaculos):
    for obs in obstaculos:
        x  = int(obs["x"])
        y  = int(obs["y"])
        cx = x + obs["largura"] // 2
        _sombra_objeto(cx, obs["largura"] + 6)
        tela.blit(obs["surface"], (x, y))


def verificar_colisao(jogador, obs):
    m   = 7
    mo  = 8
    jx1 = jogador["x"]             + m
    jx2 = jogador["x"] + jogador["largura"]  - m
    jy1 = jogador["y"]             + m
    jy2 = jogador["y"] + jogador["altura"]   - m
    ox1, ox2 = obs["x"] + mo, obs["x"] + obs["largura"] - mo
    oy1, oy2 = obs["y"] + mo, obs["y"] + obs["altura"]
    return (jx1 < ox2 and jx2 > ox1) and (jy1 < oy2 and jy2 > oy1)


def _texto_sombra(fonte, texto, cor, pos):
    sombra = fonte.render(texto, True, (0, 0, 0))
    tela.blit(sombra, (pos[0] + 2, pos[1] + 2))
    tela.blit(fonte.render(texto, True, cor), pos)


def _texto_centralizado(fonte, texto, cor, centro_x, y):
    imagem = fonte.render(texto, True, cor)
    sombra = fonte.render(texto, True, (0, 0, 0))
    rect = imagem.get_rect(midtop=(centro_x, y))
    tela.blit(sombra, (rect.x + 2, rect.y + 2))
    tela.blit(imagem, rect)


def desenhar_fundo_interface():
    if IMAGEM_FUNDO is not None:
        tela.blit(IMAGEM_FUNDO, (0, 0))
    else:
        tela.fill((0, 0, 0))


def desenhar_cenario(frame_contador):
    offset = frame_contador % LARGURA
    tela.blit(IMAGEM_FUNDO, (-offset, 0))
    tela.blit(IMAGEM_FUNDO, (LARGURA - offset, 0))


def desenhar_hud(pontuacao, vidas, recorde):
    painel_esq = pygame.Surface((320, 68), pygame.SRCALPHA)
    painel_esq.fill((0, 0, 0, 110))
    tela.blit(painel_esq, (4, 4))

    _texto_sombra(fonte_pequena, f"Pontos: {pontuacao} / {PONTUACAO_VITORIA}", BRANCO, (12, 9))

    larg_barra = 290
    progresso  = min(pontuacao / PONTUACAO_VITORIA, 1.0)
    pygame.draw.rect(tela, (60, 60, 60),  (10, 34, larg_barra, 14), border_radius=7)
    if progresso > 0:
        pygame.draw.rect(tela, AMARELO,   (10, 34, int(larg_barra * progresso), 14), border_radius=7)
    pygame.draw.rect(tela, BRANCO,        (10, 34, larg_barra, 14), border_radius=7, width=1)

    _texto_sombra(fonte_pequena, f"Recorde: {recorde}", CINZA_CLARO, (12, 52))

    painel_dir = pygame.Surface((170, 64), pygame.SRCALPHA)
    painel_dir.fill((0, 0, 0, 110))
    tela.blit(painel_dir, (LARGURA - 174, 4))
    _texto_sombra(fonte_pequena, f"Vida: {vidas}", BRANCO, (LARGURA - 162, 22))

    painel_rodape = pygame.Surface((380, 22), pygame.SRCALPHA)
    painel_rodape.fill((0, 0, 0, 90))
    tela.blit(painel_rodape, (6, ALTURA - 26))
    _texto_sombra(fonte_pequena, "ESPAÇO/↑=pular   P=pausar   ESC=menu", CINZA_CLARO, (10, ALTURA - 25))


def desenhar_pausa():
    desenhar_fundo_interface()
    if TELA_PAUSADA_IMG is not None:
        tela.blit(TELA_PAUSADA_IMG, (0, 0))
    else:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((10, 12, 24, 170))
        tela.blit(overlay, (0, 0))


def tela_menu():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return "jogar"

        recorde = ler_recorde()

        desenhar_fundo_interface()

        if TELA_INICIAL_IMG is not None:
            tela.blit(TELA_INICIAL_IMG, (0, 0))

        _texto_centralizado(fonte_pequena, f"Recorde: {recorde}", AMARELO, LARGURA // 2, ALTURA - 100)

        pygame.display.flip()
        relogio.tick(FPS)


def tela_jogo():
    jogador         = criar_jogador()
    obstaculos      = []
    pontuacao       = 0
    frame_contador  = 0
    timer_obstaculo = 0
    pausado         = False
    frames_flash    = 0
    recorde         = ler_recorde()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ("sair", pontuacao)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado
                if evento.key == pygame.K_ESCAPE:
                    return ("menu", pontuacao)
                if not pausado and evento.key in (pygame.K_SPACE, pygame.K_UP):
                    pular(jogador)
                if pausado and evento.key == pygame.K_SPACE:
                    pausado = False

        if not pausado:
            if frame_contador % 3 == 0:
                pontuacao += 1

            atualizar_jogador(jogador)

            intervalo = max(INTERVALO_OBS_MINIMO, INTERVALO_OBS_INICIAL - pontuacao // 15)
            timer_obstaculo += 1
            if timer_obstaculo >= intervalo:
                vel = min(VELOCIDADE_BASE + pontuacao // 100, 12)
                obstaculos.append(criar_obstaculo(vel))
                timer_obstaculo = 0

            atualizar_obstaculos(obstaculos, pontuacao)

            for obs in obstaculos:
                if jogador["frames_invencivel"] == 0 and verificar_colisao(jogador, obs):
                    jogador["vidas"] -= 1
                    jogador["frames_invencivel"] = TEMPO_INVENCIVEL
                    frames_flash = 20

            if frames_flash > 0:
                frames_flash -= 1

            if pontuacao >= PONTUACAO_VITORIA:
                return ("vitoria", pontuacao)
            if jogador["vidas"] <= 0:
                return ("derrota", pontuacao)

            frame_contador += 1

        desenhar_cenario(frame_contador)
        desenhar_obstaculos(obstaculos)
        desenhar_jogador(jogador)
        desenhar_hud(pontuacao, jogador["vidas"], recorde)

        if frames_flash > 0:
            fl = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            fl.fill((200, 0, 0, int(120 * frames_flash / 20)))
            tela.blit(fl, (0, 0))

        if pausado:
            desenhar_pausa()

        pygame.display.flip()
        relogio.tick(FPS)


def tela_game_over(pontuacao, vitoria, novo_recorde):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return "menu"

        desenhar_fundo_interface()

        if vitoria and TELA_VENCEU_IMG is not None:
            tela.blit(TELA_VENCEU_IMG, (0, 0))
        elif not vitoria and TELA_REPROVADO_IMG is not None:
            tela.blit(TELA_REPROVADO_IMG, (0, 0))

        pygame.display.flip()
        relogio.tick(FPS)


def main():
    estado    = "menu"
    pontuacao = 0

    while True:
        if estado == "menu":
            estado = tela_menu()
        elif estado == "jogar":
            estado, pontuacao = tela_jogo()
        elif estado in ("vitoria", "derrota"):
            novo_recorde = salvar_recorde(pontuacao)
            estado = tela_game_over(pontuacao, estado == "vitoria", novo_recorde)
        elif estado == "sair":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()

