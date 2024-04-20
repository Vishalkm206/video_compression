from flask import Flask, request, jsonify
import subprocess
from flasgger import Swagger, swag_from
from flasgger import Swagger, swag_from

app = Flask(__name__)

template = {
   "swagger":"2.0",
   "info":{
      "title":"Video Compression Api",
      "description":"API for doing Video Compression",
      "contact":{
         "responsibleOrganization":"Lazlo",
         "responsibleDeveloper":"Vishal Kumar Mahato",
         "email":"Vishalkm206@gmail.com",
         "url":"#",
      },
      "termsOfService":"#",
      "version":"1.0"
   },
   "host":"#",
   "basePath":"api",
   "schemes":['http','https'],
   "operationId":"getmeCompressed",
}

swagger= Swagger(app,template=template)
@app.route('/')
def home():
   return 'Home'

def encode_video(input_file, output_file, crf, fps, resolution):
  """
  Encodes a video using ffmpeg with specified parameters.

  Args:
      input_file: Path to the input video file.
      output_file: Path to the output video file.
      crf: CRF value for quality control (lower means better quality).
      fps: Target frame rate for the output video.
      resolution: Desired output resolution as a string (e.g., "854:480").
  """
  command = [
      "ffmpeg", "-i", input_file, "-c:v", "libx265",
      "-crf", str(crf), "-r", str(fps),
      "-vf", f"scale={resolution}", output_file,"-y"
  ]
  try:
      subprocess.run(command, check=True)
      return {"message": "Video encoded successfully!","output_file":output_file}
  except subprocess.CalledProcessError as e:
      return {"error": f"Error encoding video: {e}"}, 500

@app.route("/video_compress", methods=["POST"])
def encode_video_api():
  """API endpoint for video Compression.
    Using this api you can compress your video. you need to pass as json file inside body like :-{"input_file": "Original_video.mp4","output_file": "output_video.mkv","crf": 30,"fps": 30,"resolution": "854:480"}
  ---
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            input_file:
              type: string
              description: Path to the input video file.
            output_file:
              type: string
              description: Path to the output video file.
            crf:
              type: integer
              description: CRF value for quality control (10-51).
              minimum: 10
              maximum: 51
            fps:
              type: integer
              description: Target frame rate for the output video.
              minimum: 1
              maximum: 60
            resolution:
              type: string
              description: Desired output resolution (width:height).
  responses:
    200:
      description: Video Compressed successfully.
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                description: Success message.
    500:
      description: Error encoding video.
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message.
  """
  data = request.get_json()
  if not data:
      return {"error": "Missing JSON data"}, 400

  try:
      input_file = data["input_file"]
      output_file = data["output_file"]
      crf = data["crf"]
      fps = data["fps"]
      resolution = data["resolution"]
  except KeyError as e:
      return {"error": f"Missing key in request data: {e}"}, 400

  # Additional validation (optional)
  # ...

  return encode_video(input_file, output_file, crf, fps, resolution)

if __name__ == "__main__":
  app.run(debug=True)
