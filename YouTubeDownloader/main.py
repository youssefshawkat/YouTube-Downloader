import ctypes
import os
import PySimpleGUI as sg
from pytube import YouTube


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
    # https://www.youtube.com/watch?v=1La4QzGeaaQ&t=6s
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
            YouTube(url).streams.filter(res=values['quality']).first().download(output_path=values['Browse'])
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
