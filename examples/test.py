import krakenex
import time

k = krakenex.API()

#print(k.query_public('Depth',{'pair': 'XETHXXBT', 'count': '10'}))

a = k.query_public('Depth',{'pair': 'XETHXXBT', 'count': '4'})
print(a)
cycles = 0
    # Loop until we reach 20 minutes running
while cycles != 200:
    time.sleep(2)
    print (">>>>>>>>>>>>>>>>>>>>>", cycles)
    a = k.query_public('Depth',{'pair': 'XETHXXBT', 'count': '2'})
    print(a)
    # Sleep for 2 seconds
    
    # Increment the cycle count total
    cycles += 1
    # Bring up the dialog box here