import os
from PIL import Image, ImageDraw, ImageFilter

def create_cyber_launcher_icon():
    logo_path = r"C:\Aplikacje MVP\Android\web\app_icon.png"
    output_path = r"C:\Aplikacje MVP\Android\client\app\src\main\res\mipmap-xxxhdpi\ic_launcher.png"
    
    if not os.path.exists(logo_path):
        print(f"Error: app_icon.png not found at {logo_path}")
        return
        
    print("Loading cropped transparent logo...")
    logo = Image.open(logo_path).convert("RGBA")
    
    # 1. Create a 1024x1024 canvas with transparent background
    size = 1024
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # 2. Draw a premium squircle with obsidian background and cyber neon border
    # We will use a larger canvas for glow blur, then crop/resize, or draw directly
    # A standard squircle can be drawn as a rounded rectangle
    margin = 80
    squircle_box = [margin, margin, size - margin, size - margin]
    radius = 180  # high roundness squircle-like
    
    # Draw glow underneath
    glow_canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_canvas)
    
    # Draw a thicker soft glowing border
    glow_draw.rounded_rectangle(
        squircle_box,
        radius=radius,
        fill=None,
        outline=(0, 240, 255, 120),  # Neon Cyan with opacity
        width=36
    )
    # Blur the glow
    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(radius=24))
    
    # Draw the main squircle background and border
    base_draw = ImageDraw.Draw(canvas)
    # Draw squircle background (obsidian #080b11)
    base_draw.rounded_rectangle(
        squircle_box,
        radius=radius,
        fill=(8, 11, 17, 255),
        outline=None
    )
    
    # Composite the glow behind the background
    squircle_canvas = Image.alpha_composite(glow_canvas, canvas)
    
    # Draw the sharp neon cyan border on top
    border_draw = ImageDraw.Draw(squircle_canvas)
    border_draw.rounded_rectangle(
        squircle_box,
        radius=radius,
        fill=None,
        outline=(0, 240, 255, 255),  # Pure Neon Cyan
        width=12
    )
    
    # 3. Center the J(a)son logo inside the squircle
    # We want the logo to be nicely scaled (e.g., max width/height of 520px inside the 1024x1024 canvas)
    fit_size = 520
    if logo.width > logo.height:
        fit_w = fit_size
        fit_h = int((logo.height / logo.width) * fit_size)
    else:
        fit_h = fit_size
        fit_w = int((logo.width / logo.height) * fit_size)
        
    logo_resized = logo.resize((fit_w, fit_h), Image.Resampling.LANCZOS)
    
    # Center position
    offset_x = (size - fit_w) // 2
    offset_y = (size - fit_h) // 2
    
    # Paste logo on top of squircle canvas
    squircle_canvas.paste(logo_resized, (offset_x, offset_y), logo_resized)
    
    # Save the launcher icon
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    squircle_canvas.save(output_path, "PNG")
    print(f"Success! Saved premium cyber-glowing launcher icon to {output_path}")

if __name__ == "__main__":
    create_cyber_launcher_icon()
