from fastapi import FastAPI
import uvicorn

# Initialize FastAPI app
app = FastAPI()

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns HTTP 200 when the server is running.
    """
    return {"status": "ok", "message": "PA Bot is running! 🤖"}

def start_health_server():
    """
    Starts the health check server on port 8000.
    """
    print("🏥 Starting health check server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)