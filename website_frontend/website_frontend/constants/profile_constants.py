from collections.abc import Mapping

from website_frontend.model.avatar_status import AvatarStatus

# ===============================
# Estados del Avatar / Disponibilidad
# ===============================
AVAILABILITY_STATES: dict[str, dict[str, str]] = {
    "activo": {
        "text": "Disponible para proyectos freelance — Respuesta rápida",
        "class_name": "is-active",
        "icon": "fa-bolt",
    },
    "pausado": {
        "text": "En proyectos activos — Disponibilidad limitada",
        "class_name": "is-paused",
        "icon": "fa-pause",
    },
    "no-disponible": {
        "text": "No aceptando nuevos proyectos por ahora",
        "class_name": "is-unavailable",
        "icon": "fa-ban",
    },
    "empleo": {
        "text": "Buscando oportunidades Full-Time — Disponible para entrevistas",
        "class_name": "is-hiring",
        "icon": "fa-magnifying-glass",
    },
    "consultoria": {
        "text": "Disponible para consultoría especializada — Corto plazo",
        "class_name": "is-consulting",
        "icon": "fa-laptop-code",
    },
    "tiempo-completo": {
        "text": "Trabajo en jornada completa — Disponibilidad mínima",
        "class_name": "is-fulltime",
        "icon": "fa-briefcase",
    },
    "aprendizaje": {
        "text": "En actualización — Aprendiendo nuevas tecnologías",
        "class_name": "is-learning",
        "icon": "fa-graduation-cap",
    },
    "viajando": {
        "text": "Fuera de oficina — Respuesta lenta",
        "class_name": "is-traveling",
        "icon": "fa-plane",
    },
    "mantenimiento": {
        "text": "En mantenimiento programado — Consultas por prioridad",
        "class_name": "is-maintenance",
        "icon": "fa-wrench",
    },
    "transmisión": {
        "text": "Creando contenido — Disponible luego",
        "class_name": "is-streaming",
        "icon": "fa-video",
    },
    "enfoque": {
        "text": "En modo enfoque — Notificaciones limitadas",
        "class_name": "is-focus",
        "icon": "fa-eye",
    },
}


def _build_avatar_status(key: str, payload: object) -> AvatarStatus | None:
    if not isinstance(payload, Mapping):
        return None

    text = payload.get("text")
    class_name = payload.get("class_name")
    icon = payload.get("icon")

    if not isinstance(text, str) or not text.strip():
        return None

    if not isinstance(class_name, str) or not class_name.strip():
        return None

    if not isinstance(icon, str) or not icon.strip():
        return None

    return AvatarStatus(
        key=key,
        text=text.strip(),
        class_name=class_name.strip(),
        icon=icon.strip(),
    )


def resolve_availability_status(raw_key: object, *, default_key: str) -> AvatarStatus:
    default_status = _build_avatar_status(
        default_key, AVAILABILITY_STATES.get(default_key)
    )
    if default_status is None:
        msg = f"Invalid default availability status catalog entry: {default_key}"
        raise ValueError(msg)

    if not isinstance(raw_key, str):
        return default_status

    normalized_key = raw_key.strip().strip('"').strip("'").lower()
    if not normalized_key:
        return default_status

    return (
        _build_avatar_status(normalized_key, AVAILABILITY_STATES.get(normalized_key))
        or default_status
    )


# ===============================
# Tecnologías del Perfil
# ===============================
TECHNOLOGIES = [
    {"name": "Angular", "color": "#DD0031", "icon_class": "fa-brands fa-angular"},
    {"name": ".NET", "color": "#5C2D91", "icon_class": "fa-solid fa-code"},
    {"name": "Node.js", "color": "#339933", "icon_class": "fa-brands fa-node-js"},
    {"name": "PHP", "color": "#777BB4", "icon_class": "fa-brands fa-php"},
    {"name": "Azure", "color": "#0078D4", "icon_class": "fa-brands fa-microsoft"},
]
