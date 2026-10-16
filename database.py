
from sqlmodel import create_engine, Session

# Configuracion de la base de datos
DATABASE_URL = "sqlite:///./base_de_datos.db"

# Crear la conexion
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Obtener una sesion de la base de datos
def get_db():
    with Session(engine) as db:
        yield db
