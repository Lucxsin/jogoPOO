import random
from PIL import Image, ImageDraw

TAM = 200          # tamanho de cada quadro
BASE_Y = 170       # linha onde os "pés" ficam em todos os quadros

# (largura, altura) relativas -> deformação de cada quadro
FORMAS = [
    (1.00, 1.00),  # 0 parado
    (1.05, 0.94),  # 1 caminhada: agachado
    (1.00, 1.00),  # 2 caminhada: normal
    (0.95, 1.06),  # 3 caminhada: esticado
    (1.00, 1.00),  # 4 caminhada: normal
    (0.92, 1.12),  # 5 pulo / queda
]


def montar_linha(arquivo):
    original = Image.open(f"sprites/{arquivo}").convert("RGBA")
    quadro = original.crop((100, 100, 400, 400)).resize((TAM, TAM), Image.LANCZOS)
    corpo = quadro.crop(quadro.getbbox())

    linha = Image.new("RGBA", (TAM * len(FORMAS), TAM), (0, 0, 0, 0))
    for i, (sx, sy) in enumerate(FORMAS):
        w, h = int(corpo.width * sx), int(corpo.height * sy)
        forma = corpo.resize((w, h), Image.LANCZOS)
        x = i * TAM + (TAM - w) // 2
        y = BASE_Y - h
        linha.alpha_composite(forma, (x, y))
    return linha


def gerar_spritesheet():
    folha = Image.new("RGBA", (TAM * len(FORMAS), TAM * 2), (0, 0, 0, 0))
    folha.alpha_composite(montar_linha("gb_direita.png"), (0, 0))
    folha.alpha_composite(montar_linha("gb_esquerda.png"), (0, TAM))
    folha.save("sprites/jogador_sheet.png")


def gerar_bloco():
    random.seed(7)
    t = 50
    img = Image.new("RGBA", (t, t), (92, 24, 46, 255))
    d = ImageDraw.Draw(img)
    for _ in range(35):
        x, y, r = random.randint(0, t), random.randint(0, t), random.randint(1, 3)
        tom = random.randint(-14, 18)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(92 + tom, 24 + tom // 2, 46 + tom // 2, 255))
    d.rectangle((0, 0, t - 1, t - 1), outline=(55, 10, 28, 255))
    d.line((1, 1, t - 2, 1), fill=(205, 95, 105, 255), width=3)
    img.save("sprites/bloco.png")


if __name__ == "__main__":
    gerar_spritesheet()
    gerar_bloco()
    print("Assets gerados em sprites/")