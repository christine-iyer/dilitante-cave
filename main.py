from fastapi import FastAPI
from routes.students import router as students_router
from routes.instructors import router as instructors_router
from routes.workshops import router as workshops_router
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the students router
app.include_router(students_router)
# Include the instructors router
app.include_router(instructors_router)
# Include the workshops router     
app.include_router(workshops_router)