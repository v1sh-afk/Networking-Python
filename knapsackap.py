a=[[4,40],[5,25],[7,42],[3,12]]
for i in a:
    i.append(i[1]//i[0])
b=sorted(a,key=lambda x:x[2])
b.reverse()
max1=int(input("enter maximum capacity"))
weights=[]
item_list=[]
k=int(input("enter parameter"))
for i in range(k):
    m=int(input("enter item number"))
    weights.append(b[m-1][0])
    item_list.append(m)
max1-=sum(weights)
i=0
while max1>0 and i<=len(b)-1:
    if b[i][0]<=max1 and (i+1) not in item_list:
        item_list.append(i+1)
        max1=max1-b[i][0]
        i+=1
    else:
        i+=1
print('Items in sack: ',item_list)
