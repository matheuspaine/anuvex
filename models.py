from typing import Literal, Annotated
from decimal import Decimal
from pydantic import StringConstraints, ConfigDict
from pydantic import BaseModel, Field

class Produto(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    nome: str = Field(min_length=2, max_length=100)
    estado: str = Field(min_length=2, max_length=50)
    caracteristicas: str = Field(max_length=500)
    preco: Decimal = Field(ge=Decimal("0.01"), max_digits=12, decimal_places=2, allow_inf_nan=False)


class Anuncio(BaseModel):
    titulo: str = Field(min_length=3, max_length=160)
    descricao: str = Field(min_length=5, max_length=750)


class AnaliseIA(BaseModel):
    categoria: Literal["Informática", "Celulares", "Eletrônicos", "Casa e decoração", "Moda", "Esportes", "Veículos", "Outros"]
    perguntas: list[Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=180)]] = Field(max_length=6)
