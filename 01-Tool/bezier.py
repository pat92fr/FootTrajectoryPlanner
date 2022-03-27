import numpy as np

def fact(n):
    if n<2:
        return 1
    else:
        return n*fact(n-1)

def f(N,k):
	return fact(N)/( fact(k) * fact(N-k) )

def b(t,k,N):
	return f(N,k) * (1-t)**(N-k) * t**k

def bezier(t,points):
	N = points.shape[1]-1 # colnum
	sum = np.zeros((3,1))
	for k in range(0,N+1):
		sum[:,0] += b(t,k,N)*points[:,k]
	return sum

def bezier1D(t,points):
	N = len(points)-1
	sum = 0
	for k in range(0,N+1):
		sum += b(t,k,N)*points[k]
	return sum

if __name__ == "__main__":
	points = np.array( 
		[ 
			[ 20,  20, -20, -20], 
			[ 10,   0,   0,  10],
			[  0,   0,   0,   0]
		]
	)
	print(bezier(0.783,points))