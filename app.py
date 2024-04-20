import streamlit as st
import subprocess

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
      "-vf", f"scale={resolution}", output_file, "-y"
  ]
  try:
      subprocess.run(command, check=True)
      st.success("Video encoded successfully!")
  except subprocess.CalledProcessError as e:
      st.error(f"Error encoding video: {e}")

st.title("Video Compressor using H.265")

# Input file upload
uploaded_file = st.file_uploader("Choose a video file to encode:", type=['mp4', 'avi', 'mov'])

# Encoding parameters
col1, col2, col3 = st.columns(3)
crf_value = col1.number_input("CRF Value (Quality)", min_value=10, max_value=51, value=23, step=1)
target_fps = col2.number_input("Target Frame Rate (fps)", min_value=1, max_value=60, value=30, step=1)
resolution = col3.text_input("Output Resolution (width:height)", value="854:480")

# Encode button and processing indicator
if uploaded_file is not None:
  if st.button("Encode Video"):
    with st.spinner("Encoding video..."):
      encode_video(uploaded_file.name, "encoded_video.mkv", crf_value, target_fps, resolution)

