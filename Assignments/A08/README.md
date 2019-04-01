Instructions
- Open emoji zip file, and place folder in directory.
- Run "python3 process_emojis.py folder=emojis" in the command line.
- Run  "python3 mosaic.py image=hurricane.png input_folder=emojis size=4 output_folder=output" in the command line.
- You can increase the chunk size to speed up the process, but it will reduce the quality of the image.
- The chunk size defaults at 4, provides good quality, and runs in around an hour on my computer.
