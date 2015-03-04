import json
from pprint import pprint
import urllib
import httplib
import datetime, time
from pytz import timezone
import csv
import sys
import os
import argparse
import copy


#########################################
# API Parameters
#########################################
API_KEY = '09C43A9B270A470B8EB8F2946A9369F3'
host = 'api.topsy.com'
url = '/v2/content/tweets.json'

#########################################
# Time range for slot 21
#########################################
pacific = timezone('America/Los_Angeles')
start_date = datetime.datetime(2015,01,14)
end_date = datetime.datetime(2015,01,29)
mintime = int(time.mktime(start_date.timetuple()))
maxtime = int(time.mktime(end_date.timetuple()))

#########################################
# Send a query to Topsi API
# params: a dict for query paramaters
#########################################
def send_query(params):
	#########   set query parameters
	params = urllib.urlencode(params)

	keep_trying = True
	while keep_trying:
		try:
			#########   create and send HTTP request
			req_url = url + '?' + params
			req = httplib.HTTPConnection(host, timeout=10)
			req.putrequest("GET", req_url)
			req.putheader("Host", host)
			req.endheaders()
			req.send('')

			#########   get response and print out status
			resp = req.getresponse()

			if resp.status != 200:
				raise Exception('%s, %s' % (resp.status, resp.reason))

			#########   extract tweets
			resp_content = resp.read()
			ret = json.loads(resp_content)
			tweets = ret['response']['results']['list']
			keep_trying = False
		except:
			e = sys.exc_info()[0]
			print "ERROR: %s ... trying again" % e


	return tweets


#########################################
# Convert unix time stamps to Y-M-D H:M:S
#########################################
def timestamp_to_str(unix_timestamp, format='%Y-%m-%d %H:%M:%S'):
	return (
	    datetime.datetime.fromtimestamp(
	        int(unix_timestamp)
	    ).strftime(format)
	)

###########################################
# Question 1
# display the top 5 tweets (author, date,
# and tweet) given a search term or hashtag
# searches for the top 5 tweets for a given
# term returns them input: hashtag (str)
# output: list of the top five tweets as strings
###########################################
def top_5_tweets(term):

	params = {'apikey' : API_KEY,
              'q' :term,
              'include_metrics':'1',
              'limit': 5}

	tweets = send_query(params)
	for tweet in tweets:
		# pprint(tweet)
		print tweet['author']['name']
		print timestamp_to_str(tweet['citation_date'])
		print tweet['highlight'], '\n'

	with open('top_tweets.txt', 'w+') as f:
		for tweet in tweets:
			f.write(json.dumps(tweet) + '\n')

###########################################
# Question 2
# Get all tweets of any of the hashtags
# below in a specific time frame:
#
# *-------------------------------------*
# | #Seahawks  |  #Patriots             |
# | #GoHawks   |  #GoPatriots           |
# | #Halftime  |  #superbowlcommercials |
# |            |  #SuperBowlXLIX        |
# *-------------------------------------*
# pacific = timezone('America/Los_Angeles')
# start_date = datetime.datetime(2015,01,14, tzinfo=pacific)
# end_date = datetime.datetime(2015,01,29, tzinfo=pacific)
# mintime = int(time.mktime(start_date.timetuple()))
# maxtime = int(time.mktime(end_date.timetuple()))
###########################################
def get_all_tweets(hashtag):
	# time steps in seconds
	t_frame_size = datetime.timedelta(seconds=60)
	format = '%Y-%m-%d %H:%M:%S'

	start_frame = start_date
	end_frame = start_date + t_frame_size
	delta = end_date - end_frame

	while delta.days >= 0:
		t_frame_size = datetime.timedelta(seconds=60)
		mintime = int(time.mktime(start_frame.timetuple()))
		maxtime = int(time.mktime(end_frame.timetuple()))
		params = {'apikey' : API_KEY,
	              'q' :hashtag,
	              'include_metrics':'1',
	              'limit': 500,
	              'mintime': str(mintime),
	              'maxtime': str(maxtime)}
		tweets = send_query(params)

		while len(tweets)>=500 and (t_frame_size.seconds >= 5):
			print'''
WARNING reached maxmimum results.. adjusting time steps
			'''.strip()
			t_frame_size = t_frame_size - datetime.timedelta(seconds=5)

			end_frame = start_frame + t_frame_size

			mintime = int(time.mktime(start_frame.timetuple()))
			maxtime = int(time.mktime(end_frame.timetuple()))
			params = {'apikey' : API_KEY,
		              'q' :hashtag,
		              'include_metrics':'1',
		              'limit': 500,
		              'mintime': str(mintime),
		              'maxtime': str(maxtime)}
			tweets = send_query(params)

		# write json data to tweets.txt
		with open("tweets.txt", "a") as f:
			for tweet in tweets:
				f.write(json.dumps(tweet) + '\n')

		# write log to search_log.txt
		print "%-15sFrom: %-27sTo: %-27sNo. Of Results: %d" \
		      %(hashtag, start_frame.strftime(format),
		      	end_frame.strftime(format), len(tweets))
		with open("search_log.txt", "a") as f:
			f.write("%-15sFrom: %-27sTo: %-27sNo. Of Results: %d\n"
		           %(hashtag, start_frame.strftime(format),
		           end_frame.strftime(format), len(tweets)))

		# store data to data.csv to read it later for question 3
		data = [hashtag, mintime, maxtime, len(tweets)]
		with open("data.csv", 'a') as f:
			f_csv = csv.writer(f)
			f_csv.writerow(data)

		start_frame = end_frame
		end_frame = start_frame + t_frame_size
		delta = end_date - end_frame

###########################################
# Question 3
# To be added
###########################################
def _get_n_tweets(hashtag):
	file_name = [name for name in os.listdir('q3_data')
	             if name.startswith(hashtag)]
	print 'file name is %s' % file_name[0]
	print 'Reading file...'
	total_tweets = 0
	with open('q3_data/'+file_name[0]) as f:
		f_csv = csv.reader(f)
		for row in f_csv:
			total_tweets = total_tweets + int(row[3])
	print'--------------------'
	print'Total tweets for %s = %d' % (hashtag, total_tweets)
	print'--------------------\n'

def n_of_tweets_for_all_hashtags():
	hashtags = ['Seahawks','GoHawks', 'Patriots', 'GoPatriots', 'Halftime',
	            'superbowlcommercials', 'SuperBowlXLIX']
	for hashtag in hashtags:
		_get_n_tweets(hashtag)

def get_plot_data(hashtag):
	### data:  start_time, endtime, number of tweets
	file_name = [name for name in os.listdir('q3_data')
	             if name.startswith(hashtag)]
	data = []
	with open('q3_data/'+file_name[0]) as f:
		f_csv = csv.reader(f)
		for row in f_csv:
			start_time = datetime.datetime.fromtimestamp(int(row[1]))
			end_time = datetime.datetime.fromtimestamp(int(row[2]))
			s = timestamp_to_str(int(row[1]))
			e = timestamp_to_str(int(row[2]))
			n_of_tweets = int(row[3])
			# print '%-15s%-30s%-30s%-15d' % (hashtag, s, e, n_of_tweets)
			data.append((start_time, end_time, n_of_tweets))

	format = '%Y-%m-%d %H:%M:%S'
	i = 0
	from_t = data[i][0]
	count = data[i][2]
	end = data[0][0]
	tweets_per_time_step = []
	while i < len(data):
		while i <len(data) and (data[i][1]-from_t).seconds/3600<=3:
			count += data[i][2]
			to_t = data[i][1]
			if (to_t-from_t).seconds/3600==2:
				break
			i += 1
		# print (to_t-from_t).seconds/3600
		# print '%-30s %-30s %d' % (from_t.strftime(format), to_t.strftime(format),
		# 	                      count)
		tweets_per_time_step.append((from_t, to_t, count, count/(2.0*3600)))
		from_t = to_t
		count = 0

	headers = ['From', 'To', 'Total_tweets', 'Tweets_div_by_2hr']
	with open('Q5_plot_'+hashtag+'.csv','w') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(headers)
		f_csv.writerows(tweets_per_time_step)

###########################################
# Question 4
# To be added
###########################################
def process(hashtag):
	# initialize retweet counters
	retweet_counters = [0 for i in range(600)]

	with open('q2_data/'+hashtag+'_tweets.txt') as f:
		for line in f:
			tweet_info = json.loads(line)
			n_of_retweets = tweet_info['tweet']['retweet_count']
			retweet_counters[n_of_retweets] += 1

	rows = []
	for i, val in enumerate(retweet_counters):
		rows.append((i,val))
	headers = ['number_of_retweets', 'number_of_occurances']

	with open('Q4_plot_data.csv', 'w') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(headers)
		f_csv.writerows(rows)

###########################################
# Miscellaneous
# concatenate files for hw submission
###########################################
def concatenate_files():
	file_names = [name for name in os.listdir('q2_data')
	             if name.endswith('search_log.txt')]
	with open('q2_data/search_log.txt', 'w') as outfile:
	    for fname in file_names:
	        with open('q2_data/' + fname) as infile:
	            for line in infile:
	                outfile.write(line)

def pprint_json():
	data = []
	with open('q1_file.txt', 'r') as js_dat:
		for line in js_dat:
			# ret = json.loads(line)
			data.append(json.loads(line))

	with open('pprint_q1_file.txt', 'w+') as f:
		for dat in data:
			pprint(dat, f)
			f.write('\n-------------------------------------------------------\n\n')

if __name__ == '__main__':

	# Q1
	# top_5_tweets('#GoPatriots')

	# Q2
	# RUN ONE AT A TIME
	# get_all_tweets('#Seahawks')
	# get_all_tweets('#Patriots')
	# get_all_tweets('#GoHawks')
	# get_all_tweets('#GoPatriots')
	# get_all_tweets('#Halftime')
	# get_all_tweets('#superbowlcommercials')
	# get_all_tweets('#SuperBowlXLIX')

	# Q3
	# n_of_tweets_for_all_hashtags()
	# get_plot_data('Seahawks')

	# Q4
	# process('Seahawks')

	# Q5
	# get_plot_data('Patriots')

	# Q6
	# parser for a given file name to print tweet info based on optional criteria
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help="the name of the file containg the json data")
	parser.add_argument("--user", "-u", help="return tweets by USER")
	parser.add_argument("--date", "-d", help="return tweets on this date YYYY-MM-DD")
	parser.add_argument("--numOfRet", "-r", type=int, help="return tweets retweeted NUMOFRET times")
	parser.add_argument("--limit", "-l", type=int, default=10,
		                help="maxmimum number of results to print")
	args = parser.parse_args()
	args_dict = vars(copy.deepcopy(args))
	args_dict.pop('filename')
	args_dict.pop('limit')
	options = {(opt,val) for opt,val in args_dict.items() if val != None}
	options = dict(options)

	with open(args.filename, 'r') as f:
		limit = args.limit
		i = 0
		for line in f:
			if i >= limit:
				break
			tweet = json.loads(line)
			search = dict()
			search['user'] = tweet['author']['nick'].lower() == args.user.lower() if args.user!=None else ''
			search['date'] = timestamp_to_str(tweet['citation_date'], '%Y-%m-%d') == args.date \
			                 if args.date!=None else ''
			search['numOfRet'] = int(tweet['tweet']['retweet_count']) == int(args.numOfRet) \
			                     if args.numOfRet!=None else ''
			text = tweet['highlight'] + '\n'
			search = [value for key,value in search.items() if key in options]
			if all(search):
				print tweet['author']['nick']
				print timestamp_to_str(tweet['citation_date'])
				print 'Number of Retweets: ', tweet['tweet']['retweet_count']
				print tweet['highlight'], '\n'
				i += 1




