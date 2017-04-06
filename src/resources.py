from collections import Counter
from time import time
pages = Counter()
bad_requests = []
begin = time() # poor man's benchmarking
for line_num, line in enumerate(open('../log_input/log.txt'),1):
  req = line[line.index('"')+1 : line.rindex('"')]
  req = req.split()
  try: url = req[1]
  except IndexError:
    bad_requests += [line]
    continue
  num_bytes = line.rsplit(' ',1)[-1]
  num_bytes = int(num_bytes) if num_bytes != '-\n' else 0
  pages[url] -= num_bytes # -= instead of += is hack to get lexicographic order
if line_num == 4400644: assert len(bad_requests) == 5
most_bytes = open('../log_output/resources.txt', 'w')
for tot_bytes, page in sorted(zip(pages.values(), pages))[:10]:
  print >>most_bytes, page
del most_bytes
if line_num > 10**6: print 'resources took %g seconds'%(time() - begin)
