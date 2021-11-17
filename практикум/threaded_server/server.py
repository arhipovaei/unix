import socket, threading, sys

def acceptance(conn, addr):
	# запускаем бесконечный цикл приема сообщений от клиентов
	while True:
		# пытамся получить сообщение от клиента
		try:
			data = conn.recv(1024)
		except (ConnectionResetError, ConnectionAbortedError):
			# в случае получения ошибки соединения выводим сообщение об этом на экран
			print(f'Client {addr} aborted connection')
			# инициируем эту ошибку
			raise
			# дополнительно останавливается поток из-за ошибки
		# в случае удачного приема информации выводим кто и что отправил
		print(f'accepted from {addr}:$ {data.decode()}')
		# отправляем клиенту его же сообщение
		conn.send(data)


# устанавливаем лимит вывода глубины сообщений об ошибке
# в случае разрыва клиентом соединения поток будет закрываться, а на
# экран сервера выведется код ошибки разрыва соединения, а не полный traceback
sys.tracebacklimit = 0
# создаем объект сокета
sock = socket.socket()
# задаем ему IP адрес с которого принимать подключения
sock.bind(('', 9090))
# начинаем слушать сокет, то есть ожидаем соединений колиентов
sock.listen(0)

# начинаем бесконечный цикл приема клиентов
while True:
	# принимаем соединение от клиента
	conn, addr = sock.accept()
	# выводим присоединившегося клиента на экран
	print(f'connected {addr}')
	# создаем поток с целью - функцией acceptance, передаем данные клиента и делаем поток демонов, стартуем поток
	threading.Thread(target = acceptance, args = (conn, addr), daemon = True).start()