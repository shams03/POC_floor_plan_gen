
import ezdxf
import json

def json_to_dxf(json_data, output_path):
    # Create a new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Add layers for different elements
    doc.layers.new(name='ROOMS', dxfattribs={'color': 1})  # Red color for rooms
    doc.layers.new(name='TEXT', dxfattribs={'color': 2})   # Yellow color for text
    doc.layers.new(name='WALLS', dxfattribs={'color': 7})  # Walls (default color)

    # Process each room
    for room in json_data['floor_plan']['rooms']:
        name = room['name']
        width = room['width']
        height = room['height']
        position = room['position']
        
        # Room's bottom-left corner
        x_offset = position['x']
        y_offset = position['y']

        # Define the four corners of the room
        points = [
            (x_offset, y_offset),  # Bottom-left
            (x_offset + width, y_offset),  # Bottom-right
            (x_offset + width, y_offset + height),  # Top-right
            (x_offset, y_offset + height)  # Top-left
        ]

        # Add a polyline for the room (rectangle)
        msp.add_lwpolyline(points, dxfattribs={'layer': 'ROOMS', 'closed': True})

        # Add text for the room name in the center
        center_x = x_offset + width / 2
        center_y = y_offset + height / 2
        
        msp.add_text(
            name,
            dxfattribs={
                'layer': 'TEXT',
                'height': 10,  # Text height
                'style': 'Standard',
                'insert': (center_x, center_y)  # Position in the center
            }
        )

        # Optionally, add walls or doors here if you want them
        # You can add additional layers for doors, windows, etc.

    # Save the DXF file
    doc.saveas(output_path)
    return output_path 


# Example floor plan JSON data (with 2BHK house layout)
json_data = {
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
                "position": {"x": 0, "y": 0}
            },
            {
                "name": "Kitchen",
                "width": 150,
                "height": 150,
                "position": {"x": 300, "y": 0}
            },
            {
                "name": "Bedroom 1",
                "width": 200,
                "height": 200,
                "position": {"x": 0, "y": 300}
            },
            {
                "name": "Bedroom 2",
                "width": 200,
                "height": 200,
                "position": {"x": 200, "y": 300}
            }
        ]
    }
}

# Define output path for the DXF file
output_path = "floor_plan.dxf"

# Convert JSON to DXF
result = json_to_dxf(json_data, output_path)

print(f"DXF file saved at: {result}")
