#python tcp client A
'''import numpy

TotSeats = 5
AvailSeats = 5 
Booked = numpy.zeros((8,5))
heading = ["A","B","C","D","E"]

print("Bus reservation services server .......")
print("No of Seats Available are ", AvailSeats)
print "   ", 
for i in range(0 , 5):
	print heading[i]," ",

print()

for i in range(0 , 8):
	print i+1 , " ",
	for j in range(0,5):
		if(Booked[i][j] == 0):
			print "A"+"  " ,
		else :
			print "R"+"  ",
	print

'''

import socket
import pickle
import numpy
import psycopg2
import json

TicPrice = 1000

heading = ["A","B","C","D","E"]
#TotSeats = 40
SeatAvail = 40 
Booked = numpy.zeros((8,5))
Booked_Matrix = numpy.zeros((8,5))

def DisplaySeats():
	print("Bus reservation services server .......")
	print("No of Seats Available are ", SeatAvail)
	print "   ", 
	for i in range(0 , 5):
		print heading[i]," ",

	print

	for i in range(0 , 8):
		print i+1 , " ",
		for j in range(0,5):
			if(Booked_Matrix[i][j] == 0):
				print "A"+"  " ,
			elif(Booked_Matrix[i][j] == 1) :
				print "R"+"  ",
		print	

def BookTicket():
	global SeatAvail
	global Booked_Matrix
	global Booked
	
	SeatAvail = 40 
	Booked = numpy.zeros((8,5))
	Booked_Matrix = numpy.zeros((8,5))

	SeatAvail=tcpClientA.recv(BUFFER_SIZE)
	SeatAvail = int(SeatAvail)
	Booked = tcpClientA.recv(BUFFER_SIZE)
	Booked_Matrix  =  pickle.loads(Booked)

	DisplaySeats()
	noSeats =raw_input("Enter the number of seats you want to book:")	
	tcpClientA.send(noSeats)
	noSeats = int(noSeats)
	status =tcpClientA.recv(BUFFER_SIZE)
	print "status is " , status
	if(status == "1"):
		print"The no of seats you want are available :"
		User_Data(noSeats)
	else:
		print"The number of seats you require are not available , only " , SeatAvail , "seats are available."
		print"Please try again with only the available seats"



def User_Data(s):
	global SeatAvail
	global Booked_Matrix
	global Booked
	for i in range(1,s+1):
		s_no = raw_input("Enter the seat number you want to book (Eg: A1, E4) :")
		tcpClientA.send(s_no)
		name = raw_input("Enter passengers name :")
		tcpClientA.send(name)
		email = raw_input("Enter your Email ID :")
		tcpClientA.send(email)
		age =  raw_input("Enter passengers age :")
		tcpClientA.send(age)
		spq =  raw_input("Enter if You fall under Special Quota : t for yes , f otherwise :")
		tcpClientA.send(spq)

		if(spq=="t"):
			price = int((float(TicPrice)*(0.95)))
		elif(int(age)>=60):
			price = int((float(TicPrice)*(0.90)))
		else :
			price = TicPrice 

		c_no = ord(s_no[0]) - 65
		r_no = int(s_no[1])
		r_no = r_no -1
		Booked_Matrix[r_no][c_no] = 1
		SeatAvail = SeatAvail - 1;
		ticketDisplay(name , age , s_no , price)
	print "Data Updated"
'''	global SeatAvail
	global Booked_Matrix
	global Booked

	SeatAvail=tcpClientA.recv(BUFFER_SIZE)
	SeatAvail = int(SeatAvail)
	Booked = tcpClientA.recv(BUFFER_SIZE)
	Booked_Matrix  =  pickle.loads(Booked)
'''
	
	
'''SeatAvail=tcpClientA.recv(BUFFER_SIZE)
	SeatAvail = int(SeatAvail)
	Booked = tcpClientA.recv(BUFFER_SIZE)
	Booked_Matrix  =  pickle.loads(Booked)

	print SeatAvail
	print Booked_Matrix

	DisplaySeats()
'''

def CancellTicket():
	DisplaySeats()
	name =raw_input("Enter your  Email ID :")	
	tcpClientA.send(name)
	SNum =raw_input("Enter your  seat number :")	
	tcpClientA.send(SNum)
	statP =tcpClientA.recv(BUFFER_SIZE)
	#ststP = int(statP)
	statP = int((float(statP)*(0.80)))
	print "The amount of Rupees " , statP , " will be refunded" 
	print "Cancellation Succesfull"
	print"*****************************************"
	print"*****************************************"
'''
	c_no = ord(SNum[0]) - 65
	r_no = int(SNum[1])
	r_no = r_no -1
	Booked_Matrix[r_no][c_no] = 0
	SeatAvail = SeatAvail + 1;
	'''
	
	
'''def refundAmount(name , s_no):
	print"Details",details
	print"Refunded"
'''
def history():
	email =raw_input("Enter your  Email ID:")	
	#tcpClientA.send(email)
	print"*****************************************"
	print"*****************************************"
	dbCon = None
	try:
		dbCon = psycopg2.connect(host="localhost",database="postgres",user="postgres" , password="cnp")
		#print dbCon
		cur = dbCon.cursor()
		#print "Database Connection Open"
		cur.execute('SELECT * from thebus where emailId = %(some_n)s', {'some_n': email})
		details =  cur.fetchall()
		print "::::::Your Booking History::::::"
		#print details
		cur.close()
		dbCon.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print error
		print "Invalid data , Please try again"
	finally:
		if dbCon  is not None:
			dbCon.close()
			#dbCon.commit()
		print "   Name       Seat Number   Ticket Price"
		for row in details:
   			print " ", row[0] , "      " , row[3] , "    " , row[5]
		#print "Database connection closed."
	print"*****************************************"
	print"*****************************************"


def ticketDisplay(name , age , s_no , price):
	print"***********Cool Bus travels**************"
	print"*****************************************"
	print"***  Name: " , name
	print"***  Age: " , age
	print"***  SeatNumber: " , s_no
	print"***  Price to be paid is: " , price
	print"*****************************************"
	print""


host=socket.gethostname()
port=2004
BUFFER_SIZE=2000
tcpClientA=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpClientA.connect((host,port))



flag = True
while(flag):

	#DisplaySeats();

	print "Hello Welcome to Bus sevices:"
	print "1:BOOKING"
	print "2:CANCELLATION "
	print "3: VIEW BOOKING HISTORY "
	print "4:EXIT"
	choice=raw_input("Enter your choice:")
	print choice
	if(choice=="1"):
		tcpClientA.send(choice)
		BookTicket()
	elif(choice=="2"):
		tcpClientA.send(choice)
		CancellTicket()
	elif(choice=="3"):
		tcpClientA.send(choice)
		history()
	elif(choice=="4"):
		print"THANK YOU , COME AGAIN"
		tcpClientA.send(choice)
		flag = False

	


tcpClientA.close()














'''
#python tcp client A
import socket

host=socket.gethostname()
port=2004
BUFFER_SIZE=2000
MESSAGE=raw_input("tcpClientA: enter mesggage/enter exit:")
tcpClientA=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpClientA.connect((host,port))
while MESSAGE!='exit':
	tcpClientA.send(MESSAGE)
	data=tcpClientA.recv(BUFFER_SIZE)
	print " client1 received data", data
	MESSAGE=raw_input("tcpClientA: Enter msg to continue / enter exit:")

tcpClientA.close()
'''




