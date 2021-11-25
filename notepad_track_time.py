import sys
import re
import datetime

from typing import List

def parse_time(lines: List[str] = ['']):
    # 4 types of lines:
    # 1. start with # -> comment lines
    # 2. start with number -> time tracking NOTE: assuming number == time tracking
    # 3. start with text before time line -> title
    # 4. empty lines
    total_time = datetime.timedelta()
    for l in lines:
        if len(l) == 0:
            pass
        elif l[0] == '#':
            pass
        elif l[0].isdigit():
            # figure out which format
            if '/' in l: #notepad format
                pattern = re.compile('(\d{1,2})(:\d{2} [AP]M \d{2}/\d{2}/\d{4}) (\d{1,2})(:\d{2} [AP]M \d{2}/\d{2}/\d{4})( /\d)?')
                result = pattern.findall(l) #list of 2-ples
                assert len(result) == 1, f'Error: Too few or too many timestamps in notepad format!, f{l}'
                result = result[0]
                s_hh, e_hh = result[0], result[2]
                start, end = result[0]+result[1], result[2]+result[3]
                divider = 1
                if result[4] != '': divider = int(result[4].split('/')[-1])
                # need to have HH format
                if len(s_hh) == 1: start = '0'+start
                if len(e_hh) == 1: end = '0'+end
                # parse into datetime objects and calculate delta
                start = datetime.datetime.strptime(start, "%I:%M %p %m/%d/%Y")
                end = datetime.datetime.strptime(end, "%I:%M %p %m/%d/%Y")
                duration = (end - start).total_seconds() // divider
                total_time +=  datetime.timedelta(seconds=duration)
            # elif ' ' in l: #2-digit start-end format #TODO:
            else: #duration only format
                if 'm' not in l:
                    print('NOTE: Assuming duration only format',file=sys.stderr)
                #TODO track time subject
                #NOTE just using first number
                result = re.findall(r'\d+', l)
                total_time += datetime.timedelta(minutes=int(result[0]))
        else:
            pass
    return total_time


lines = []
with open(sys.argv[1], 'r') as filehandle:
    lines = filehandle.readlines()
lines = [l.strip() for l in lines]
print(parse_time(lines))
