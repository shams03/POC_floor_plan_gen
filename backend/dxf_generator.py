import ezdxf
import json

def json_to_dxf(json_data, output_path):
    # Create a new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Add layers for different elements
    doc.layers.new(name='ROOMS', dxfattribs={'color': 1, 'linetype': 'Continuous'})  # Red color for rooms
    doc.layers.new(name='TEXT', dxfattribs={'color': 2})   # Yellow color for text
    doc.layers.new(name='WALLS', dxfattribs={'color': 7, 'linetype': 'Continuous'})  # Walls (default color)
    doc.layers.new(name='DOORS', dxfattribs={'color': 5, 'linetype': 'Continuous'})  # Blue color for doors
    doc.layers.new(name='WINDOWS', dxfattribs={'color': 6, 'linetype': 'Continuous'})  # Green color for windows

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
        msp.add_lwpolyline(points, dxfattribs={'layer': 'ROOMS', 'closed': True, 'lineweight': 2})

        # Add text for the room name in the center
        center_x = x_offset + width / 2
        center_y = y_offset + height / 2
        
        # Correcting the text insertion by manually positioning it at the center
        msp.add_text(
            name,
            dxfattribs={
                'layer': 'TEXT',
                'height': 20,  # Text height increased for better visibility
                'style': 'Standard',
                'insert': (center_x, center_y)  # Position text in the center
            }
        )

        # Draw doors for the room (every room should have a door)
        if 'doors' in room:
            for door in room['doors']:
                door_position = door['position']
                door_width = door['width']

                if door_position == 'top':
                    door_x = x_offset + width / 2 - door_width / 2
                    door_y = y_offset + height
                    msp.add_line((door_x, door_y), (door_x + door_width, door_y), dxfattribs={'layer': 'DOORS', 'lineweight': 2})
                
                elif door_position == 'bottom':
                    door_x = x_offset + width / 2 - door_width / 2
                    door_y = y_offset
                    msp.add_line((door_x, door_y), (door_x + door_width, door_y), dxfattribs={'layer': 'DOORS', 'lineweight': 2})
                
                elif door_position == 'left':
                    door_x = x_offset
                    door_y = y_offset + height / 2 - door_width / 2
                    msp.add_line((door_x, door_y), (door_x, door_y + door_width), dxfattribs={'layer': 'DOORS', 'lineweight': 2})
                
                elif door_position == 'right':
                    door_x = x_offset + width
                    door_y = y_offset + height / 2 - door_width / 2
                    msp.add_line((door_x, door_y), (door_x, door_y + door_width), dxfattribs={'layer': 'DOORS', 'lineweight': 2})

        # Draw windows for the room (windows are smaller and placed on one of the walls)
        if 'windows' in room:
            for window in room['windows']:
                window_position = window['position']
                window_width = window['width']

                if window_position == 'top':
                    window_x = x_offset + width / 2 - window_width / 2
                    window_y = y_offset + height
                    msp.add_line((window_x, window_y), (window_x + window_width, window_y), dxfattribs={'layer': 'WINDOWS', 'lineweight': 1})
                
                elif window_position == 'bottom':
                    window_x = x_offset + width / 2 - window_width / 2
                    window_y = y_offset
                    msp.add_line((window_x, window_y), (window_x + window_width, window_y), dxfattribs={'layer': 'WINDOWS', 'lineweight': 1})
                
                elif window_position == 'left':
                    window_x = x_offset
                    window_y = y_offset + height / 2 - window_width / 2
                    msp.add_line((window_x, window_y), (window_x, window_y + window_width), dxfattribs={'layer': 'WINDOWS', 'lineweight': 1})
                
                elif window_position == 'right':
                    window_x = x_offset + width
                    window_y = y_offset + height / 2 - window_width / 2
                    msp.add_line((window_x, window_y), (window_x, window_y + window_width), dxfattribs={'layer': 'WINDOWS', 'lineweight': 1})

        # Optional: Add corridors if defined in the JSON
        if name == "Corridor":
            corridor_x = x_offset
            corridor_y = y_offset
            corridor_width = width
            corridor_height = height
            corridor_points = [
                (corridor_x, corridor_y),  
                (corridor_x + corridor_width, corridor_y),
                (corridor_x + corridor_width, corridor_y + corridor_height),
                (corridor_x, corridor_y + corridor_height)
            ]
            msp.add_lwpolyline(corridor_points, dxfattribs={'layer': 'ROOMS', 'closed': True, 'lineweight': 2})

    # Save the DXF file
    doc.saveas(output_path)
    return output_path 


# Example floor plan JSON data (with advanced features like doors, windows, and corridors)
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
                "position": {"x": 0, "y": 0},
                "doors": [
                    {"position": "right", "width": 50},   # Door on the right wall
                    {"position": "bottom", "width": 30}   # Door on the bottom wall
                ]
            },
            {
                "name": "Kitchen",
                "width": 150,
                "height": 150,
                "position": {"x": 300, "y": 0},
                "doors": [
                    {"position": "left", "width": 50}    # Door on the left wall
                ],
                "windows": [
                    {"position": "top", "width": 50}     # Window on the top wall
                ]
            },
            {
                "name": "Bedroom 1",
                "width": 200,
                "height": 200,
                "position": {"x": 0, "y": 300},
                "doors": [
                    {"position": "right", "width": 30}   # Door on the right wall
                ]
            },
            {
                "name": "Bedroom 2",
                "width": 200,
                "height": 200,
                "position": {"x": 200, "y": 300},
                "doors": [
                    {"position": "left", "width": 30}    # Door on the left wall
                ]
            },
            {
                "name": "Corridor",
                "width": 50,
                "height": 300,
                "position": {"x": 150, "y": 0}
            }
        ]
    }
}

# Define output path for the DXF file
output_path = "floor_plan_with_feature.dxf"

# Convert JSON to DXF
result = json_to_dxf(json_data, output_path)

print(f"DXF file saved at: {result}")


#----------------------------------------------------------------------------------------
# import ezdxf
# import json

# def json_to_dxf(json_data, output_path):
#     # Create a new DXF document
#     doc = ezdxf.new('R2010')
#     msp = doc.modelspace()

#     # Add layers for different elements
#     doc.layers.new(name='ROOMS', dxfattribs={'color': 1})  # Red color for rooms
#     doc.layers.new(name='TEXT', dxfattribs={'color': 2})   # Yellow color for text
#     doc.layers.new(name='WALLS', dxfattribs={'color': 7})  # Walls (default color)

#     # Process each room
#     for room in json_data['floor_plan']['rooms']:
#         name = room['name']
#         width = room['width']
#         height = room['height']
#         position = room['position']
        
#         # Room's bottom-left corner
#         x_offset = position['x']
#         y_offset = position['y']

#         # Define the four corners of the room
#         points = [
#             (x_offset, y_offset),  # Bottom-left
#             (x_offset + width, y_offset),  # Bottom-right
#             (x_offset + width, y_offset + height),  # Top-right
#             (x_offset, y_offset + height)  # Top-left
#         ]

#         # Add a polyline for the room (rectangle)
#         msp.add_lwpolyline(points, dxfattribs={'layer': 'ROOMS', 'closed': True})

#         # Add text for the room name in the center
#         center_x = x_offset + width / 2
#         center_y = y_offset + height / 2
        
#         msp.add_text(
#             name,
#             dxfattribs={
#                 'layer': 'TEXT',
#                 'height': 10,  # Text height
#                 'style': 'Standard',
#                 'insert': (center_x, center_y)  # Position in the center
#             }
#         )

#         # Optionally, add walls or doors here if you want them
#         # You can add additional layers for doors, windows, etc.

#     # Save the DXF file
#     doc.saveas(output_path)
#     return output_path 


# # Example floor plan JSON data (with 2BHK house layout)
# json_data = {
#     "floor_plan": {
#         "dimensions": {
#             "total_area": 1000,
#             "unit": "sq_ft"
#         },
#         "rooms": [
#             {
#                 "name": "Living Room",
#                 "width": 300,
#                 "height": 300,
#                 "position": {"x": 0, "y": 0}
#             },
#             {
#                 "name": "Kitchen",
#                 "width": 150,
#                 "height": 150,
#                 "position": {"x": 300, "y": 0}
#             },
#             {
#                 "name": "Bedroom 1",
#                 "width": 200,
#                 "height": 200,
#                 "position": {"x": 0, "y": 300}
#             },
#             {
#                 "name": "Bedroom 2",
#                 "width": 200,
#                 "height": 200,
#                 "position": {"x": 200, "y": 300}
#             }
#         ]
#     }
# }

# # Define output path for the DXF file
# output_path = "floor_plan.dxf"

# # Convert JSON to DXF
# result = json_to_dxf(json_data, output_path)

# print(f"DXF file saved at: {result}")
