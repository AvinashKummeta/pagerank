import networkx as nx 
import matplotlib.pyplot as plt

# reading input from a file and store them in list

fo = open("adj_list","r+")
list = []
main_list = fo.readlines()
for line in main_list:
    int_list = [int(i) for i in line.split()] 
    del int_list[0]
    del int_list[-1]
    list.append(int_list)

length = len(list)

# adj_matrix used for calculating page rank 
#main_matrix used for calculating topic specific page rank

adj_matrix = [[0 for x in range(length)] for y in range(length)]
dup_matrix = [[0 for x in range(length)] for y in range(length)]
spec_matrix = [[0 for x in range(length)] for y in range(length)]
main_matrix = [[0 for x in range(length)] for y in range(length)]
for i in range(0,length):
       index = len(list[i])
       for j in list[i]:
            adj_matrix[j][i]=(1/index)
            dup_matrix[j][i]=(1/index)
            spec_matrix[j][i]=(1/index)
            main_matrix[j][i]=(1/index)*0.8

# making adj_matrix stochastic for handling deadends

for i in range(0,length):
    d=0 
    for j in range(0,length):
       d=d+adj_matrix[j][i] 
    if d==0 :
        for k in range(0,length):
            adj_matrix[k][i]=1/length
         

        
pg_matrix = [0 for x in range(length)]          #pg_matrix for page ranks
ex_matrix = [0 for x in range(length)]            
init_matrix = [0 for x in range(length)]        #init_matrix for topic specific page ranks

for i in range(0,length):
     pg_matrix[i] =1/length
     ex_matrix[i] = (1/length)*0.2    
     init_matrix[i] =1/length


#power iteration for calculating page rank
     
temp = [0 for x in range(length)]      
limit = 0                          
while limit<100:
    limit = limit+1
    for i in range(0,length):
        sum = 0
        for j in range(0,length):
            sum = sum + adj_matrix[i][j]*pg_matrix[j]
        sum = sum*0.8
        sum = sum+ex_matrix[i]
        temp[i] = sum
    min = 0
    for x in range(0,length):
        diff=temp[x]-pg_matrix[x]
        if(min<abs(diff)):
            min = abs(diff)      
    if(min<10**-9):
        break
    for k in range(0,length):
        pg_matrix[k] = temp[k]
    print("waiting.....")
#print(limit)




# for topic specific page rank--------------------------
# dfs for grouping the interconnected nodes
vis=[0 for i in range(length)]
li=[]
size=[0 for i in range(length)]
def dfs(x):
	vis[x]=1
	li.append(x)
	for i in range(length):
		if vis[i]==0 and main_matrix[x][i]>0:
			dfs(i) 
for i in range(length):
	if vis[i]==0:
		dfs(i)
		sz=len(li)
		for j in range(sz):
			size[li[j]]=sz
		li.clear()


for i in range(0,length):
    for j in range(0,length):
        if(spec_matrix[i][j]>0):
            spec_matrix[i][j]=(1/size[i])*0.2


for i in range(0,length):
     for j in range(0,length):
        main_matrix[i][j]=main_matrix[i][j]+spec_matrix[i][j]
            
#print("Topic Specific page rank")

#power iteration for calculating topic specific page rank
tempg = [0 for x in range(length)]     
iterate=0
while iterate<100:
    iterate= iterate+1
    for i in range(0,length):
        row_sum = 0
        for j in range(0,length):
            row_sum = row_sum + main_matrix[i][j]*init_matrix[j]       
        tempg[i] = row_sum                                          
    minimum = 0
    for x in range(0,length):
        diff=tempg[x]-init_matrix[x]
        if(minimum<abs(diff)):
            minimum = abs(diff)      
    if(minimum<10**-9):
        break
    for k in range(0,length):
        init_matrix[k] = tempg[k]
    print("waiting.....")
   

#------------------------------------------------------

# final values for page rank in pg_matrix and for topic specif page rank in init_matrix


list = [None]*length
for i in range(0,length):
      list[i]=[pg_matrix[i],i]

list1 = [None]*length
for i in range(0,length):
      list1[i]=[init_matrix[i],i]

# sorting page ranks 
for i in range(0,length):
    for j in range(i+1,length):
        if(list[i][0]<list[j][0]):
            temp1 = list[i]                 #list contains sorted page ranks
            list[i]=list[j]
            list[j]=temp1
        if(list1[i][0]<list1[j][0]):
            temp2 = list1[i]               #list1 contains sorted topc specific page ranks
            list1[i]=list1[j]
            list1[j]=temp2

print("Top 40 page rank")
for i in range(0,40):
    print(list[i])
    
print("Top 40 Topic Specific page rank")
for i in range(0,40):
    print(list1[i]) 


#print(list)
index = [None]*length
for i in range(0,length):
    index[i]=list[i][1]     

d_matrix = [0 for x in range(length)]    
for i in range(0,length):
    d_matrix[i]=pg_matrix[i]*10**6        


# directional graph for visualization  
g=nx.DiGraph() 
for i in range(0,100):
   g.add_node(list[i][1])   #adding nodes to the graph


   
for i in range(0,100):
    for j in range(0,100):
        
        if (dup_matrix[list[i][1]][list[j][1]] > 0):
            g.add_edge(list[j][1],list[i][1])                   #adding the edges between the nodes in the digraph   
print(nx.info(g))
nx.draw(g,node_size=d_matrix,arrows=True,with_labels=True)
plt.show()


