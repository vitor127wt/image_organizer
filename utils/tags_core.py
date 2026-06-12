from typing import NamedTuple

# Tipo usado para categorizar imagens.
# O nivel é um int usado para criar a arvore de pastas baseadas nas tags
# 0(root) e etc..


class Tag(NamedTuple):
    nivel: int
    nome: str


class TagsList:
    IRL = Tag(0, "IRL")
    NIRL = Tag(0, "NIRL")
    FOTOS = Tag(1, "FOTOS")
    VIDEOS = Tag(1, "VIDEOS")
    LOLIS = Tag(1, "LOLIS")
    PONYS = Tag(1, "PONYS")
    FURRIES = Tag(2, "FURRIES")
