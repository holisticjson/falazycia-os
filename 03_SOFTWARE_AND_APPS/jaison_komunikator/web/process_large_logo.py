import os
from PIL import Image
import numpy as np

def process_large_logo():
    input_path = r"C:\Aplikacje MVP\Android\web\app jason large.png"
    output_dir = r"C:\Aplikacje MVP\Android\web"
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return
        
    print(f"Loading large logo from {input_path}")
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    print(f"Original size: {width}x{height}")
    
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Compute brightness
    max_rgb = np.maximum(np.maximum(r, g), b)
    
    # Create smooth alpha channel based on brightness to remove black background
    # Since background is very dark (values < 15), we map it to transparent
    # Threshold below 15 becomes transparent, above that scales up
    new_a = np.where(max_rgb < 15, 0, max_rgb)
    
    # Avoid division by zero when unmultiplying alpha
    div = np.where(new_a == 0, 1, new_a)
    
    # Unmultiply alpha to restore original color vividness in translucent areas
    new_r = np.clip(r.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    new_g = np.clip(g.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    new_b = np.clip(b.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    
    data[:,:,0] = new_r
    data[:,:,1] = new_g
    data[:,:,2] = new_b
    data[:,:,3] = new_a.astype(np.uint8)
    
    out_img = Image.fromarray(data, "RGBA")
    
    # Crop the image to non-transparent boundaries to center it and remove empty borders
    non_zero = np.where(new_a > 15)
    if len(non_zero[0]) > 0:
        min_y, max_y = np.min(non_zero[0]), np.max(non_zero[0])
        min_x, max_x = np.min(non_zero[1]), np.max(non_zero[1])
        
        # Add a comfortable padding
        padding = 20
        min_y = max(0, min_y - padding)
        max_y = min(height, max_y + padding)
        min_x = max(0, min_x - padding)
        max_x = min(width, max_x + padding)
        
        out_img = out_img.crop((min_x, min_y, max_x, max_y))
        print(f"Cropped logo bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")
        print(f"New size after crop: {out_img.width}x{out_img.height}")
    
    # Save high-resolution transparent version
    hires_path = os.path.join(output_dir, "app_icon_transparent.png")
    out_img.save(hires_path, "PNG")
    print(f"Saved high-res transparent logo to {hires_path}")
    
    # Create web version (e.g. max height 512px for optimization, keeping aspect ratio)
    web_img = out_img.copy()
    web_height = 512
    web_width = int((web_height / web_img.height) * web_img.width)
    web_img = web_img.resize((web_width, web_height), Image.Resampling.LANCZOS)
    
    web_logo_path = os.path.join(output_dir, "app_icon.png")
    web_img.save(web_logo_path, "PNG")
    print(f"Saved optimized app_icon.png ({web_width}x{web_height}) to {web_logo_path}")
    
    # Create square icon version for Android app and Chatbot (e.g. 512x512 with logo centered)
    square_size = 512
    square_img = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
    
    # Resize cropped logo to fit nicely in 512x512
    fit_size = 420  # leave some padding around the logo in the square icon
    if out_img.width > out_img.height:
        fit_w = fit_size
        fit_h = int((out_img.height / out_img.width) * fit_size)
    else:
        fit_h = fit_size
        fit_w = int((out_img.width / out_img.height) * fit_size)
        
    resized_fit = out_img.resize((fit_w, fit_h), Image.Resampling.LANCZOS)
    
    # Paste centered
    offset_x = (square_size - fit_w) // 2
    offset_y = (square_size - fit_h) // 2
    square_img.paste(resized_fit, (offset_x, offset_y), resized_fit)
    
    square_logo_path = os.path.join(output_dir, "app_icon_square.png")
    square_img.save(square_logo_path, "PNG")
    print(f"Saved 512x512 square logo to {square_logo_path}")

if __name__ == "__main__":
    process_large_logo()
