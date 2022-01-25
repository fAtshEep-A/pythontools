import socket

target_host = "www.baidu.com"
target_port = 80

#建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#连接客户端
client.connect((target_host,target_port))

#发送一些数据
client.send("GET / HTTP/1.1\r\nHost:google.com\r\n\r\n")

#接收一些数据
response = client.recv(4096)
print(response)

#首先建立一个AF_INET和SOCK_STREAM参数的socket对象，AF_INET说明我们将使用标准的ipv4地址和主机名，SOCK_STREAM说明我们是tcp客户端
#然后连接到服务器
#发送一些数据
#接收返回的数据，并将数据打印出来