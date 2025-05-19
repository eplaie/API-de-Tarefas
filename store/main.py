from fastapi import FastAPI
from store.core.config import settings
from store.controllers.tarefas import router as tarefas_router
from store.db.mongo import db_client
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Gere eventos de inicialização e desligamento da aplicação.
    """
    print("Aplicação a iniciar com lifespan...")
    try:
        client_instance = db_client.get()
        print(
            f"Configuração do cliente MongoDB acedida (lifespan). A ligar a: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"Erro durante o evento de startup do MongoDB (lifespan): {e}")

    yield

    print("Aplicação a desligar (lifespan)...")
    if hasattr(db_client, "close") and callable(getattr(db_client, "close")):
        print("Lógica de fecho do wrapper do cliente MongoDB executada (lifespan, se aplicável).")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
    description="Uma API para gerir as suas tarefas diárias.",
    root_path=settings.ROOT_PATH,
    lifespan=lifespan
)

# --- Rota Raiz ---


@app.get("/", tags=["Root"])
async def ler_raiz():
    """
    Endpoint raiz da API.
    Retorna uma mensagem de boas-vindas.
    """
    return {"message": f"Bem-vindo à {settings.PROJECT_NAME}!"}


app.include_router(tarefas_router, prefix="/tarefas")
