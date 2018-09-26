#!/usr/bin/env python3

from datetime import datetime

f = open('web-access.log')
i = 0
ip_rating = {}
status_404_raiting = {}
minutes = [];
first_minute = [];
minute_index = 0;

for row in f.readlines():
	#row = input()
	i += 1	
	import re
	a = list(map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', row)))
	#print(a)
	
	remote_addr = ""
	time_local = ""
	upstream_status = ""

	if len(a) > 0 : remote_addr = a[0]
	if len(a) > 2 : time_local = a[2]
	if len(a) > 18 : upstream_status = a[18]
	#print(i, remote_addr, time_local, upstream_status)

	# ip adresses request rating	
	if( ip_rating.get(remote_addr) == None ) : ip_rating[remote_addr] = 0
	ip_rating[remote_addr] += 1
	#print(ip_rating[remote_addr])
	
	# ip status 404 rating	
	if( upstream_status == "404" ) :
		if( status_404_raiting.get(remote_addr) == None ) : status_404_raiting[remote_addr] = 0
		status_404_raiting[remote_addr] += 1
		#print(status_404_raiting[remote_addr])
	
	# requests per minute
	d = datetime.strptime(time_local, "%d/%b/%Y:%H:%M:%S %z")
	dt = d.timestamp()
	#print( datetime.utcfromtimestamp(dt) )
	if( i == 1 ) : first_minute = int(dt // 60)
	minute_index = int(dt // 60 - first_minute)
	if( len(minutes) <= minute_index ) : minutes.extend( [0] * (minute_index - len(minutes) + 1) )
	minutes[minute_index] += 1

# ip adresses request rating
print("\n#1")
print("TOP 5 IP adresses (adress / requests):")
b = []
for key, val in ip_rating.items() :
    temp = [key,val]
    b.append(temp)

b = sorted(b, key = lambda x: x[1], reverse = True)

for val in b[:5] :
	print(val[0], val[1])

# ip status 404 rating
print("\n#2")
print("TOP 1 IP got code 404 (adress / number of \"404\" responses):")
b = []
max_s404 = 0
max_s404_key = ""
for key, val in status_404_raiting.items() :
		if( val > max_s404 ) :
			max_s404 = val
			max_s404_key = key

print(max_s404_key, max_s404)
		
# requests per hour
print("\n#3")
print("the busiest hour:")
hour = 0

for val in minutes[:60] :
	hour += val

max_hour_start = 0
max_hour_rate = 0
hours = []
for i in range(60, len(minutes)) :
	#print(i, minutes[i])
	hour += minutes[i]
	hour -= minutes[i - 60]
	hours.append(hour)
	if( hour > max_hour_rate ) :
		max_hour_rate = hour
		max_hour_start = i
	
print(
"from", datetime.utcfromtimestamp( (first_minute + max_hour_start) * 60 ),
"till", datetime.utcfromtimestamp( (first_minute + max_hour_start + 60) * 60 ),
"processed", max_hour_rate, "- requests")

print()
