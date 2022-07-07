import ctypes
import os
import PySimpleGUI as sg
import pytube
from pytube import YouTube
import ffmpeg



def url_window():

    layout_url = [
        [sg.Text('Please Enter YouTube Video URL: ')],
        [sg.Text('URL', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]

    window_url = sg.Window('YouTube Downloader', layout_url, margins=(20, 20))

    event, values = window_url.read()
    streams = set()
    global url
    window_url.close()
    url = values[0]
    yt = YouTube(values[0])

    for stream in yt.streams.filter(type="video"):
        streams.add(stream.resolution)

    streams = {x for x in streams if x is not None}
    global streams_list
    streams_list = list(streams)
    for x in range(len(streams_list)):
        streams_list[x] = streams_list[x].replace('p', '')

    streams_list.sort(key=int)
    for x in range(len(streams_list)):
        streams_list[x] += "p"

    start()


def start():
    layout = [[sg.Text("Choose a Folder: ", font=('Times New Roman', 12)), sg.FolderBrowse()],
              [sg.Text('Choose Your Preferred Quality: ', size=(30, 1), font=('Times New Roman', 13),
                       justification='left')],
              [sg.Combo(streams_list, key='quality', size=(30, 1))],
              [sg.Text('Choose Audio Or Video: ', size=(20, 1), font=('Times New Roman', 13), justification='left')],
              [sg.Combo(["Audio", "Video"], key='Type', size=(30, 1))],
              [sg.Button('Download', font=('Times New Roman', 11))]]

    window = sg.Window('YouTube Downloader', layout)

    event, values = window.read()
    try:
        if values["Type"] == "Video":
            yt = YouTube(url).streams.filter(progressive=True, res=values['quality'])
            ys = yt.get_highest_resolution()
            try:
                ys.download(output_path=values['Browse'])
            except:
                yt = YouTube(url)

                try:
                    os.chdir(values['Browse'])
                except:
                    try:
                        file_name = yt.streams.first().default_filename.replace(".3gpp", "")
                        # download audio only
                        yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
                        audio = ffmpeg.input("audio.mp3")
                        # download video only
                        yt.streams.filter(res=values['quality'], progressive=False).first().download(filename="video.mp4")
                        video = ffmpeg.input("video.mp4")
                        ffmpeg.output(audio, video, file_name+".mp4").run(overwrite_output=True)
                        os.remove('audio.mp3')
                        os.remove('video.mp4')
                    except:
                        pytube.YouTube(url).streams.get_highest_resolution().download(values['Browse'])


            ctypes.windll.user32.MessageBoxW(0, "The Video is Downloaded Successfully", "Congratulations")
        else:
            yt = YouTube(url)

            video = yt.streams.filter(only_audio=True).first()

            destination = values['Browse']
            title = video.title + ".mp3"

            if os.path.exists(destination +"/"+ title):

                raise FileExistsError

            else:
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                ctypes.windll.user32.MessageBoxW(0, "The Song is Downloaded Successfully", "Congratulations")
                window.close()

    except FileExistsError:
        ctypes.windll.user32.MessageBoxW(0, "File Already Exists", "Error!")
        window.close()
        url_window()


begin = url_window()
