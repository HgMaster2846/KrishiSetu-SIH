import uvicorn

if __name__ == "__main__":
    print("================================================================")
    print("?? KrishiSetu AI Backend Server Starting...")
    print("?? AI Voice Hotline Number: 1800-260-3300")
    print("?? API Swagger Documentation: http://localhost:8000/docs")
    print("?? Web Demo & Phone Simulator: http://localhost:8000")
    print("================================================================")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
