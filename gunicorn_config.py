# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

timeout = 120

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

_logpath = 'gunicorn_logs/'
errorlog = _logpath + 'errors'
loglevel = 'info'
accesslog = _logpath + 'access'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
