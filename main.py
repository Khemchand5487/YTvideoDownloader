from tkinter import * # pip install tkinter
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk # pip install pillow
from pytube import YouTube # pip install pytube3
from threading import *
from tkinter.messagebox import askyesno

# video size container
file_size = 0

# thread for downloading video
def downThread():
    thread = Thread(target=downloader)
    thread.start()

# monitor the progress of downloading
def progress(chunk, file_handle, remaining):
    global download_status
    file_downloaded = file_size-remaining
    per = (file_downloaded/file_size)*100  # percentage of downloaded file
    download_status.config(text='{:00.0f} % downloaded'.format(per))


# Download the video
def downloader():
    global file_size, download_status
    download_button.config(state=DISABLED) # Disable the download button
    download_status.place(x=230,y=250)
    try:
        url1 = url.get() # url of the video
        path = askdirectory() # ask for the download location
        yt = YouTube(url1, on_progress_callback=progress)  # search and load the video using url
        video = yt.streams.filter(progressive=True, file_extension='mp4').first() # highest quality video available
        file_size = video.filesize # total size of the video
        video.download(path) # download the video
        download_status.config(text='Download Finish...')
        res = askyesno("YTvideo Downloader [Made by KD Singh]", "Do you want to download another video?")
        if res == 1:
            url.delete(0, END)
            download_button.config(state=NORMAL)
            download_status.config(text=' ')
        else:
            root.destroy() # exit the programme
    except Exception as e:
        download_status.config(text='Faild! There is an error.') # show the error occured


root = Tk() # main window handler
root.geometry('600x400') # size of the window
root.iconbitmap('logo.ico') # logo of the window

root.title("YTvideo Downloader [Made by KD Singh]") # title of window
root['bg'] = 'red'  # color of window
root.resizable(0, 0) # disable maximize button

img = Image.open('logo.ico') # logo image
img = img.resize((80, 80), Image.ANTIALIAS) # resize the logo image
img = ImageTk.PhotoImage(img) # load the image for tkinter
head = Label(root, image=img) # main image or icon as a heading
head.config(anchor=CENTER)
head.pack()
enter_url = Label(root, text='Enter URL:', bg='red')
enter_url.config(font=('Verdana', 15))
enter_url.place(x=5,y=120)
url = Entry(root, width=35, border=1, relief=SUNKEN, font=('Verdana', 15)) # take input of url from user
url.place(x=125, y=123)
download_button_img = Image.open('download_button.png')
download_button_img = download_button_img.resize((200,150), Image.ANTIALIAS)
download_button_img = ImageTk.PhotoImage(download_button_img) # download button image

download_button = Button(root, width=160, height=45, bg='red', relief=FLAT, activebackground='red', command=downThread) # download button
download_button.config(image=download_button_img)
download_button.place(x=220,y=170)
download_status = Label(root, text="Please wait...", font= ('Verdana', 15), bg = 'red') # download status


root.mainloop()