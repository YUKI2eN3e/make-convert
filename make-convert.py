import subprocess as sp
import anitopy

anitopy_options = {'allowed_delimiters': ' '}

# Get a list of all the mkv video files
'''
dir_grep = sp.run("dir /b | grep .mkv", stdout=sp.PIPE, shell=True, universal_newlines=True)
videos = dir_grep.stdout.strip().split('\n')
'''
dir = sp.run("dir /b", stdout=sp.PIPE, shell=True, universal_newlines=True)
videos = dir.stdout.strip().split('\n')
#print(videos)
videos = [v for v in videos if ".mkv" in v]
#print(videos)

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