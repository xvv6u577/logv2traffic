import sys, getopt
from datetime import datetime

from util.check_db_util import get_days_stats, get_users_info, between_days_stats
from util.byte_converter import get_printable_size

def echo_stats(info = [], time_from = 0, time_to = 0):
  print('\nFrom', datetime.utcfromtimestamp(time_from).strftime('%Y-%m-%d %H:%M:%S'),\
    'to', datetime.utcfromtimestamp(time_to).strftime('%Y-%m-%d %H:%M:%S'),'\n')
  i = 1
  for item in info:
    print('[{:2s}]: {:15s} uplink {:10s}, downlink {:10s}'.format(str(i), item['user'], \
      get_printable_size(item['uplink']), get_printable_size(item['downlink'])))
    i += 1

def entry():
  try:
    # short option with options that require an argument followed ':', like 'o:'
    # long option with options that require an argument followed '=', like "out-file="
    opts, args = getopt.getopt(sys.argv[1:], 'ld:uf:t:', ['list-users', 'days=', 'users', 'from=', 'to='])

  except getopt.GetoptError as err:
    print("Error: ", str(err))
    sys.exit(2)

  from_moment = 0
  to_moment = 0

  for opt, arg in opts:
    if opt in ("-l", "--list-users"):
      info, time_from, time_to = get_days_stats()
      echo_stats(info, time_from, time_to)
      sys.exit()

    elif opt in ("-d", "--days"):
      info, time_from, time_to = get_days_stats(int(arg))
      echo_stats(info, time_from, time_to)
      sys.exit()
    elif opt in ("-u", "--users"):
      infos = get_users_info()
      i = 1
      for user_info in infos:
        record_start = ''
        if 0 != user_info['timestamp']:
          record_start = datetime.utcfromtimestamp(user_info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        print('[{:2s}]: {:15s} {:20s}'.format(str(i), user_info['user'], record_start))
        i += 1
      sys.exit()
    elif opt in("-f", "--from"):
      from_moment = int(arg)
    elif opt in("-t", "--to"):
      to_moment = int(arg)
  
  if from_moment and to_moment:
    infos = between_days_stats(from_moment, to_moment)
    echo_stats(infos, from_moment, to_moment)

  # print(opts, args)

if __name__ == "__main__":
  entry()