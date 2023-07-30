# Folge 1: Bilder auf 4x hochskalieren mit DeepAI

import os
import requests
from PIL import Image
import io

# Set your DeepAI API key
api_key = 'DEINE-DeepAI-API-HIER-REIN'

# Set the path to the directory containing the images
image_dir = 'd:/dein Ordner/'

# Go through each image file in the directory
for image_file in os.listdir(image_dir):
    # Check if the file is an image
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Open the image file
        with open(os.path.join(image_dir, image_file), 'rb') as file:
            # Send a request to the DeepAI API
            response = requests.post(
                'https://api.deepai.org/api/torch-srgan',
                files={
                    'image': file,
                },
                headers={
                    'api-key': api_key
                }
            )

            # Check if the request was successful
            if response.status_code == 200:
                # Get the URL of the upscaled image
                output_url = response.json()['output_url']

                # Download the upscaled image
                upscaled_image = requests.get(output_url).content

                # Save the upscaled image
                upscaled_image_file = image_file.rsplit('.', 1)[0] + '_upscaled.png'
                with open(os.path.join(image_dir, upscaled_image_file), 'wb') as file:
                    file.write(upscaled_image)
                    
                # Open the upscaled image with PIL
                upscaled_image = Image.open(io.BytesIO(upscaled_image))

                # Resize the image to 4K
                upscaled_image = upscaled_image.resize((3840, 2160), Image.LANCZOS)

                # Save the 4K image
                upscaled_image_file_4k = image_file.rsplit('.', 1)[0] + '_upscaled_4k.png'
                upscaled_image.save(os.path.join(image_dir, upscaled_image_file_4k))

            else:
                print(f'Error upscaling image {image_file}: {response.text}')
