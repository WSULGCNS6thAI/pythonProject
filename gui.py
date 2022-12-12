import tkinter
import threading
import socket
import sys

IP = ""
PORT = 0

def connect(event=None):
    global IP, PORT
    input_string = input_addr_string.get()
    addr = input_string.split(":")
    IP = addr[0]
    PORT = int(addr[1])
    print("서버 접속 [{}:{}]".format(IP, PORT))
    win_connect.destroy()

def recv_message():
    global sock
    while True:
        msg = sock.recv(1024)
        chat_list.insert(tkinter.END, msg.decode("utf-8"))
        chat_list.see(tkinter.END)

def send_message(event=None):
    global sock
    message = input_msg.get()
    sock.send(bytes(message, "utf-8"))
    input_msg.set("")
    if message == "/bye":
        sock.close()
        window.quit()

def window_input_close(event=None):
    print("윈도우 종료")
    win_connect.destroy()
    sys.exit(1)

win_connect = tkinter.Tk()
win_connect.protocol("WM_DELETE_WINDOW", window_input_close)
win_connect.title("접속대상")

tkinter.Label(win_connect, text="접속대상").grid(row=0, column=0)
input_addr_string = tkinter.StringVar(value="127.0.0.1:8274")
input_addr = tkinter.Entry(win_connect, textvariable=input_addr_string, width=20)
input_addr.grid(row=0, column=1, padx=5, pady=5)
connect_button = tkinter.Button(win_connect, text="접속하기", command=connect)
connect_button.grid(row=0, column=2, padx=5, pady=5)

width = 280
height = 40

screen_width = win_connect.winfo_screenwidth()
screen_height = win_connect.winfo_screenheight()

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))
win_connect.geometry('%dx%d+%d+%d' % (width, height, x, y))
input_addr.focus()
win_connect.mainloop()

window = tkinter.Tk()
window.title("채팅 클라이언트")
frame = tkinter.Frame(window)
scroll = tkinter.Scrollbar(frame)
scroll.pack(side = tkinter.RIGHT, fill=tkinter.Y)
chat_list = tkinter.Listbox(frame, height=15, width=50, yscrollcommand=scroll.set)
chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)
frame.pack()

input_msg = tkinter.StringVar()
inputbox = tkinter.Entry(window, textvariable=input_msg)
inputbox.bind("<Return>", send_message)
inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)
send_button = tkinter.Button(window, text="전송", command=send_message)
send_button.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("서버 접속시도 [{}:{}]".format(IP, PORT))
r = sock.connect_ex((IP, PORT))
if r == 0:
    receive_thread = threading.Thread(target=recv_message)
    receive_thread.daemon=True
    receive_thread.start()

    width = 383
    height = 292

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    window.mainloop()