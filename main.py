

# audio captcha generator

import pyfiglet
import termcolor
import playsound

print(termcolor.colored(pyfiglet.figlet_format('Audio Captcha Generator'), 'yellow'))

import random
import string
# step 1
# generate random numbers like 15579
def generate_number():
    return [random.choice(string.digits) for n in range(6)]
# step 2
# save the speech of evry number and store it in list
import pyttsx3

def generate_speech():
    random_numbers = generate_number()
    engine = pyttsx3.init()
    engine.setProperty('rate', random.randint(10, 100))
    for number in random_numbers:
        engine.save_to_file(number, f'audio/{number}.wav')
        engine.runAndWait()


# step 3
# add noise to audio file list
import moviepy.editor as mp
from os import listdir

def add_noise():

    generate_speech()

    audio_clips = []
    video_clips = []

    for i, audio_file in enumerate(listdir('audio')):
        audio_clip = mp.AudioFileClip(f'audio/{audio_file}')
        video_clip = mp.TextClip('captcha',
        fontsize = 100,
        color = 'white'
        ).set_duration(int(audio_clip.duration)).set_position('center')

        audio_clips.append(audio_clip)
        video_clips.append(video_clip)

    # create audio clip
    final_audio = mp.concatenate_audioclips(audio_clips)
    final_audio.write_audiofile('captcha.mp3')

    # add audio to video
    final_video = mp.concatenate_videoclips(video_clips, method='compose')
    final_video.audio = mp.AudioFileClip('captcha.mp3')
    final_video.write_videofile('captcha.mp4', fps = 30)

    # add noise
    noise_path = f'noise/{random.choice(listdir("noise"))}'
    noise_clip = mp.AudioFileClip(noise_path).subclip(0, int(final_video.audio.duration))

    final_audio = mp.CompositeAudioClip([noise_clip, final_video.audio])
    final_audio.write_audiofile('captcha with noise.mp3', fps = noise_clip.fps)

    a = input('Doy you want to play audio captcha [y/n]: ')
    if a == 'y':
        playsound.playsound('captcha with noise.mp3')
    else:
        exit(0)


def main():
    a = input('Doy you want to generate audio captcha [y/n]: ')
    if a == 'y':
        try:
            add_noise()
        except Exception as e:
            print(e)
            add_noise()
    else:
        exit(0)


if __name__ == '__main__':
    main()
