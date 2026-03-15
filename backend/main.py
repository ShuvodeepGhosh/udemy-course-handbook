from fastapi import FastAPI

app = FastAPI(
    title="Course Handbook AI",
    description="Generate structured handbooks from course transcripts",
    version="1.0"
)

@app.get("/")
def health_check():
    return {"status": "running"}