import praw
import pandas as pd
import csv
from googletrans import Translator
from gtts import gTTS
import os
from moviepy import editor
from mutagen.mp3 import MP3
from PIL import Image
from pathlib import Path

reddit = praw.Reddit(client_id='THEID', client_secret='THESECRET', user_agent='THEUSERAGENT')
posts = []
l_subreddit = reddit.subreddit('redditdev')
for post in l_subreddit.new(limit=10):
    posts.append([post.title, post.selftext])
posts = pd.DataFrame(posts,columns=['', ''])
print(posts)

posts.to_csv(rf'path\YoutubeAutomator\posts.csv')


csv_file = ('posts.csv')
txt_file = ('posts.txt')
with open(txt_file, "w", encoding='utf-8') as my_output_file:
    with open(csv_file, "r", encoding='utf-8') as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()


f = open('posts.txt', 'r')

if f.mode == 'r':
    contents = f.read()
    print(contents)

translator = Translator()
result = translator.translate(contents, src='en', dest='es')
print(result.text)

with open('spanish.txt', 'w', encoding='utf-8') as f:
     f.write(result.text)

fh = open('spanish.txt','r')
mytext = fh.read() 
language= 'es'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")

song = MP3('welcome.mp3')

length = song.info.length
path_images = Path('')
images = list(path_images.glob('*.jpg'))
image_list = list()

for image_name in images:
    image =Image.open(image_name).resize((1920,1080), Image.ANTIALIAS)
    image_list.append(image)

image_list[0].save('temp.gif',save_all=True, append_images = image_list[1:], duration = length)

video = editor.VideoFileClip('temp.gif')
audio = editor.AudioFileClip('welcome.mp3')
final_video = video.set_audio(audio)
final_video.write_videofile('test.mp4', fps=60)
