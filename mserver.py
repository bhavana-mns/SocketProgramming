#!usr/bin/env/python
import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import numpy
import pickle
import psycopg2
import json
#import sqlite3
'''
#Miultithreaded python server: TCP Server Socket THread Pool

TotSeats = 5
AvailSeats = 5
Booked = [0,0,0,0,0]
#if(data<AvailSeats):
			#	AvailSeats-=data
			'''

TicPrice = 1000

TotSeats = 40
AvailSeats = 40 
Booked = numpy.zeros((8,5))
heading = ["A","B","C","D","E"]



class ClientThread(Thread):

	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("[+] New Server Socket Thread started for" + ip +":"+ str(port))
	
	def run(self):
		print "In run"
		global AvailSeats 
		global Booked
		while (True):
			choice  = conn.recv(2048)
			print choice
			if(choice =="1"):
				#while(True):
				conn.send(str(AvailSeats))
				Booked_Matrix  = pickle.dumps(Booked)
				conn.send(Booked_Matrix)
				seats_req = conn.recv(2048)
				print("Server recieved data :" + seats_req)
				seats_req = int(seats_req)
				MESSAGE = "0"
				if(AvailSeats>=seats_req):
					MESSAGE = "1"
				conn.send(MESSAGE)
					#if(MESSAGE == "1"):
				if(AvailSeats>=seats_req):	#	for i in range(1,seats_req+1):
					print "Seats req" , seats_req
					i = 1
					while (i<=seats_req):
						print "In While"
						spq = 'f'
						s_no = conn.recv(2048)
						name = conn.recv(2048)
						email=conn.recv(2048)
						age = conn.recv(2048)
						spq = conn.recv(2048)
						print s_no
						i = i+1
						c_no = ord(s_no[0]) - 65
						r_no = int(s_no[1])
						r_no = r_no -1
						Booked[r_no][c_no] = 1
						AvailSeats = AvailSeats - 1;

						if(spq=="t"):
							price = int((float(TicPrice)*(0.95)))
						elif(int(age)>=60):
							price = int((float(TicPrice)*(0.90)))
						else :
							price = TicPrice 

						dbCon = None
						try:
							dbCon = psycopg2.connect(host="localhost",database="postgres",user="postgres" , password="cnp")
							#print dbCon
							cur = dbCon.cursor()
							print "Database Connection Open"
							cur.execute("""insert into thebus(name, age , sq ,SeatNumber , price , emailId) values(%s,%s, %s,%s,%s,%s)""",(name,age , spq , s_no , price,email))
							print "inserted"
							cur.close()
							dbCon.commit()
						except (Exception, psycopg2.DatabaseError) as error:
								print error
						finally:
							if dbCon  is not None:
							    dbCon.close()
							print "Database connection closed."
					print"Data Updated"
				else:
					print"Seats Not available , TRY AGAIN"
				'''
				conn.send(str(AvailSeats))
				Booked_Matrix  = pickle.dumps(Booked)
				conn.send(Booked_Matrix)'''

			elif(choice=="2"):
				'''conn.send(str(AvailSeats))
				Booked_Matrix  = pickle.dumps(Booked)
				conn.send(Booked_Matrix)'''
				email = conn.recv(2048)
				s_no  = conn.recv(2048)
				c_no = ord(s_no[0]) - 65
				r_no = int(s_no[1])
				r_no = r_no -1
				Booked[r_no][c_no] = 0
				AvailSeats = AvailSeats + 1;
				dbCon = None
				try:
					dbCon = psycopg2.connect(host="localhost",database="postgres",user="postgres" , password="cnp")
					#print dbCon
					cur = dbCon.cursor()
					print "Database Connection Open"
					cur.execute('SELECT * from thebus where SeatNumber = %(some_snum)s ', {'some_snum': s_no})
					details =  cur.fetchall()
					#print "Deleted succesfully"
					cur.close()
					dbCon.commit()
				except (Exception, psycopg2.DatabaseError) as error:
					print error
					print "Invalid data , Please try again"
				finally:
					if dbCon  is not None:
						dbCon.close()
					#dbCon.commit()
					print "Database connection closed."
				print " ",details

				dbCon = None
				try:
					dbCon = psycopg2.connect(host="localhost",database="postgres",user="postgres" , password="cnp")
					#print dbCon
					cur = dbCon.cursor()
					print "Database Connection Open"
					cur.execute("""delete from thebus where emailId = %s and SeatNumber =%s ;""",(email , s_no ))			
					print "Deleted succesfully"
					cur.close()
					dbCon.commit()
				except (Exception, psycopg2.DatabaseError) as error:
					print error
					print "Invalid data , Please try again"
				finally:
					if dbCon  is not None:
						dbCon.close()
					print "Database connection closed."
				#details.astype(int)
				print details
				tempVar = int(details[0][5])
				print type(tempVar)
				conn.send(str(tempVar))	
				print "Cancell"
				
			elif(choice=="3"):
				#email = conn.recv(2048)
				print "Booking History "
				
			else:
				print "Good Bye"
				break;

#cursor.execute('SELECT * from table where id = %(some_id)d', {'some_id': 1234})
#Multithreaded python server: TCP Server Socket THread stub

TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 20 #Usually 1024 , but we need quick response 

tcpServer =  socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
tcpServer.bind((TCP_IP , TCP_PORT))
threads = []

while True :
	tcpServer.listen(4)
	( conn , (ip , port)) =  tcpServer.accept()
	newthread =  ClientThread(ip , port)
	newthread.start()
	threads.append(newthread)

for t in threads: 
	t.join


#Solutions to Prob
#getidT1 -> close T1

#select system call  
