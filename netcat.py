import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()

class Netcat:
    def __int__(self,args,buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建socket对象
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def run(self):
        if self.args.listen:
            self.listen()# 如果是接收方就监听
        else:
            self.send()#如果是发送方就send

    def send(self):
        self.socket.connect((self.args.target,self.args.port)) #进行连接
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt: #键入ctrl+c进行中断
            print('user stop')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)
        while True:
            client_socket,_ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle,args=(client_socket,))
            client_thread.start()

    def handle(self,client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload,'wb') as f:
                f.write(file_buffer)
            message = f'Save file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                        cmd_buffer = b''


                except Exception as e:
                    print(f'server kill {e}')
                    self.socket.close()
                    sys.exit()

"""
main函数暂时未添加
"""
