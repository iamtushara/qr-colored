"""Interface for Rest API"""

import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from qr_colored import VERSION
from qr_colored.settings import Settings


LOGGER = logging.getLogger()


def start_app() -> FastAPI:
    """Returns REST Application"""

    LOGGER.info("Starting FastApi")
    app = FastAPI(
        title="qr_colored".upper(),
        description="Data Science Engine | qr_colored",
        version=VERSION,
    )

    # TODO: add more endpoints here

    @app.get("/")
    def redirect_to_documentation():
        """Redirects to /docs for easier navigation"""
        return RedirectResponse("/docs")

    return app


def start_rest_api(settings: Settings) -> None:
    """Starts Uvicorn Server"""

    LOGGER.info("Starting Uvicorn")
    uvicorn.run(
        "qr_colored.rest:start_app",
        host=settings.rest.host,
        port=settings.rest.port,
        log_level=settings.log.level,
        # log_config=settings.logging,
        reload=settings.rest.server_reload,
        factory=True,
    )
