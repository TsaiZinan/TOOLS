import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(image_path, n_colors):
    # Open the image
    image = Image.open(image_path)
    # Convert the image to a numpy array
    image_np = np.array(image)

    # Reshape the array to two dimensions (number of pixels, number of color channels)
    pixels = image_np.reshape(-1, 3)

    # Use the K-means algorithm to find the most common colors
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(pixels)

    # Get the color blocks
    colors = kmeans.cluster_centers_
    
    # The colors need to be integers, so we convert them to integers
    colors = colors.round(0).astype(int)
    
    return colors

def create_image_with_colors(image_path, colors):
    # Open the original image
    original_image = Image.open(image_path)
    
    # Create color blocks and color codes
    color_blocks = [Image.new('RGB', (original_image.width // 5, original_image.width // 5), tuple(color)) for color in colors]
    color_codes = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in colors]
    
    # Create a new image, the height is the height of the original image plus the height of the color block, and the width is the width of the original image
    new_image = Image.new('RGB', (original_image.width, original_image.height + original_image.width // 5 + original_image.width // 20))
    
    # Paste the original image on the new image
    new_image.paste(original_image, (0, 0))
    
    # Paste the color blocks
    for i, (color_block, color_code) in enumerate(zip(color_blocks, color_codes)):
        # Create a white color block
        white_block = Image.new('RGB', (original_image.width // 5, original_image.width // 20), (255, 255, 255))
        
        # Create an ImageDraw object and draw the color code on the white color block
        draw = ImageDraw.Draw(white_block)

        # Gradually increase the font size in a loop until the width of the text is about half the width of the white color block
        font_size = 1
        text_width, text_height = 0, 0
        while text_width < white_block.width // 2:
            font = ImageFont.truetype('arial', font_size)
            text_width, text_height = draw.textsize(color_code, font=font)
            font_size += 1
            
        draw.text(((white_block.width - text_width) / 2, (white_block.height - text_height) / 2), color_code, fill='black', font=font)
        
        # Paste the white color block and color block on the new image
        new_image.paste(white_block, (i * (original_image.width // 5), original_image.height))
        new_image.paste(color_block, (i * (original_image.width // 5), original_image.height + white_block.height))
        
    return new_image

def main(image_path=None):
    if image_path is None:
        print("Please enter the image path")
        return
    
    n_colors = 5
    colors = extract_colors(image_path, n_colors)  # Extract 5 main colors
    new_image = create_image_with_colors(image_path, colors)  # Create new image
    
   # Base name of the original image file, including extension
    base_name = os.path.basename(image_path)  
    # Split the base name into file name and extension
    file_name, ext = os.path.splitext(base_name)  
    # Append "_colorCode" to the file name to create new file name
    new_file_name = f"{file_name}_colorCode{ext}"  
    
    new_image.save(new_file_name)  # Save the new image

if __name__ == "__main__":
    # sys.argv is a list containing command line parameters
    # sys.argv[0] is the script name, sys.argv[1] is the first argument, and so on
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
