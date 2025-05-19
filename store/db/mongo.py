from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings


class MongoClient:
    """
    Classe para gerenciar a conexão com o MongoDB.
    O cliente é inicializado uma vez quando uma instância de MongoClient é criada.
    """
    client: AsyncIOMotorClient  

    def __init__(self) -> None:
        """
        Inicializa o AsyncIOMotorClient usando a DATABASE_URL das configurações.
        """
        print(
            f"MongoClient: Inicializando conexão com MongoDB usando URL: {settings.DATABASE_URL}")
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL)

    def get(self) -> AsyncIOMotorClient:
        """
        Retorna a instância do cliente AsyncIOMotorClient já inicializada.
        """
        return self.client

    async def close(self):
        """
        Fecha a conexão com o MongoDB.
        """
        if self.client:

            print(
                "MongoClient: 'Fechando' a lógica do cliente MongoDB (o Motor gerencia as conexões reais).")
            self.client = None
db_client = MongoClient()
