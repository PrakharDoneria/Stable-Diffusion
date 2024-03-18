# Image Generation API

This API allows users to generate images based on prompts using a pre-trained model. It also provides functionality to upload the generated images to an image hosting service.

## Endpoints

### /prompt [POST]

This endpoint accepts a POST request with a prompt in the form data. It generates an image based on the provided prompt and returns the URL of the uploaded image.

#### Request Body

- `prompt`: The prompt for generating the image.

#### Response

- `200 OK`: If the image is successfully generated and uploaded, it returns a JSON object with the URL of the uploaded image.
  ```json
  {
      "image_url": "https://example.com/image.jpg"
  }
  ```

- `400 Bad Request`: If no prompt is provided in the request.
  ```json
  {
      "error": "No prompt provided"
  }
  ```

- `500 Internal Server Error`: If there's an error processing the image or uploading it to the image hosting service.
  ```json
  {
      "error": "Error processing image: <error_message>"
  }
  ```

  ```json
  {
      "error": "Failed to retrieve image"
  }
  ```

  ```json
  {
      "error": "Failed to upload image to imgBB"
  }
  ```

## Example Usage

```bash
curl -X POST -d "prompt=Generate an image of a peaceful countryside with a small cottage surrounded by trees and a clear blue sky." https://api.example.com/prompt