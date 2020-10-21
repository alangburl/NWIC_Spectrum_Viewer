import matplotlib.pyplot as plt

f=open('Back_Die_Away.csv','r')
data=f.readlines()
f.close()
time=[]
counts=[]

for i in range(75,len(data)):
    line=data[i].split(sep=',')
    if float(line[0])<20000:
        counts.append(float(line[0]))
        time.append(float(line[1].split(sep='\n')[0]))
plt.plot(time,counts)
plt.xlabel('Time(s)')
plt.ylabel('Count rate (cps)')
plt.savefig('Back.png',dpi=600)
plt.show()

