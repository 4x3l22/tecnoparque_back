from dataclasses import dataclass
from datetime import datetime


@dataclass
class UsuarioDTO:
    id_usuario: int
    nombre: str
    correo: str
    contrasena: str
    fecha_creacion: datetime | None
    fecha_actualizacion: datetime | None
    fecha_eliminacion: datetime | None