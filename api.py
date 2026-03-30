from fastapi import FastAPI, UploadFile, File
import shutil
import os
from identify import faceDetection, faceRecognition, setKnownName, setFacesToZero, getKnownName

app = FastAPI(title="Face Recognition API")

@app.post("/recognize")
async def recognize_faces(file: UploadFile = File(...)):
    """
    Upload an image to detect and recognize faces.
    Returns the total count of faces and the names of recognized individuals.
    """
    # Create temp directory if not exists
    os.makedirs("./temp", exist_ok=True)
    temp_path = f"./temp/{file.filename}"
    
    # Save uploaded file temporarily
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Reset global state in identify.py before processing
        setKnownName()
        setFacesToZero()
        
        # Run detection and recognition
        total_faces = faceDetection(temp_path)
        names = faceRecognition(temp_path)
        
        return {
            "total_faces": total_faces,
            "recognized_names": names,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    # To run: python api.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
