#one file code - incomplete VCs - setting bounds

#! ~/anaconda/bin/python
import numpy as np
import scipy.spatial.distance as spa
from scipy.sparse.csgraph import dijkstra
import scipy as sp
import random
import matplotlib.pyplot as plt
import math
# from repo.dimredu.denseSolvers import MCWithBounds
from repo.dimredu import sRPCAviaADMMFast
from repo.dimredu import MCviaIALMFast  
import networkx as nx


## start of code:------------------------
#percentage of elements to be removed
fraction = 20 


# -------------LOADING NETWORK-----------------------------
############################## Hop distance matrix #############################

## making the adjacency matrix  
dHp = np.loadtxt('Original_Dist_nw1.txt')
n,n = dHp.shape
adj = np.ones((n,n))



# exit()
# -------------------------------------------------------
# create graph
gg = nx.Graph()
adj = np.zeros((n,n))

for i in range(n):
    gg.add_node(i)

r,c = dHp.shape
for i in range(r):
  for j in range(c):
    if dHp[i,j]==1:
      adj[i,j] = 1

for i in range(r):
    for j in range(c):
        if adj[i,j]==1: #detecting where there is an edge
            gg.add_edge(i,j)


#print('----------------------------TEST----------------------------')
#print (nx.algorithms.components.is_connected(gg))





# plt.figure(1)
# nx.draw_networkx(gg)
# plt.show()


# SELECTING ANCHOR NODES-------------
row_size = n

# UPDATE NAMES:------------
VC = np.copy(dHp)
A = np.copy(adj)

#print ("Hello there---------")

# remove the given fraction 
[Rn, Cn] = VC.shape
rem_num = (Rn*Cn*fraction/100) # total number of entries to be removed
rem_num = int(rem_num) 
VC_removed = np.copy(VC)
VCcopy = np.copy(VC)
RR = np.random.choice(Rn, rem_num)
CC = np.random.choice(Cn, rem_num)
 
for xx in range(rem_num):
  i=RR[xx]
  j=CC[xx]
  VC_removed[i][j] = 0
  VCcopy[i][j] = -1
  VC_removed[j][i] = 0
  VCcopy[j][i] = -1


#print (VC_removed)
#print ("total removed entries: ", rem_num)
print ("fraction: ", fraction)

# ------ calculate bounds for the missing entries.. set bounds of known entries as the current value
m,n = VC_removed.shape

#print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print(m)
#print(n)

# ------ calculate bounds for the missing entries.. set bounds of known entries as the current value
m,n = VC_removed.shape

UB = np.zeros((m,n)) # initial matrix for Upper bound
LB = np.zeros((m,n)) # initial matrix for lower bound

count = 0            # counts the entries for which LB != UB
delta = []           # record of gap between LB and UB

# # for complete distance matrix
for i in range(m):
  for j in range(n):
  	# check if it is diagonal entry:
    if i == j:
    	LB[i,j] = 0
    	UB[i,j] = 0
    	# delta = np.insert(delta, len(delta), UB[i,j]-LB[i,j] )
    	continue
    	
    # off diagonal entries
    if VCcopy[i,j]==(-1): #if the entry is missing..
      # consider only known entries
    	valid = []
    	index_i = np.where( VCcopy[i,:] != (-1) )
    	index_j = np.where( VCcopy[j,:] != (-1) )
    	valid = np.intersect1d(index_i, index_j)

      # calculate lower bound:
      #if there are any known entries
    	if len(valid) > 0:
      		XX = max(abs(VC_removed[i,valid]-VC_removed[j,valid]))
      		LB[i,j] = max(XX, 1)
      		UB[i,j] = min(VC_removed[i,valid]+VC_removed[j,valid])
    	else:
      		# print ('---------couldnt find anything-----------')
      		XX = min(abs(VC_removed[i,:]-VC_removed[j,:]))
      		LB[i,j] = max(XX, 1)
      		l1 = LB[i,j]
      		UB[i,j] = max(VC_removed[i,:]+VC_removed[j,:])
      		# print ('No valid case found: ',LB[i,j], UB[i,j], VC[i,j], VCcopy[i,j], VC_removed[i,j] )

    # if the entry is known:
    else:
    	UB[i,j] = VC_removed[i,j]  #set it to the actual value
    	LB[i,j] = VC_removed[i,j]  #set it to the actual value
    # count non-exact entries
    # if UB[i,j] != LB[i,j]:
      	# count = count + 1
    # error:
    # if (VC[i,j] > UB[i,j]) or (VC[i,j] < LB[i,j]):
    	# print ('ERROR')
    	# print ('LB,UB,actual, removed: ',LB[i,j], UB[i,j], VC[i,j], VCcopy[i,j], VC_removed[i,j] )
    	# print (i,j)
    	# print ('Something is wrong - FIX it')
    	# exit()   #there should be no error so if there is any, garcefully exit the code
    # delta = np.insert(delta, len(delta), UB[i,j]-LB[i,j] )

#  ----fill values before passing to Matrix Completion-----------
count = 0            # counts the entries for which LB != UB
for i in range(m):
	for j in range(n):
		if UB[i,j] == LB[i,j]:
			VCcopy[i,j] = UB[i,j]
		else:
			count = count + 1

# ----------------------------------calling Matrix Completion----------

m,n = VC_removed.shape

u = []
v = []
vecM = []
vecEpsilon = []
for i in range(m):
  for j in range(n):
    if VCcopy[i,j]!=(-1):
      u.append(i)
      v.append(j)
      vecM.append(VCcopy[i,j])
      vecEpsilon.append(0)
    else: #if value ==-1
      u.append(i)
      v.append(j)
      vecM.append((LB[i,j]+UB[i,j])/2)
      vecEpsilon.append((UB[i,j]-LB[i,j])/2)




maxRank = n

u = np.asarray(u)
v = np.asarray(v)
vecM = np.asarray(vecM)
vecEpsilon = np.asarray(vecEpsilon)


U, E, VT, S, B  = sRPCAviaADMMFast.sRPCA(m,n,u,v,vecM,vecEpsilon,maxRank,SOff=True, rho=1, mu=0.01, maxIteration=100)

# RCP: I added some tests to make sure that S is not used
# assert np.all(S.todense()==0),'****DANGER****'
LHat = U*np.diag(E)*VT

# RCP: and that the bounds are respected.
# assert np.all(np.round(LHat) >= LB),'****DANGER****'
# # assert np.all(np.round(LHat) <= UB),'****DANGER****'

# np.savetxt('recovered_bound_20_nw3.txt', LHat)
# print ('BEFORE correction--------------')
# print (LHat[0,0:10])


# CORRECTION CODE:
for i in range(n):
	for j in range(n):
		if ((i == j) and (LHat[i,j] !=0)):
			# set the value to 0
			LHat[i,j] = 0
		elif i!=j:
			if LHat[i,j] < LB[i,j]:
				LHat[i,j] = LB[i,j] # set the value to lower bound
			elif LHat[i,j] > UB[i,j]:
				LHat[i,j] = UB[i,j] # set it to ubber bound
			else:
				LHat[i,j] = round( LHat[i,j] )


# measure mean error before correction--------------
# measure abs hop distance error before correction
# xx = mean error
# yy = abs hop distance error
# ee = std deviation


r,c = dHp.shape
hop = np.zeros((r*c))
ori = np.zeros((r*c))

p = 0
for i in range(r):
  for j in range(c):
    hop[p] = (LHat[i,j])  
    ori[p] = (dHp[i,j])
    p = p+1

x = np.round(hop-ori)
xx = (np.sum(abs(x)))/(np.sum(ori))
xx = xx*100
yy = (np.sum(abs(x)))/(r*c)
ee = np.std(abs(x))


# store the mean error values in file_mean

if fraction == 20:
  hs = open("file_mean.txt","a")
  hs.write(str('Iteration_1'))
  hs.write('\n')
  hs.write('20')
  hs.write('%')
  hs.write(' ')
  hs.write(format(xx))
  hs.close() 
elif fraction == 40:
  hs = open("file_mean.txt","a")
  hs.write('\n')
  hs.write('40')
  hs.write('%')
  hs.write(' ')
  hs.write(format(xx))
  hs.close() 
elif fraction == 60:
  hs = open("file_mean.txt","a")
  hs.write('\n')
  hs.write('60')
  hs.write('%')
  hs.write(' ')
  hs.write(format(xx))
  hs.close() 
elif fraction == 80:
  hs = open("file_mean.txt","a")
  hs.write('\n')
  hs.write('80')
  hs.write('%')
  hs.write(' ')
  hs.write(format(xx))
  hs.close() 
elif fraction == 90:
  hs = open("file_mean.txt","a")
  hs.write('\n')
  hs.write('90')
  hs.write('%')
  hs.write(' ')
  hs.write(format(xx))
  hs.write('\n')
  hs.write('\n')
  hs.close() 
  
  

# store the abs hop error  values in file_abs

if fraction == 20:
  hs = open("file_abs.txt","a")
  hs.write(str('Iteration_1'))
  hs.write('\n')
  hs.write('20')
  hs.write('%')
  hs.write(' ')
  hs.write(format(yy))
  hs.close() 
elif fraction == 40:
  hs = open("file_abs.txt","a")
  hs.write('\n')
  hs.write('40')
  hs.write('%')
  hs.write(' ')
  hs.write(format(yy))
  hs.close() 
elif fraction == 60:
  hs = open("file_abs.txt","a")
  hs.write('\n')
  hs.write('60')
  hs.write('%')
  hs.write(' ')
  hs.write(format(yy))
  hs.close() 
elif fraction == 80:
  hs = open("file_abs.txt","a")
  hs.write('\n')
  hs.write('80')
  hs.write('%')
  hs.write(' ')
  hs.write(format(yy))
  hs.close() 
elif fraction == 90:
  hs = open("file_abs.txt","a")
  hs.write('\n')
  hs.write('90')
  hs.write('%')
  hs.write(' ')
  hs.write(format(yy))
  hs.write('\n')
  hs.write('\n')
  hs.close() 



# print ('AFTER correction--------------')


# create a graph
G = nx.Graph()
adj = np.zeros((n,n))

for i in range(n):
    G.add_node(i)

r,c = LHat.shape
for i in range(r):
  for j in range(c):
    if LHat[i,j]==1:
      adj[i,j] = 1

for i in range(r):
    for j in range(c):
        if adj[i,j]==1: #detecting where there is an edge
            G.add_edge(i,j)

# calculate average clustering coefficient
C_value = nx.algorithms.average_clustering(G)
# calculate average node degree
A_value = sum(adj[:])
A_value = sum(A_value)
A_value = A_value/n


# exit()


# store the clustering values in file_C

if fraction == 20:
  hs = open("file_C.txt","a")
  hs.write(str('Iteration_1'))
  hs.write('\n')
  hs.write('20')
  hs.write('%')
  hs.write(' ')
  hs.write(format(C_value))
  hs.close() 
elif fraction == 40:
  hs = open("file_C.txt","a")
  hs.write('\n')
  hs.write('40')
  hs.write('%')
  hs.write(' ')
  hs.write(format(C_value))
  hs.close() 
elif fraction == 60:
  hs = open("file_C.txt","a")
  hs.write('\n')
  hs.write('60')
  hs.write('%')
  hs.write(' ')
  hs.write(format(C_value))
  hs.close() 
elif fraction == 80:
  hs = open("file_C.txt","a")
  hs.write('\n')
  hs.write('80')
  hs.write('%')
  hs.write(' ')
  hs.write(format(C_value))
  hs.close() 
elif fraction == 90:
  hs = open("file_C.txt","a")
  hs.write('\n')
  hs.write('90')
  hs.write('%')
  hs.write(' ')
  hs.write(format(C_value))
  hs.write('\n')
  hs.write('\n')
  hs.close() 


# store the average node degree values in file_A

if fraction == 20:
  hs = open("file_A.txt","a")
  hs.write(str('Iteration_1'))
  hs.write('\n')
  hs.write('20')
  hs.write('%')
  hs.write(' ')
  hs.write(format(A_value))
  hs.close() 
elif fraction == 40:
  hs = open("file_A.txt","a")
  hs.write('\n')
  hs.write('40')
  hs.write('%')
  hs.write(' ')
  hs.write(format(A_value))
  hs.close() 
elif fraction == 60:
  hs = open("file_A.txt","a")
  hs.write('\n')
  hs.write('60')
  hs.write('%')
  hs.write(' ')
  hs.write(format(A_value))
  hs.close() 
elif fraction == 80:
  hs = open("file_A.txt","a")
  hs.write('\n')
  hs.write('80')
  hs.write('%')
  hs.write(' ')
  hs.write(format(A_value))
  hs.close() 
elif fraction == 90:
  hs = open("file_A.txt","a")
  hs.write('\n')
  hs.write('90')
  hs.write('%')
  hs.write(' ')
  hs.write(format(A_value))
  hs.write('\n')
  hs.write('\n')
  hs.close() 


# store the non-exact count values in file_count

if fraction == 20:
  hs = open("file_count.txt","a")
  hs.write(str('Iteration_1'))
  hs.write('\n')
  hs.write('20')
  hs.write('%')
  hs.write(' ')
  hs.write(format(count))
  hs.close() 
elif fraction == 40:
  hs = open("file_count.txt","a")
  hs.write('\n')
  hs.write('40')
  hs.write('%')
  hs.write(' ')
  hs.write(format(count))
  hs.close() 
elif fraction == 60:
  hs = open("file_count.txt","a")
  hs.write('\n')
  hs.write('60')
  hs.write('%')
  hs.write(' ')
  hs.write(format(count))
  hs.close() 
elif fraction == 80:
  hs = open("file_count.txt","a")
  hs.write('\n')
  hs.write('80')
  hs.write('%')
  hs.write(' ')
  hs.write(format(count))
  hs.close() 
elif fraction == 90:
  hs = open("file_count.txt","a")
  hs.write('\n')
  hs.write('90')
  hs.write('%')
  hs.write(' ')
  hs.write(format(count))
  hs.write('\n')
  hs.write('\n')
  hs.close() 
