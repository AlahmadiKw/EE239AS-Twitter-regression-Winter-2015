import json
from pprint import pprint
# import urllib
# import httplib
import datetime, time
# from pytz import timezone
import csv
import sys
# import os
# import argparse
import copy
import os

#########################################
# Convert unix time stamps to Y-M-D H:M:S
#########################################
def t_to_str(unix_timestamp, format='%Y-%m-%d %H:%M:%S'):
	return (
	    datetime.datetime.fromtimestamp(
	        int(unix_timestamp)
	    ).strftime(format)
	)

#########################################
# Gets number of lines in file
#########################################
def file_len(fname):
    with open(fname, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#########################################
# convert Time to decimal
#########################################
def time_to_decimal(time_):
	format = '%H:%M:%S'
	t = time_.strftime(format)
	(h, m, s) = t.split(':')
	result = int(h) * 3600 + int(m) * 60 + int(s)
	return str(result)


#########################################
# Question 1
# creates a csv files containing stats for
# inputs:
#   hashtag: ex: '#gohawks'
#   time_bin: time granularity in seconds (size of time bins)
#########################################
def get_stats(hashtag, time_bin=3600, directory = 'ignore/tweet_data/'):
	print '---> Processing ' + hashtag
	format = '%Y-%m-%d %H:%M:%S'

	file_l = file_len(directory + '/' +hashtag)
	headers = ['from', 'to', 'twt_count', 'flwrs_count', 'ret_cnt', 'max_flwrs', 'date_hr', 'hr', 'favorite', 'momentum', 'accel', 'peak']
	# initialize file to store data
	with open('statistics_'+hashtag+'.csv', 'w') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(headers)

	with open(directory+ '/' +hashtag, 'r') as f:

		# load first tweet
		tweet = json.loads(f.readline())
		start_time = datetime.datetime.fromtimestamp(int(tweet['citation_date']))
		cnt = 1
		flwrs_cnt = int(tweet['author']['followers'])
		rt_cnt = int(tweet['metrics']['citations']['total'])
		max_flwrs= int(tweet['author']['followers'])
		favorite_count= int(tweet['tweet']['favorite_count'])
		momentum = int(tweet['metrics']['momentum'])
		accel = int(tweet['metrics']['acceleration'])
		peak = int(tweet['metrics']['peak'])

		flag = False
		i=0
		for line in f:
			tweet = json.loads(line)
			end_time = datetime.datetime.fromtimestamp(int(tweet['citation_date']))
			delta = end_time - start_time
			delta_sec = delta.days*86400.0 + delta.seconds # convert to seconds

			##### STATUS BAR ######
			sys.stdout.write('\r')
			sys.stdout.write("[%-20s] %.1f%%" % ('='*int((20.0/file_l)*i), 100.0/file_l*i))
			sys.stdout.flush()
			i += 1
			#######################

			# while within time bin, inc counters
			# else dump into global counters and reset local oens
			if delta_sec <=time_bin:
				cnt += 1
				flwrs_cnt += int(tweet['author']['followers'])
				rt_cnt += int(tweet['metrics']['citations']['total'])
				favorite_count += int(tweet['tweet']['favorite_count'])
				momentum += int(tweet['metrics']['momentum'])
				accel += int(tweet['metrics']['acceleration'])
				peak += int(tweet['metrics']['peak'])
				if (max_flwrs < int(tweet['author']['followers'])):
					max_flwrs = int(tweet['author']['followers'])
				pass
			else :
				# append data to file
				format = '%Y-%m-%d-%H-%M-%S'
				row = [start_time.strftime(format),
				       (start_time+datetime.timedelta(seconds=time_bin)).strftime(format),
				       cnt,
				       flwrs_cnt,
				       rt_cnt,
				       max_flwrs,
				       start_time.strftime('%Y-%m-%d-%H'),
				       start_time.strftime('%H'),
				       favorite_count,
				       momentum,
				       accel,
				       peak]
				with open('statistics_'+hashtag+'.csv', 'a') as f:
					f_csv = csv.writer(f)
					f_csv.writerow(row)
				# reset counters
				start_time = datetime.datetime.fromtimestamp(int(tweet['citation_date']))
				cnt = 1
				flwrs_cnt = int(tweet['author']['followers'])
				rt_cnt = int(tweet['metrics']['citations']['total'])
				max_flwrs = int(tweet['author']['followers'])
				favorite_count= int(tweet['tweet']['favorite_count'])
				momentum = int(tweet['metrics']['momentum'])
				accel = int(tweet['metrics']['acceleration'])
				peak = int(tweet['metrics']['peak'])
				pass
	print '\n---> Done!'


if __name__ == '__main__':
	# get_stats('#SuperBowl')
	# get_stats('#NFL')
	directory = 'ignore/test_data'
	files = os.listdir(directory)
	for f in files:
		get_stats(f, directory=directory)


