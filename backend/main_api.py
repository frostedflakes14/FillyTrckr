from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)