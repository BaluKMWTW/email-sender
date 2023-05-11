from socket import *
from base64 import *
import ssl
userEmail = input("Enter your email address: ")
userPasswrod = input("Enter your password: ")
userDestinationEmail = input("Enter destination: ")
userSubject = input("Enter subject: ")
userBody = input("Enter message:" )

msg = "I love computer networks!\r\n"
endmsg = "\r\n.\r\n"

#Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
port = 587
#465

#Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

#Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

#AUTH
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recv2 = clientSocket.recv(1024)

sslClientSocket = ssl.wrap_socket(clientSocket)

emailA = b64encode(userEmail.encode())
emailP = b64encode(userPasswrod.encode())

authrorizationCMD = "Auth Login\r\n"

sslClientSocket.send(authrorizationCMD.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)

sslClientSocket.send(emailA + "\r\n".encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)

sslClientSocket.send(emailP + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)

#Send MAIL FROM command and print server response.
mailFromCommand = "MAIL FROM: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(mailFromCommand.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

#Send RCPT TO command and print server response.
rcptToCommand = "RCPT TO: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(rcptToCommand.encode())
recv6 = sslClientSocket.recv(1024)
print(recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')

#Send DATA command and print server response.
dataCommand = 'DATA\r\n'
sslClientSocket.send(dataCommand.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)
if recv7[:3] != '354':
    print('354 reply not received from server.')

#Send message data.
sslClientSocket.send("Subject: {}\n\n{}".format(userSubject, msg).encode())

#Message ends with a single period.
sslClientSocket.send(endmsg.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)
if recv8[:3] != '250':
    print('250 reply not received from server.')

#Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
sslClientSocket.send(quitCommand.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)
if recv9[:3] != '221':
    print('221 reply not received from server.')

#Close the socket.
sslClientSocket.close()
