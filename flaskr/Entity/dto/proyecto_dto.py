from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProyectoDTO:
    id_proyecto: int
    id_usuario: int
    id_vista: int
    nombre_proyecto: str
    fecha_creacion: datetime | None
    fecha_actualizacion: datetime | None
    fecha_eliminacion: datetime | None