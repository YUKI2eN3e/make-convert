import subprocess as sp
import anitopy

anitopy_options = {'allowed_delimiters': ' '}

# Get a list of all the mkv video files
sp.run("dir /b | grep .mkv > videos.txt", shell=True)
with open("videos.txt", "r") as f:
	videos = f.readlines()
f.close()

script = open("convert.bat", "w")
for v in videos:
	vid = v.strip()
	info = anitopy.parse(vid, options=anitopy_options)
	e = info["episode_number"]
	title = info["anime_title"]
	title = title.replace(".", " ")
	output = title + " - " + e + ".mp4"
	sub = vid.replace("[", "\\[")
	sub = sub.replace("]", "\\]")
	sub = sub.replace(",", "\\,")
	script.write("ffmpeg -i \"%s\" -c:v libx265 -vf subtitles=\"%s\" -c:a libfdk_aac \"%s\" & ^ \n" % (vid, sub, output))
script.write("echo Done")
script.close()