from calendar import timegm
from time import time, strptime
wrong_login = {}
blocked = open('../log_output/blocked.txt', 'w')
def parse_time(line): # slow, avoid calling needlessly
  when = line[1 + line.index('[') : line.index(']')]
  when = strptime(when, '%d/%b/%Y:%H:%M:%S -0400')
  return timegm(when)
begin = time() # poor man's benchmarking
for line_num, line in enumerate(open('../log_input/log.txt'),1):
  host = line.split(' ', 1)[0]
  if host in wrong_login:
    prev = wrong_login[host]
    if len(prev) == 3:
      when = parse_time(line)
      if when - prev[-1] < 5*60:
        print >> blocked, line[:-1]
        continue
      del wrong_login[host]
  req = line[line.index('"')+1 : line.rindex('"')]
  req = req.split()
  try: url = req[1]
  except IndexError: continue
  if url != '/login': continue
  response_code = line.rsplit(' ', 2)[-2]
  if host not in wrong_login:
    if response_code != 200:
      when = parse_time(line)
      wrong_login[host] = [when]
    continue
  if response_code == 200:
    del wrong_login[host]
    continue
  assert len(prev) in (1,2)
  when = parse_time(line)
  prev += [when]
  while when - prev[0] >= 20:
    del prev[0]
del blocked
if line_num > 10**6: print 'blocked took %g seconds'%(time() - begin)
