from fastapi import FastAPI
from models.create_students import router as students_router

app = FastAPI()

# Include the students router
app.include_router(students_router)