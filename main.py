from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ball tracker AI is running"}

# نقطة بداية رفع الفيديو (تطوير لاحق)
@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    # مبدئياً فقط يعيد اسم الملف
    return {"filename": file.filename}
