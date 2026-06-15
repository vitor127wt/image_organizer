from dataclasses import dataclass
from typing import NamedTuple

# Tipo usado para categorizar imagens.
# O nivel é um int usado para criar a arvore de pastas baseadas nas tags
# 0(root) e etc..


class Tag(NamedTuple):
    nivel: int
    nome: str


@dataclass
class TagsList:
    IRL = Tag(0, "IRL")
    NIRL = Tag(0, "NIRL")
    Imagem = Tag(1, "Imagem")
    Video = Tag(1, "Video")
    Lolis = Tag(1, "Lolis")
    Ponies = Tag(1, "Ponies")
    Furrie = Tag(2, "Furrie")


if __name__ == "__main__":
    pass
