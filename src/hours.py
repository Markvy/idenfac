from time import gmtime, strftime, time
begin = time() # poor man's benchmarking
from calendar import timegm
months = '- Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
months = dict(zip(months, range(len(months))))
def extract_time(line):
  return line[line.index('[')+1 : line.index(']')]
def parse_time(when):
  # DD/MON/YYYY:HH:MM:SS -0400
  # 0  3   7    c  f  i
  # 0123456789abcdefghi
  base36i = int('i',36)
  return timegm(map(int, [
    when[7:7+4],
    months[when[3:3+3]],
    when[:2],
    when[0xc:0xc+2],
    when[0xf:0xf+2],
    when[base36i:base36i+2]
  ]))
log_file_name = '../log_input/log.txt'
for line in open(log_file_name):
  when = extract_time(line)
  start = parse_time(when) # time of first event
  start_month = when[3:7+4]
  break
log = open(log_file_name)
try: log.seek(-512, 2) # assume no line longer than 0.5KB; true for the 426 MB log
except IOError: pass # file is less than half a kilobyte; whatever
for line in log: pass
del log
total_seconds = 1 + parse_time(extract_time(line)) - start
seconds = [0]*total_seconds # seconds[i] == # of requests during "i"th second
prev_time_str = None
prev_time_int = None
for line_num, line in enumerate(open(log_file_name),1):
  when = extract_time(line)
  if when == prev_time_str:
    when = prev_time_int
  else:
    prev_time_str = when
    when = parse_time(when)
    prev_time_int = when
  when = when - start
  seconds[when] += 1
stop_month = prev_time_str[3:7+4] # final month + year
hours = [] # hours[i] # of requests during hour that begins at "i"th second
s = sum(seconds[:3600])
seconds += [0]*3600
for idx in range(when+1):
  hours += [-s] # hack: use negative count for silly lexicographic sorting
  x = seconds[idx]
  y = seconds[idx + 3600]
  s = s - x + y
def to_str(when):
  return strftime('%d/%b/%Y:%H:%M:%S -0400', gmtime(when+start))
tie_break = range(len(hours))
if start_month != stop_month:
  tie_break = map(to_str, tie_break)
from heapq import nsmallest
hours_txt = open('../log_output/hours.txt', 'w')
for count, when in nsmallest(10, zip(hours, tie_break)):
  if type(when) is int: when = to_str(when)
  print >>hours_txt, when+','+`-count`
del hours_txt
if line_num > 10**6: print 'hours took %g seconds'%(time() - begin)
