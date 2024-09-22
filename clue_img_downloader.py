from openai import OpenAI
import requests
import os

# Replace with your OpenAI API key
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Function to generate and download images using OpenAI API
def download_images(prompts, num_images=1, save_directory='downloads'):
    os.makedirs(save_directory, exist_ok=True)
    
    for prompt in prompts:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt="a white siamese cat",
                size="1024x1024",
                quality="standard",
                n=num_images,
            )
            
            image_url = response.data[0].url

            # Save each image returned
            for idx, image_data in enumerate(response['data']):
                image_url = image_data['url']
                img_name = f'{prompt.replace(" ", "_")}_{idx+1}.png'  # Filename convention
                img_path = os.path.join(save_directory, img_name)

                # Download image
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f'Downloaded: {img_name}')
                else:
                    print(f'Failed to download image from {image_url}')
        
        except Exception as e:
            print(f'Error creating images for prompt "{prompt}": {e}')

# Example usage
prompts = ['conspiracy theory proofs']
download_images(prompts, num_images=2, save_directory='image_downloads')
