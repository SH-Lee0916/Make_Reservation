import uvicorn
from fastapi import FastAPI

# Middle wares
from fastapi.middleware.cors import CORSMiddleware  # For CORS
from middlewares.logger import MiddleLogger, create_logger # For logging

def create_app() -> FastAPI:
    """ Create FastAPI app
    Return:
        FastAPI app
    """

    app = FastAPI()
    
    # Logging middleware
    app.add_middleware(MiddleLogger)
    
    # CORS middlewarea
    origins = [ "http://localhost:3000" ]
    app.add_middleware(CORSMiddleware,
                       allow_origins = origins,
                       allow_credentials = True,
                       allow_methods = ["*"],
                       allow_headers = ["*"])

    return app

app = create_app()

if __name__ == "__main__":

    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True)