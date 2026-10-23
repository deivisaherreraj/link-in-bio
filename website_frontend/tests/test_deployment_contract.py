import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = REPOSITORY_ROOT / "website_frontend" / "Dockerfile"
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "deploy-railway.yml"
UV_VERSION = "0.10.12"


def test_dockerfile_uses_the_locked_uv_deployment_contract() -> None:
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")

    assert re.search(r"^FROM python:3\.12(?:\s|$)", dockerfile, re.MULTILINE)
    assert f"COPY --from=ghcr.io/astral-sh/uv:{UV_VERSION} " in dockerfile
    assert "COPY pyproject.toml uv.lock ./" in dockerfile
    assert "RUN uv sync --locked --no-dev --no-install-project" in dockerfile
    assert not (REPOSITORY_ROOT / "website_frontend" / "requirements.txt").exists()


def test_railway_workflow_validates_before_deployment() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "uses: astral-sh/setup-uv@v3" in workflow
    assert f'version: "{UV_VERSION}"' in workflow
    assert "run: uv sync --locked --dev" in workflow

    for command in (
        "uv run ruff format --check .",
        "uv run ruff check .",
        "uv run mypy",
        "uv run --locked pytest",
    ):
        assert command in workflow

    assert "run: railway up --service=$RAILWAY_SERVICE_ID" in workflow
