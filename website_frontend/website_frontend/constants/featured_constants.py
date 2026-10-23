from website_frontend.model.project_status import ProjectStatus

# Mapeo de estados del proyecto (colores y animaciones)
PROJECT_STATUS_CONFIG: dict[str, ProjectStatus] = {
    "dev": ProjectStatus(
        key="dev",
        label="En Desarrollo",
        color="#FBBF24",
        bg_color="rgba(251, 191, 36, 0.15)",
        icon="code",
        animation_class="animate-pulse-dev",
    ),
    "migration": ProjectStatus(
        key="migration",
        label="En Migración",
        color="#FB923C",
        bg_color="rgba(251, 146, 60, 0.15)",
        icon="move",
        animation_class="animate-fade-migration",
    ),
    "testing": ProjectStatus(
        key="testing",
        label="Pruebas Unitarias",
        color="#A78BFA",
        bg_color="rgba(167, 139, 250, 0.15)",
        icon="box",
        animation_class="animate-glow-testing",
    ),
    "deploying": ProjectStatus(
        key="deploying",
        label="En Despliegue",
        color="#0099FF",
        bg_color="rgba(0, 153, 255, 0.15)",
        icon="rocket",
        animation_class="animate-pulse-deploying",
    ),
    "production": ProjectStatus(
        key="production",
        label="En Producción",
        color="#10B981",
        bg_color="rgba(16, 185, 129, 0.15)",
        icon="globe",
        animation_class="",
    ),
    "finalized": ProjectStatus(
        key="finalized",
        label="Finalizado",
        color="#22D3EE",
        bg_color="rgba(34, 211, 238, 0.15)",
        icon="circle-check",
        animation_class="",
    ),
    "paused": ProjectStatus(
        key="paused",
        label="Pausado",
        color="#EF4444",
        bg_color="rgba(239, 68, 68, 0.15)",
        icon="circle-pause",
        animation_class="animate-fade-paused",
    ),
}

# Clave del estado por defecto
DEFAULT_PROJECT_STATUS_KEY = "dev"


def _build_project_status(key: str, payload: object) -> ProjectStatus | None:
    if isinstance(payload, ProjectStatus):
        candidate = payload
    elif isinstance(payload, dict):
        try:
            candidate = ProjectStatus(key=key, **payload)
        except TypeError:
            return None
    else:
        return None

    label = candidate.label.strip()
    color = candidate.color.strip()
    bg_color = candidate.bg_color.strip()
    icon = candidate.icon.strip()
    animation_class = candidate.animation_class.strip()

    if not label or not color or not bg_color or not icon:
        return None

    return ProjectStatus(
        key=key,
        label=label,
        color=color,
        bg_color=bg_color,
        icon=icon,
        animation_class=animation_class,
    )


def resolve_project_status(raw_key: object) -> ProjectStatus:
    default_status = _build_project_status(
        DEFAULT_PROJECT_STATUS_KEY,
        PROJECT_STATUS_CONFIG.get(DEFAULT_PROJECT_STATUS_KEY),
    )
    if default_status is None:
        msg = (
            "Invalid default project status catalog entry: "
            f"{DEFAULT_PROJECT_STATUS_KEY}"
        )
        raise ValueError(msg)

    if not isinstance(raw_key, str):
        return default_status

    normalized_key = raw_key.strip().lower()
    if not normalized_key:
        return default_status

    return (
        _build_project_status(
            normalized_key,
            PROJECT_STATUS_CONFIG.get(normalized_key),
        )
        or default_status
    )
