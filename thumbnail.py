import subprocess

def thumbnail():
	input_file = "./transcripts/Atom.mp4"
	temp_output = "./output.png"
	command = ["ffmpeg", "-i", input_file, "-ss", "00:00:03.000", "-vframes", "1", temp_output]
	subprocess.check_output(command)
	f = open(temp_output, 'rb')
	f_binary = f.read()
	f.close()
	remove = ["rm", temp_output]
	subprocess.check_output(remove)
	return f_binary
	
print thumbnail()