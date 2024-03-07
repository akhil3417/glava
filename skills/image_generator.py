import requests
from urllib.parse import quote


def generate_image(user_input):
    """
    Make a request to the pollinations.ai and save the response as a .jpg file.

    Parameters:
    user_input (str): The user input to be formatted and used to construct the URL.

    Returns:
    None
    """
    # Format the user input
    formatted_input = quote(user_input)

    # Construct the URL
    url = f"https://image.pollinations.ai/prompt/{formatted_input}"

    print(f"Making request to: {url}")

    # Make the request
    response = requests.get(url)

    # Create a dynamic filename
    filename = "-".join(user_input.split()[:4]) + ".jpg"

    print(f"Saving response to: {filename}")

    # Save the response as a .jpg file
    with open(filename, "wb") as f:
        f.write(response.content)

    print("Response saved successfully.")
