#! python3
import sys
from textwrap import wrap

L = 64
b = 6
Nr = 12 + 2*b
initial_vector = [ 0 for initial in range(1600) ]

data = [
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3", 
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
		"A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "A3", "A3", "A3", "A3", "A3", "A3", "A3", "A3",
        "06", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "00",
        "00", "00", "00", "00", "00", "00", "00", "80",
]

rot_table = [ 
	[21 ,136 ,105, 45, 15],
	[120, 78 ,210, 66, 253],
	[28 ,91 ,0 ,1 ,190],
	[55 ,276 ,36 ,300, 6],
	[153, 231, 3 ,10 ,171]
]

RC = [
	"0000000000000001", "0000000000008082", "800000000000808A", "8000000080008000", "000000000000808B", "0000000080000001", 
	"8000000080008081", "8000000000008009", "000000000000008A", "0000000000000088", "0000000080008009", "000000008000000A", 
	"000000008000808B", "800000000000008B", "8000000000008089", "8000000000008003", "8000000000008002", "8000000000000080", 
	"000000000000800A", "800000008000000A", "8000000080008081", "8000000000008080", "0000000080000001", "8000000080008008"
]

data = input("Enter data in hexadecimal : ")
data = wrap(data,2)

if len(data) < 288:
	length = len(data)
	for d in range(288-length):
		data = ["00"]+data

def theta(cube):
	output_block = [[[-1 for xy in range(64)] for xy in range(5)] for xy in range(5)]
	for x in range(5):
		for y in range(5):
			for z in range(64):
				
				col1_x = (x-1)%5
				col1_z = z

				col2_x = (x+1)%5
				col2_z = (z-1)%64
				#print(col1_x,col1_z,col2_x,col2_z)

				xor_col1 = cube[col1_x][0][col1_z] ^ cube[col1_x][1][col1_z] ^ cube[col1_x][2][col1_z] ^ cube[col1_x][3][col1_z] ^ cube[col1_x][4][col1_z]
				xor_col2 = cube[col2_x][0][col2_z] ^ cube[col2_x][1][col2_z] ^ cube[col2_x][2][col2_z] ^ cube[col2_x][3][col2_z] ^ cube[col2_x][4][col2_z]

				output_block[x][y][z] = cube[x][y][z] ^ xor_col2 ^ xor_col1
				#print(cube[col1_x][0][col1_z],cube[col1_x][1][col1_z],cube[col1_x][3][col1_z],cube[col1_x][4][col1_z])

	return output_block

def rho(cube):
	a_prime = [ [[-1 for zs in range(64)] for ys in range(5)] for xs in range(5) ]
	a_prime[2][2] = cube[2][2]
	X = 1
	Y = 0 
	for t in range(24):
		#print(x,y)
		for z in range(64):
			num = int(((t+1)*(t+2))/2)
			num = (z-num)%64
			x = (X+2)%5
			y = (Y+2)%5
			a_prime[x][y][z] = cube[x][y][num]
		tempx = X
		tempy = Y
		X = Y 
		Y = (2*tempx + 3*tempy)%5
	return a_prime

def pi(temp):
	B = [[[-1 for xpa in range(L)] for xpb in range(5)] for xpc in range(5)]
	for X in range(5):
		for Y in range(5):
			x_cordinate = (X+3*Y)%5
			y_cordinate = X
			x = (x_cordinate+2)%5
			y = (y_cordinate+2)%5
			B[(X+2)%5][(Y+2)%5] = temp[x][y]
	return B

def chi(B):
	# for z in range(5):
	A = [[[0 for x in range(L)] for x in range(5)] for x in range(5)]
	for x in range(5):
		for y in range(5):
			for z in range(L):
				A[x][y][z] = B[x][y][z] ^ ( (B[(x+1)%5][y][z]+1)%2 & B[(x+2)%5][y][z] )
	return A

def iota(cube,round):
	xor = "{0:064b}".format(int(RC[round],16))[::-1]
	#print(cube[2][2])
	for z in range(64):
		cube[2][2][z] = cube[2][2][z] ^ int(xor[z],2)
	#print(cube[2][2])
	return cube

def xor(row1,row2,n):
	output = [ 0 for y in range(n) ] 
	for xorfunc in range(n):
		output[xorfunc] = row1[xorfunc] ^  row2[xorfunc]
	return output

def getcube(msgBit):
	getcube = [[[-1 for x in range(L)] for x in range(5)] for x in range(5)]
	for Y in range(5):
		for X in range(5):
			for z in range(64):
				x = (X+2)%5
				y = (Y+2)%5
				getcube[x][y][z] = msgBit[64*(5*Y+X) + z ]
	return getcube

def byte_state(input_row,n=1600):
	out = list()
	for op in range(0,n,8):
		binary = (str(input_row[op])+str(input_row[op+1])+ str(input_row[op+2])+str(input_row[op+3]) + str(input_row[op+4])+str(input_row[op+5])+ str(input_row[op+6])+str(input_row[op+7]))[::-1]
		#binary = binary[::-1]
		out.append("{0:02x}".format(int(binary,2)))
	return out

def getrow_from_cube(cube,n=1600):
	getrow_from_cube = [0 for x in range(n)]
	index = 0
	for Y in range(5):
		for X in range(5):
			for z in range(64):
				x = (X+2)%5
				y = (Y+2)%5
				getrow_from_cube[index] = cube[x][y][z]
				index = index +1
	# print(getrow_from_cube)
	# getrow_from_cube = getrow_from_cube
	return getrow_from_cube

def getbinary_from_byte_state(row,n=200):
	bit = list()
	for index in range(n):
		hexa = row[index]
		binary = list("{0:08b}".format(int(hexa,16))[::-1])
		for z in binary:
			bit.append(int(z)) 
	return bit

def f(cube):
	for x in range(Nr):
		after_theta_cube = theta(cube)
		after_theta_row = getrow_from_cube(after_theta_cube)
		before_rho_cube = after_theta_cube
		after_rho_cube = rho(before_rho_cube)
		after_pi_cube = pi(after_rho_cube)
		after_chi_cube = chi(after_pi_cube)
		after_iota_cube = iota(after_chi_cube,x)
		cube = after_iota_cube
	return getrow_from_cube(cube)

def get_output(ByteState,n=1):
	List = [ 28, 32, 48, 64 ]
	output = ""
	for x in range(List[n-1]):
		output+=ByteState[x]
	return output

def hash(bs,option):
	row = getbinary_from_byte_state(bs,len(bs))
	rounds = int(len(bs)/144)
	vector = initial_vector
	list2 = [ 1152, 1088, 833, 576 ]
	r = list2[option-1]
	for t in range(rounds):
		up = xor(row[:r],vector[:r],r)
		down = vector[r:]
		inp = up+down
		cube = getcube(inp)
		row_out = f(cube)
		vector = row_out
		row = row[r:]
	return(byte_state(row_out))

option = int(input("Enter 1 for sha3-224\n      2 for sha3-256\n      3 for sha3-384\n      3 for sha3-512\n Your answer : "))

hashed =  hash(data,option)

print("Hashed Input :",get_output(hashed,option))
