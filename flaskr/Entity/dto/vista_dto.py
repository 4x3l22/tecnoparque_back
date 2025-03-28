from dataclasses import dataclass
from datetime import datetime

@dataclass
class VistaDTO:
    id_vista: int
    descripcion: str
    fecha_creacion: datetime | None
    fecha_actualizacion: datetime | None
    fecha_eliminacion: datetime | None
    ruta: str
    nombre: str
