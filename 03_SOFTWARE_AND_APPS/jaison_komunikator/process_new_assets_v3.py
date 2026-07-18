import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def unmultiply_alpha(img_path, threshold=20):
    """Load image, remove black background and restore translucent details."""
    print(f"Processing transparency for: {img_path}")
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Calculate brightness
    max_rgb = np.maximum(np.maximum(r, g), b)
    
    # Values below threshold become transparent, above scale up
    new_a = np.where(max_rgb < threshold, 0, max_rgb)
    
    # Avoid division by zero
    div = np.where(new_a == 0, 1, new_a)
    
    # Unmultiply alpha to restore original colors in translucent parts
    new_r = np.clip(r.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    new_g = np.clip(g.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    new_b = np.clip(b.astype(float) * 255.0 / div, 0, 255).astype(np.uint8)
    
    data[:,:,0] = new_r
    data[:,:,1] = new_g
    data[:,:,2] = new_b
    data[:,:,3] = new_a.astype(np.uint8)
    
    out_img = Image.fromarray(data, "RGBA")
    
    # Crop to non-transparent bounding box
    non_zero = np.where(new_a > threshold)
    if len(non_zero[0]) > 0:
        min_y, max_y = np.min(non_zero[0]), np.max(non_zero[0])
        min_x, max_x = np.min(non_zero[1]), np.max(non_zero[1])
        
        padding = 16
        min_y = max(0, min_y - padding)
        max_y = min(height, max_y + padding)
        min_x = max(0, min_x - padding)
        max_x = min(width, max_x + padding)
        
        out_img = out_img.crop((min_x, min_y, max_x, max_y))
        print(f"Cropped to: {out_img.width}x{out_img.height}")
        
    return out_img

def process_logo_clean():
    # Path to our newly generated clean logo
    src_logo = r"C:\Users\tomas_yq1b9su\.gemini\antigravity\brain\f347e78a-eca8-4860-8fc0-59a63af37afe\jaison_service_logo_clean_v4_1783105681200.png"
    dest_logo = r"C:\Aplikacje MVP\Android\web\app_icon_jaison_clean.png"
    
    if not os.path.exists(src_logo):
        print(f"Error: {src_logo} does not exist!")
        return
        
    # Process transparency
    processed_logo = unmultiply_alpha(src_logo, threshold=15)
    
    # Resize to maximum height of 512px for optimization, keeping aspect ratio
    target_height = 512
    target_width = int((target_height / processed_logo.height) * processed_logo.width)
    optimized_logo = processed_logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    os.makedirs(os.path.dirname(dest_logo), exist_ok=True)
    optimized_logo.save(dest_logo, "PNG")
    print(f"Saved optimized clean logo to {dest_logo} ({target_width}x{target_height})")

def make_squircle_mask(size, radius):
    """Create a high-quality squircle mask."""
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return mask

def process_mobile_icon():
    src_icon = r"C:\Users\tomas_yq1b9su\.gemini\antigravity\brain\f347e78a-eca8-4860-8fc0-59a63af37afe\jaison_mobile_icon_v3_1783093107206.png"
    dest_web_square = r"C:\Aplikacje MVP\Android\web\app_icon_square.png"
    
    if not os.path.exists(src_icon):
        print(f"Error: {src_icon} does not exist!")
        return
        
    img = Image.open(src_icon).convert("RGBA")
    
    # The generated image by AI has solid black borders outside the squircle icon.
    # We want to crop to the squircle itself and make everything outside transparent.
    # 1. Let's find the squircle bounding box by checking brightness
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    max_rgb = np.maximum(np.maximum(r, g), b)
    
    # Squircle background is obsidian #080b11, which has max_rgb around 15-20.
    # The pure black outside border is 0.
    non_zero = np.where(max_rgb > 8)
    if len(non_zero[0]) > 0:
        min_y, max_y = np.min(non_zero[0]), np.max(non_zero[0])
        min_x, max_x = np.min(non_zero[1]), np.max(non_zero[1])
        
        # Crop to the active area
        img = img.crop((min_x, min_y, max_x, max_y))
        print(f"Cropped mobile icon to active region: {img.width}x{img.height}")
        
    # Resize to 1024x1024 base
    size = 1024
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Apply a smooth squircle mask to make sure the corners are perfectly transparent
    # A standard squircle at 1024x1024 has radius ~220
    mask = make_squircle_mask(size, radius=220)
    
    # We create a transparent background canvas
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(img, (0, 0), mask=mask)
    
    # Save optimized 512x512 version for web and chatbot
    web_square = canvas.resize((512, 512), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(dest_web_square), exist_ok=True)
    web_square.save(dest_web_square, "PNG")
    print(f"Saved 512x512 web icon to {dest_web_square}")
    
    # Export to Android mipmap folders
    res_dir = r"C:\Aplikacje MVP\Android\client\app\src\main\res"
    mipmaps = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }
    
    for folder, res_size in mipmaps.items():
        android_dest_dir = os.path.join(res_dir, folder)
        os.makedirs(android_dest_dir, exist_ok=True)
        android_dest_file = os.path.join(android_dest_dir, "ic_launcher.png")
        
        # Resize to target size
        android_icon = canvas.resize((res_size, res_size), Image.Resampling.LANCZOS)
        android_icon.save(android_dest_file, "PNG")
        print(f"Exported {res_size}x{res_size} icon to {android_dest_file}")

if __name__ == "__main__":
    print("--- Starting Pack V3 Asset Processing ---")
    process_logo_clean()
    process_mobile_icon()
    print("--- Finished Pack V3 Asset Processing ---")
