from calendar import timegm
from time import gmtime, strftime, time
months = '- Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
months = dict(zip(months, range(len(months))))
start = None # time of first event
busy = []
prev_time_str = None
prev_time_int = None
begin = time() # poor man's benchmarking
for line_num, line in enumerate(open('../log_input/log.txt'),1):
  when = line[line.index('[')+1 : line.index(']')]
  if when == prev_time_str:
    when = prev_time_int
  else:
    prev_time_str = when
    # DD/MON/YYYY:HH:MM:SS -0400
    # 0  3   7    c  f  i
    # 0123456789abcdefghi
    base36i = int('i',36)
    when = timegm(map(int, [
      when[7:7+4],
      months[when[3:3+3]],
      when[:2],
      when[0xc:0xc+2],
      when[0xf:0xf+2],
      when[base36i:base36i+2]
    ]))
    prev_time_int = when
  if start is None: start = when
  when = when - start
  busy += [0]*(when-len(busy)+1)
  busy[when] += 1
# if line_num > 10**6: print time() - begin
busiest = []
s = sum(busy[:3600])
busy += [0]*3600
for idx, x in enumerate(busy[:when]):
  busiest += [-s] # hack: use negative count for silly lexicographic sorting
  s = s - x + busy[idx+3600]
def to_string(when):
  return strftime('%d/%b/%Y:%H:%M:%S -0400', gmtime(when+start))
from heapq import nsmallest
most_busy = sorted(zip(busiest, map(to_string, range(len(busiest)))))
hours = open('../log_output/hours.txt', 'w')
for count, when in most_busy[:10]:
  print >>hours, when+','+`-count`
del hours
if line_num > 10**6: print 'hours took %g seconds'%(time() - begin)
