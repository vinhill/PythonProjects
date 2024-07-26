from openai import OpenAI
from env import OPENAI_API_KEY

SIMULATE = False

if __name__ == "__main__":
    if not SIMULATE:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        client = None

    response = client.images.generate(
        model="dall-e-2",
        prompt=input("prompt: "),
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print(image_url)