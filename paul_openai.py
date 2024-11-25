import comfy.ui as comfy
import requests
import base64

class PaulOpenIA(comfy.Node):
    """
    A custom node for ComfyUI that takes an image, a prompt, and an API key,
    sends the data to OpenAI's API, and returns the response as a string.
    """
    def __init__(self):
        super().__init__(
            inputs={
                "imagen": comfy.ImageInput(),
                "prompt": comfy.StringInput(),
                "api_key": comfy.StringInput()
            },
            outputs={
                "respuesta": comfy.StringOutput()
            }
        )

    def process(self, inputs):
        """
        Sends the image and the prompt to the OpenAI API using the provided API key
        and returns the response.
        """
        # Get the inputs
        imagen = inputs['imagen']
        prompt = inputs['prompt']
        api_key = inputs['api_key']

        if not api_key:
            raise ValueError("API Key is required to use this node.")

        # Convert the image to base64
        image_bytes = imagen.to_bytes()  # Ensure this method correctly retrieves image bytes
        imagen_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Prepare the API request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4-turbo",  # Use gpt-4-turbo for cost and performance optimization
            "messages": [
                {"role": "system", "content": "You are an assistant that analyzes images and answers questions about them."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"data:image/png;base64,{imagen_base64}"}
            ]
        }

        # Send the request to the OpenAI API
        response = requests.post(url, headers=headers, json=data)

        # Handle API errors
        if response.status_code != 200:
            raise RuntimeError(f"OpenAI API Error: {response.status_code} - {response.text}")

        # Parse the response from the API
        respuesta = response.json()['choices'][0]['message']['content']

        # Return the response
        return {"respuesta": respuesta}

# Register the node in ComfyUI
comfy.register_node(
    PaulOpenIA,
    category="Custom Nodes",
    name="Paul OpenIA"
)
