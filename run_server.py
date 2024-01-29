import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from chain_logic import get_chain

logging.basicConfig(format='[%(levelname)s] :%(message)s',
                    level=logging.DEBUG if os.getenv('VERBOSE') == "True" else logging.INFO)

# Load settings from the .env file
load_dotenv()

if __name__ == '__main__':
    chain = get_chain(
        document_path=os.getenv("DOCUMENT_PATH", "./raw-documents"),
        model_name=os.getenv("MODEL", "mistral"),
        model_url=os.getenv("MODEL_URL", "http://localhost:11434"),
        max_depth=int(os.getenv("MAX_DEPTH", "2")),
        start_legislation=os.getenv("START_LEGISLATION", "CELEX:32020R0852"),
        metadata_path=os.getenv("METADATA", "crawled_data.json"),
        html_dir=os.getenv("DOCUMENT_PATH", "./raw-documents"),
        fixed_document_path=os.getenv("FIXED_DOCUMENT_PATH", "./fixed-documents")
    )

    app = FastAPI(
        title="LegalLLM API",
        version="1.0",
        description="API for LegalLLM.",
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    add_routes(
        app,
        chain,
        path="/legal",
    )

    uvicorn.run(app, host="localhost", port=8000)