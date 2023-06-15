import re
import time
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientRateLimitError

# Get the API keys from Imgur
client_id = 'Your Client ID'
client_secret = 'Your Client Secret'

# Create an Imgur client
client = ImgurClient(client_id, client_secret)

# Read the Markdown file
with open('new_markdown_file.md', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# First, calculate the total number of images
total_images = sum('![' in line for line in lines)

# Read the last progress
try:
    with open('progress.txt', 'r') as file:
        last_progress = int(file.readline())
except (FileNotFoundError, ValueError):
    last_progress = 0

# Number of images already processed, starting from the last progress
processed_images = sum('![' in line for line in lines[:last_progress])

# Traverse each line, starting from the last progress
for i, line in enumerate(lines, start=1):
    # If the current line number is less than or equal to the last progress, skip it
    if i <= last_progress:
        continue

    # Check if this line contains an image link
    match = re.search(r'!\[\]\((.*)\)', line)
    if match:
        # Extract the image link
        url = match.group(1)

        try:
            # Upload the image from the URL to Imgur
            response = client.upload_from_url(url, config=None, anon=True)

            # Get the new Imgur link
            new_url = response['link']

            # Replace the original link
            new_line = line.replace(url, new_url)

            # Update this line
            lines[i - 1] = new_line

            # The image conversion is complete, increase the number of processed images
            processed_images += 1

            # Print the completed information and progress
            print(f"Image {processed_images}/{total_images} converted, progress: {processed_images / total_images * 100:.2f}%")

            # Save after each image is processed
            with open('new_markdown_file.md', 'w', encoding='utf-8') as file:
                file.writelines(lines)
            with open('progress.txt', 'w') as file:
                file.write(str(i))

            # Wait for 8 seconds to avoid triggering Imgur's rate limit
            time.sleep(8)
        except ImgurClientRateLimitError:
            print("Rate-limit exceeded! Please change your IP to avoid the upload limit.")
            break
    # Print the number of processed lines
    print(f"Processed lines: {i}")

# Save the new Markdown file
with open('new_markdown_file.md', 'w', encoding='utf-8') as file:
    file.writelines(lines)
