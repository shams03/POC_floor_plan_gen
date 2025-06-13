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

curr_room_size_global = '1'
ind1 = 0
ind2 = 0
ind3 = 0
ind4 = 0

class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(message: ChatMessage):
    try:
        global curr_room_size_global
        global ind2
        global ind3
        global ind4
        global ind1
        values2 = ['2', '22', '222']
        values3 = ['3', '33', '333']
        values4 = ['4', '44']
        values1 = ['1', '11' , '111']
        print(message.message , "message" , type(message.message))

        if '2' in message.message:
            curr_room_size_global = values2[ind2]
            ind2 += 1
            ind2 = ind2 % len(values2)
        elif '3' in message.message:
            curr_room_size_global = values3[ind3]
            ind3 += 1
            ind3 = ind3 % len(values3)
        elif '4' in message.message:
            curr_room_size_global = values4[ind4]
            ind4 += 1
            ind4 = ind4 % len(values4)
        elif '1' in message.message:
            curr_room_size_global = values1[ind1]
            ind1 += 1
            ind1 = ind1 % len(values1)
        else:
            curr_room_size_global = ''

        print(curr_room_size_global , "curr_room_size_global")
        

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a floor plan generator. When given a natural language description of a house layout, respond only with a JSON object that describes the floor plan. Do NOT add extra explanation. 
                - Every message has the context of the previous messages.
                - Assume the house layout is rectangular and that all rooms will be connected to each other. 
                - Make sure that rooms are placed logically and that the floor plan is complete. 
                - Each room should have dimensions, a position (x, y), doors, and windows. 
                - The format of the response must be like the sample but the room names and values must be as per the user message below:

 {
    "floor_plan": {
        "dimensions": {
            "total_area": 1000,
            "unit": "sq_ft"
        },
        "rooms": [
            {
                "name": "Living Room",
                "width": 300,
                "height": 300,
                "position": {"x": 0, "y": 0},
                "doors": [
                    {"position": "right", "width": 50},
                    {"position": "bottom", "width": 30}
                ]
            },
            {
                "name": "Kitchen",
                "width": 150,
                "height": 150,
                "position": {"x": 300, "y": 0},
                "doors": [
                    {"position": "left", "width": 50}
                ],
                "windows": [
                    {"position": "top", "width": 50}
                ]
            },
            {
                "name": "Bedroom 1",
                "width": 200,
                "height": 200,
                "position": {"x": 0, "y": 300},
                "doors": [
                    {"position": "right", "width": 30}
                ]
            },
            {
                "name": "Bedroom 2",
                "width": 200,
                "height": 200,
                "position": {"x": 200, "y": 300},
                "doors": [
                    {"position": "left", "width": 30}
                ]
            }
        ]
    }
 }
                 
                  - For example if the user message is "I want a house with a kitchen, bedroom, and a bathroom", the response should be like the sample but the room names and context must be as per the user message and no extra rooms should be added.
                 - Design the floor plan in such a way that it is aesthetically pleasing and that the rooms are placed logically.
                 """},
                {"role": "user", "content": message.message}
            ]
        )
        print(response, "OpenAI Response")  # Debug the full response to inspect it.

        # Extract JSON from response
        json_str = response.choices[0].message.content
        floor_plan_data = json.loads(json_str)

        print(floor_plan_data , "floor_plan_data")
        
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
    global curr_room_size_global
    file_path = f"output/floor_plan{curr_room_size_global}.dxf"
    print(file_path , "file_path in api/download")
    # file_path = "output/floor_plan.dxf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=f"floor_plan{curr_room_size_global}.dxf") 

# @app.get("/api/download_mock")
# async def download_file_mock(chat_history:str):
#     file_path = f"output/floor_plan{chat_history}.dxf"
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#     return FileResponse(file_path, filename=f"floor_plan{chat_history}.dxf") 