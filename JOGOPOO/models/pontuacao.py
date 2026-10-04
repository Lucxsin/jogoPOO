import datetime

from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    IntegerField,
    FloatField,
    DateTimeField,
    PeeweeException,
)

# Conexão com o banco SQLite (o arquivo ranking.db é criado automaticamente)
db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    """Classe base: todos os modelos do jogo herdam daqui e usam o mesmo banco."""

    class Meta:
        database = db


class Pontuacao(BaseModel):
    """Cada linha da tabela 'pontuacao' é uma partida finalizada."""

    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"

    @classmethod
    def registrar(cls, nome, pontos, tempo):
        """CREATE: grava uma partida. Devolve o registro, ou None se der erro."""
        try:
            return Pontuacao.create(
                nome_jogador=nome,
                pontos=pontos,
                tempo_partida=tempo,
            )
        except PeeweeException as erro:
            print(f"Erro ao salvar a pontuação: {erro}")
            return None

    @classmethod
    def top10(cls):
        """READ: as 10 maiores pontuações, da maior para a menor."""
        consulta = Pontuacao.select().order_by(Pontuacao.pontos.desc()).limit(10)
        return list(consulta)


def iniciar_banco():
    """Abre a conexão e cria a tabela caso ela ainda não exista."""
    db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])