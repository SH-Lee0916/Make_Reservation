import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Middle wares
from fastapi.middleware.cors import CORSMiddleware  # For CORS
from middlewares.logger import MiddleLogger # For logging

def create_app() -> FastAPI:
    """ Create FastAPI app
    Return:
        FastAPI app
    """

    app = FastAPI()
    
    # logging middleware
    app.add_middleware(MiddleLogger,
                       logger = logging.getLogger(__name__))
    
    # CORS middleware
    origins = [ "http://localhost:3000" ]
    app.add_middleware(CORSMiddleware,
                       allow_origins = origins,
                       allow_credentials = True,
                       allow_methods = ["*"],
                       allow_headers = ["*"])

    @app.get("/")
    def test_page():
        return JSONResponse({"test_page": "Hello FastAPI"})

    return app

app = create_app()

if __name__ == "__main__":

    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True)