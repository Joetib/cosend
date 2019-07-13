from flask import Flask, url_for, render_template, send_file
import tkinter
import tkinter.messagebox as msgbox
import os
from socket import gethostbyname_ex, gethostname, gethostbyname
from wsgiref.simple_server import make_server
from threading import Thread
from time import sleep
import glob
import webbrowser


folder = ''

if os.path.isfile('foldername.txt'):
    """checks and copies the content of foldername.txt and use as the serving folder"""
    with open('foldername.txt', 'r') as foldername:
        folder = foldername.read().strip()
    if not folder.endswith('/'):
        folder += '/'


def reverse_url(filenames):
    """reduce the list filenames to more simpler list of lists
    containing filename and corresponding revesed url related to 'download_file' route"""
    filename = []
    for dd in filenames:
        for d in dd:
            d = os.path.abspath(d)
            if d.endswith('/'):
                pass
            else:
                filename.append(d)
    file_list = []
    for file in filename:
        sub_file_list = []
        dir, name = os.path.split(file)
        sub_file_list.append(url_for('download_file', dire=file))
        sub_file_list.append(name)
        file_list.append(sub_file_list)
    return file_list


def get_video_list():
    """gets a  list of video files in the directory served : 'folder' """
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.mp4', recursive=True))
    filenames.append(glob.glob(folder+'*.mkv', recursive=True))
    filenames.append(glob.glob(folder+'*.flv', recursive=True))
    print(filenames)
    return reverse_url(filenames)


def get_pictures_list():
    """gets a  list of picture files in the directory served : 'folder' """
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.jpg', recursive=True))
    filenames.append(glob.glob(folder+'*.jpeg', recursive=True))
    filenames.append(glob.glob(folder+'*.png', recursive=True))
    filenames.append(glob.glob(folder+'*.gif', recursive=True))
    return reverse_url(filenames)


def get_music_list():
    """gets a  list of audio files in the directory served : 'folder' """
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.mp3', recursive=True))
    filenames.append(glob.glob(folder+'*.wav', recursive=True))
    filenames.append(glob.glob(folder+'*.m4a', recursive=True))
    return reverse_url(filenames)


def get_documents_list():
    """gets a  list of documents files in the directory served : 'folder' """
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.doc', recursive=True))
    filenames.append(glob.glob(folder+'*.txt', recursive=True))
    filenames.append(glob.glob(folder+'*.docx', recursive=True))
    filenames.append(glob.glob(folder+'*.pdf', recursive=True))
    filenames.append(glob.glob(folder+'*.c', recursive=True))
    filenames.append(glob.glob(folder+'*.cpp', recursive=True))
    filenames.append(glob.glob(folder+'*.py', recursive=True))
    filenames.append(glob.glob(folder+'*.java', recursive=True))
    return reverse_url(filenames)

def get_application_list():
    """gets a list of application files in the directory served : 'folder'
    These files include .exe, .apk, .msi"""
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.exe', recursive=True))
    filenames.append(glob.glob(folder+'*.msi', recursive=True))
    filenames.append(glob.glob(folder+'*.apk', recursive=True))
    return reverse_url(filenames)


def get_compressed_list():
    """gets a  list of compressed files in the directory served : 'folder'
    These files include .rar, .iso, .zip, .tar, .gz"""
    global folder
    filenames = []
    filename = []
    filenames.append(glob.glob(folder+'*.zip', recursive=True))
    filenames.append(glob.glob(folder+'*.rar', recursive=True))
    filenames.append(glob.glob(folder+'*.iso', recursive=True))
    filenames.append(glob.glob(folder+'*.tar', recursive=True))
    filenames.append(glob.glob(folder+'*.gz', recursive=True))
    filenames.append(glob.glob(folder+'*.7z', recursive=True))

    return reverse_url(filenames)


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    """Route for the index page"""
    videos_list = get_video_list()
    pictures = get_pictures_list()
    musics = get_music_list()
    documents = get_documents_list()
    applications = get_application_list()
    compressed = get_compressed_list()

    return render_template('index.html', section='index',
                           videos=videos_list,
                           pictures=pictures,
                           documents=documents,
                           musics=musics,
                           compressed=compressed,
                           applications=applications)


@app.route('/download/<string:dire>/')
def download_file(dire):
    """Route that serves files requested to enable download.
    Also ensures that the requested file is in the directory being served to avoid criminal access to files"""

    if str(os.path.abspath(dire)).startswith(str(os.path.abspath(folder))):
        return send_file(dire, as_attachment=True)
    return '<h1 style="color: red; text-align: center;">Sorry File not found</h1>'


@app.route('/video/')
def video_list():
    """Serves video files only through the /video/ link"""
    videos = get_video_list()
    return render_template('index.html', section='video', videos= videos,)


@app.route('/music/')
def music_list():
    musics = get_music_list()
    return render_template('index.html', section='music', musics=musics)


@app.route('/picture/')
def picture_list():
    """serves page for pictures through /pictures/ route"""
    pictures = get_pictures_list()
    return render_template('index.html', section='picture', pictures=pictures)


@app.route('/document/')
def document_list():
    """serves page for documents through /document/ route"""
    documents = get_documents_list()
    return render_template('index.html', section='document', documents=documents)


@app.route('/application/')
def application_list():
    """serves page for applications through /application/ route"""
    applications = get_application_list()
    return render_template('index.html', section='application', applications=applications)


@app.route('/compressed/')
def compressed_list():
    """serves page for compressed files through the /compressed/ route"""
    compressed = get_compressed_list()
    return render_template('index.html', section='compressed', compressed=compressed)


class Window(tkinter.Tk):
    def __init__(self):
        """initiates the main window"""
        super().__init__()

        self.host = gethostbyname(gethostname())
        self.port = 80
        self.server = None
        self.server_thread = None
        self.configure(bg="green")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            self.tk.call('wm', 'iconphoto', self._w, tkinter.PhotoImage(file='assets/icon.png'))
        except:
            pass

        self.geometry("350x200")
        self.title('CoSend app')
        self.resizable(False, False)

        copyright_label = tkinter.Label(self, text="© JoeTiB InCoroporation & CyberTek & Paddy Pyker", bg='green')
        copyright_label.pack(side=tkinter.BOTTOM, pady=(10, 10))

        self.main_frame = tkinter.Frame(self, width=300, height=150, bg="green")
        self.main_frame.pack_propagate(0)

        self.server_state_label = tkinter.Label(self.main_frame, text="Server is off. ", height=2)
        self.server_state_label.pack(side=tkinter.BOTTOM, fill=tkinter.X, pady=(7, 0))

        self.top_main_frame = tkinter.Frame(self.main_frame, bg="green")
        self.top_main_frame.pack_propagate()
        self.app_config_label = tkinter.Label(self.top_main_frame, width=19, text="IP: {}\n Dir: {}".format(
            self.host, str(folder)))
        self.app_config_label.pack(side=tkinter.LEFT, padx=(0, 5))
        self.about = tkinter.Button(self.top_main_frame, text="Help", height=2, width=20, command=self.show_help)
        self.about.pack(side=tkinter.RIGHT, padx=(0, 0))
        self.top_main_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        self.config_button = tkinter.Button(self.main_frame, text="Click to configure",
                                            width=20, height=2, command=self.show_config)
        self.config_button.pack(side=tkinter.RIGHT, padx=(5, 0), pady=(2, 0))

        self.start_button = tkinter.Button(self.main_frame, text='start server'
                                           , command=self.startserver, width=20, height=2)
        self.start_button.pack(side=tkinter.LEFT, padx=(0, 5), pady=(2, 0))

        self.stopbutton = tkinter.Button(self.main_frame, text='stop server', width=200, height=2,
                                         command=self.stopserver)

        self.main_frame.pack(side=tkinter.BOTTOM)

        self.config_frame = tkinter.Frame(self, width=300, height=150, bg="green")
        self.config_frame.pack_propagate(0)

        dir_input_frame = tkinter.Frame(self.config_frame, width=300, height=30, bg="green")
        dir_input_frame.pack_propagate(0)

        self.dir_label = tkinter.Label(dir_input_frame, height=2, width=12, text="Enter new dir: ")
        self.dir_label.pack(side=tkinter.LEFT, padx=(0, 10))

        self.dir_input = tkinter.Text(dir_input_frame, height=2)
        self.dir_input.pack(side=tkinter.RIGHT)

        dir_input_frame.pack(side=tkinter.BOTTOM, pady=(5, 5))

        ip_input_frame = tkinter.Frame(self.config_frame, width=300, height=30, bg="green")
        ip_input_frame.pack_propagate()

        ip_label = tkinter.Label(ip_input_frame, width=12, height=2, text="Use custom ip:")
        ip_label.pack(side=tkinter.LEFT, padx=(0, 5))

        self.ip_input = tkinter.Text(ip_input_frame, height=2)
        self.ip_input.pack(side=tkinter.RIGHT, padx=(5, 0))

        ip_input_frame.pack(side=tkinter.BOTTOM, pady=(5, 5))
        back_button = tkinter.Button(self.config_frame, text="Back", height=2, width=20, command=self.show_main_frame)
        back_button.pack(side=tkinter.LEFT, padx=(0, 5))

        save_button = tkinter.Button(self.config_frame, height=2,  width=20, text="Save", command=self.save_config)
        save_button.pack(side=tkinter.RIGHT, padx=(5, 0))

    def show_help(self):
        """Shows the help info using tkinter's messagebox"""
        msgbox.showinfo("CoSend Help", "This is a simple help to get you started.\n\n"
                                       " CoSend is a simple app that helps"
                                       " you to share files from a chosen directory.\n\n"
                                       "Please go to Configurations and set your "
                                       "preferred directory to serve files from.\n\n"
                                       "Also note: If you have multiple network adapters,"
                                       "such as if you have virtual machine players "
                                       "then please configure the Ip as your default Ip"
                                       "on the network you intend to use.\n\n"
                                       "Please make sure that the set ip is an ip that is related to your device.\n\n"
                                       "You can find the ip addresses of your computer by entering 'ipconfig'"
                                       " in the command prompt.\n\n"
                                       "After starting the server, open a browser and connect"
                                       " to the ip address the server is launched on.\n \n"
                                       "You can also edit the template and styling by editing 'index.html' found in the"
                                       "templates directory where the app is installed.\n\n"
                                       "Ensure that you do not make changes to the"
                                       " variables used in rendering the templates. Changes in these variables will"
                                       "result in incorrect rendering. However you are free to change the styling."
                                       "without encountering any major problems\n"
                                       "\n Enjoy!!!\n"
                                       "\n"
                                       "\n"
                                       "© JoeTiB Incorporation & Paddy Pyker")

    def show_config(self):
        """shows the configuration frame """
        self.main_frame.pack_forget()
        self.config_frame.pack()

    def on_closing(self):
        """Runs whenever the user closes the window. It checks to see if the server is still running and if so closes
        it to avoid having the server run in the background"""
        if self.server:
            self.stopserver()
        self.quit()

    def show_main_frame(self):
        """Show the main frame """
        self.config_frame.pack_forget()
        self.main_frame.pack()

    def save_config(self):
        """handles saving of configured settings in the various text input areas in th configuratins page
        It checks if the ip address specified is valid (if you type in a value in the ip input area)
        and checks if the folder specified exits ( if you type in a value in the directory input area)
        If any one of these conditions is not met, an error alert pops up.
        The server is run in a seperate thread to avoid interruptions with the main thread and avoid breaking user
         interface updates."""
        global folder
        text_dir = str(self.dir_input.get("1.0", tkinter.END)).strip()
        text_addr = str(self.ip_input.get("1.0", tkinter.END)).strip()
        if text_addr != '' or text_dir != '':
            if text_addr != '':
                if text_addr in gethostbyname_ex(gethostname())[-1]:
                    self.host = text_addr
                else:
                    a = str(gethostbyname_ex(gethostname())[-1])
                    msgbox.showerror('IP address Error', 'Sorry the ip address you typed in is \n'
                                                         'not associated with this device\n'
                                                         'the valid ip addresses are {}'.format(a))
            if text_dir != '':
                if os.path.isdir(text_dir):
                    if not text_dir.endswith('/'):
                        text_dir += '/'
                    folder = text_dir
                    with open('foldername.txt', 'w') as foldername:
                        foldername.write(text_dir.strip())

            self.app_config_label.configure(text="IP: {}:{}\n Dir: {}".format(self.host, str(self.port), str(folder)))
            self.show_main_frame()

    def startserver(self):
        """Starts the http server and opens a broswer showing the index page
        If an error occurs in the process, a tkinter messagebox error info page is shown"""
        global folder
        if folder != '' and os.path.isdir(folder):
            try:
                self.server = make_server(self.host, self.port, app)
                self.server_thread = Thread(target=self.server.serve_forever)
                self.server_thread.start()
                sleep(2)
                self.server_state_label.configure(text='server running on {} with port {}'.format(str(self.host),
                                                                                                  str(self.port)))
                self.stopbutton.pack(side=tkinter.LEFT, padx=(0, 5), pady=(5, 0))
                self.start_button.pack_forget()
                webbrowser.open('http://'+self.host+':'+str(self.port))
            except OSError:
                msgbox.showerror("IP error", "The set Ip address is invalid!.\n Use an IPv4"
                                             " address that is related to this machine.")
        else:
            self.server_state_label.configure(text="Please configure path to server files first")

    def stopserver(self):
        """Stops the server thread and shuts the server down"""
        self.server_state_label.configure(text='Closing server ...')
        self.server.shutdown()
        self.server_thread.join()
        sleep(1)
        self.stopbutton.pack_forget()
        self.start_button.configure(text="Restart server!")
        self.server_state_label.configure(text='Server closed')
        self.start_button.pack(side=tkinter.LEFT, padx=(0, 5), pady=(5, 0))


if __name__ == '__main__':
    if not os.path.isfile('templates/index.html'):
        if os.path.isfile('index.html'):
            os.makedirs('templates')
            with open('index.html', 'r') as template:
                template_content = template.read()
            with open('templates/index.html', 'w') as template:
                template.write(template_content)
            os.remove('index.html')
        else:
            msgbox.showerror('Template Not Found', 'The template "index.html" cannot be found \n'
                                                   ' please reinstall the application.')
            import sys
            sys.exit(0)
    window = Window()
    window.mainloop()
