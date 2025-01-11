import os
import plistlib
from PIL import Image

# Paths
SPRITE_SHEET_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Geometry Dash/Resources/GJ_GameSheet-hd.png"  # Path to your sprite sheet
PLIST_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Geometry Dash/Resources/GJ_GameSheet-hd.plist"       # Path to your .plist file
OUTPUT_FOLDER = "extracted_sprites"   # Folder to save extracted sprites

# Ensure the output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the sprite sheet
sprite_sheet = Image.open(SPRITE_SHEET_PATH)

# Load the plist data
with open(PLIST_PATH, 'rb') as plist_file:
    plist_data = plistlib.load(plist_file)

# Iterate over sprites in the plist
for sprite_name, sprite_info in plist_data.get("frames", {}).items():
    # Extract textureRect
    texture_rect_raw = sprite_info.get("textureRect")
    if not texture_rect_raw:
        print(f"Skipping {sprite_name}: Missing textureRect.")
        continue
    
    # Parse textureRect: {{x, y}, {width, height}}
    texture_rect_raw = texture_rect_raw.strip("{}")
    parts = texture_rect_raw.split("},{")
    position = tuple(map(int, parts[0].strip("{}").split(",")))
    size = tuple(map(int, parts[1].strip("{}").split(",")))
    x, y = position
    width, height = size
    
    # Crop the sprite
    texture_rect = (x, y, x + width, y + height)
    sprite = sprite_sheet.crop(texture_rect)
    
    # Save the sprite
    output_path = os.path.join(OUTPUT_FOLDER, sprite_name)
    sprite.save(output_path)
    print(f"Extracted and saved: {sprite_name}")

print(f"All sprites have been extracted to: {OUTPUT_FOLDER}")
