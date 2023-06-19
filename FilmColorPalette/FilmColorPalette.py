import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from PIL import Image
import sys
import os

def get_main_colors_k(image, num_colors):
    try:
        # Reshape the image into a list of pixels
        reshaped = image.reshape(-1, 3)

        # Remove pixels with too low or too high grayscale values
        reshaped = reshaped[(reshaped.mean(axis=1) > 10) & (reshaped.mean(axis=1) < 245)]

        # Use KMeans to find the most dominant colors
        # kmeans = KMeans(n_clusters=num_colors).fit(reshaped)
        kmeans = MiniBatchKMeans(n_clusters=num_colors, batch_size=3072).fit(reshaped)

        # Return the colors
        return kmeans.cluster_centers_
    except ValueError:
        # If not enough unique colors are found, return None
        return None

def generate_image(colors):
    # Define the height and width of the color blocks
    height = 4
    width = 720
    
    # Initialize a blank image
    bar = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Calculate the width of each color block
    color_width = width // len(colors)

    # Fill in the color blocks
    for idx, color in enumerate(colors):
        start = idx * color_width
        end = start + color_width
        bar[:, start:end] = color

    # Return the image of color blocks
    return bar

def main(video_path, num_colors):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Calculate the total length of the video (in seconds)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    
    # Calculate the interval time
    interval = video_length / 600
    
    # Convert the interval time to number of frames
    interval_frames = int(cap.get(cv2.CAP_PROP_FPS) * interval)
    
    # Calculate the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the number of frames that need to be processed
    total_captures = total_frames // interval_frames
    
    images = []
    frame_num = 0
    capture_num = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        # If it's an interval frame, process this frame
        if frame_num % interval_frames == 0:
            # Get the dominant colors
            colors = get_main_colors_k(frame, num_colors)
            
            # If not enough colors are found, skip this frame
            if colors is None:
                frame_num += 1
                continue

            # Sort the colors by color value
            colors = colors[np.argsort(colors.sum(axis=1))]
            
            # Generate an image of color blocks and add it to the list
            images.append(generate_image(colors))
            
            # Update the number of processed frames
            capture_num += 1
            
            # Calculate and display the progress
            progress = capture_num / total_captures * 100
            print(f'{capture_num}/{total_captures} Finished  |  Progress: {progress:.2f}%')

            # Vertically concatenate all images of color blocks
            image = np.concatenate(images, axis=0)
    
            # Convert the image to PIL format and save
            # Note: OpenCV uses the BGR color space, while PIL assumes the input is in the RGB color space.
            # Therefore, here we directly convert the BGR image from OpenCV to a PIL image, without performing a color space conversion.
            # This means that PIL will mistakenly interpret the BGR image as an RGB image, but in this particular case, the result looks correct.
            image = Image.fromarray(image.astype('uint8')).convert('RGB')
            
            # Convert the PIL image to OpenCV format
            # Note: Here we assume the PIL image is in the RGB color space, so the converted OpenCV image will be in the BGR color space.
            image = np.array(image)
            
            # Add a white border to the image
            # Note: OpenCV uses the BGR color space, so the white color here is white in the BGR color space.
            image = cv2.copyMakeBorder(image, 80, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])

            # Add the filename in the white border at the top
            filename = os.path.basename(video_path)
            cv2.putText(image, filename, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_8)
            
            # Save the image with the border
            # Note: OpenCV uses the BGR color space, so the image saved here will be in the BGR color space.
            cv2.imwrite(f'{video_path}_colorBar.png', image)

        frame_num += 1

    # Release the video file
    cap.release()

if __name__ == '__main__':
    # Check the command line arguments
    if len(sys.argv) != 3:
        print('Usage: python script.py <video_path> <num_colors>')
        sys.exit(1)

    # Parse the command line arguments
    video_path = sys.argv[1]
    num_colors = int(sys.argv[2])

    # Run the main function
    main(video_path, num_colors)
