from time import time
from collections import Counter
from heapq import nsmallest
hosts = Counter()
begin = time()
for line_num, line in enumerate(open('../log_input/log.txt'),1):
  host = line.split(' ', 1)[0]
  hosts[host] -= 1 # -= instead of += is hack for lexicographic order
top_hosts = open('../log_output/hosts.txt', 'w')
for count, host in nsmallest(10, zip(hosts.values(), hosts)):
  print >>top_hosts, host+','+`-count`
del top_hosts
if line_num > 10**6: print 'hosts took %g seconds'%(time() - begin)
