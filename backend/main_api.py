from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

common_path = Path(__file__).parent.parent / "common"
sys.path.insert(0, str(common_path))
from config import filly_trkr_config
from common_logging import get_logger

logger = get_logger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/filly/get_version")
async def get_version():
    return {"version": "1.0"}

def main():
    """Main entry point to run the FastAPI application."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()