import socket
from time import sleep


signup_jacek = (0).to_bytes(1, 'big') + b'jakub.kucharski@poczta.pl\rjacek\rjacek666'
signup_placek = (0).to_bytes(1, 'big') + b'jakub.kucharski@smcebi.edu.pl\rplacek\rplacek69'
signup_wacek = (0).to_bytes(1, 'big') + b'waclaw.czeresniak@o2.pl\rwacek2\rwszystkiewackitofajneprawaczki'
signup_tomek = (0).to_bytes(1, 'big') + b'tomasz.tomaszewski@tlen.pl\rtominator\rrakendrol'
login_tomek = (1).to_bytes(1, 'big') + b'tominator\rrakendrol'
login_placek = (1).to_bytes(1, 'big') + b'placek\rplacek69'
login_wrong_just_wrong = (1).to_bytes(1, 'big') + b'piotrek\rwhoami?!'
login_tomek_wrong = (1).to_bytes(1, 'big') + b'tominator\rhewimjetal'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 54321))


sock.send(signup_tomek)
r = sock.recv(10)
print(repr(r.decode("utf", "replace")) + ": " + str(len(r)))

sock.send(login_tomek)
r = sock.recv(10)
print(repr(r.decode("utf", "replace")) + ": " + str(len(r)))

sock.send(login_wrong_just_wrong)
r = sock.recv(10)
print(repr(r.decode("utf", "replace")) + ": " + str(len(r)))

sock.send(login_tomek_wrong)
r = sock.recv(10)
print(repr(r.decode("utf", "replace")) + ": " + str(len(r)))


sock.close()

"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 54321))
sock.send(signup_placek)
sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 54321))
sock.send(signup_wacek)
sock.close()"""

