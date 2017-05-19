#Write code that outputs p after multiplying each entry 
#by pHit or pMiss at the appropriate places. Remember that
#the red cells 1 and 2 are hits and the other green cells
#are misses.


p=[0.2,0.2,0.2,0.2,0.2]
world=['green','red','red','green','green']
pHit = 0.6
pMiss = 0.2

_sum=0.0
for i in range(len(p)):
    p[i]*=(pMiss*(world[i]=='green')+pHit*(world[i]=='red'))
    _sum+=p[i]
print _sum


