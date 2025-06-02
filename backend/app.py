from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import openai
import json
import os
from dxf_generator import json_to_dxf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(message: ChatMessage):
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a floor plan generator. When given a natural language description of a house layout, respond only with a JSON object describing the floor plan. Do NOT add extra explanation."},
                {"role": "user", "content": message.message}
            ]
        )
        
        # Extract JSON from response
        json_str = response.choices[0].message.content
        floor_plan_data = json.loads(json_str)
        
        # Save JSON file
        os.makedirs("output", exist_ok=True)
        json_path = "output/floor_plan.json"
        with open(json_path, "w") as f:
            json.dump(floor_plan_data, f, indent=2)
        
        # Generate DXF file
        dxf_path = "output/floor_plan.dxf"
        json_to_dxf(floor_plan_data, dxf_path)
        
        # Return both the JSON data and success message
        return JSONResponse({
            "status": "success",
            "message": "Floor plan generated successfully",
            "data": floor_plan_data
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download")
async def download_file():
    file_path = "output/floor_plan.dxf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename="floor_plan.dxf") 