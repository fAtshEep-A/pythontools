import socket

target_host = "127.0.0.1"
target_port = 80

#创建一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#发送数据
client.sendto("AAAAABBBBB",(target_host,target_port))

#接收数据
data,addr = client.recvfrom(4096)

print(data)

#我们套接字的类型从tcp的SOCK_STREAM改成了SOCK_DGRAM，之后我们调用sento函数将数据传到想发送的服务器上。
#因为UDP是一个无连接状态的传输协议，所以不需要在此之前调用connect()函数
#最后一步是调用recvfrom()函数接收返回的数据包。你将接收到回传的数据及远程主机的信息及端口号