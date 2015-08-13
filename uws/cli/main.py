#!/usr/bin/env python

import sys, os
import getpass

from uws.UWS import connection as UWSconnection
from uws.UWS import base as UWSbase
from uws.UWS.base import UWSerror
#from lib import texttable as tt
from uws.lib.terminalsize import terminalsize as console
import texttable as tt
import argparse

debug = False

def listJobs(url, usr, pwd, bitmask):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)

	try:
		jobs = UWS.getJobList()
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise

	rows = [["ID", "Job name", "Status"]]
	for job in jobs.jobref:
		if bitmask == 0:
			_registerJobrefForTable(rows, job)
		if bitmask & 1:
			if 'COMPLETED' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 2:
			if 'PENDING' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 4:
			if 'QUEUED' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 8:
			if 'EXECUTING' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 16:
			if 'ERROR' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 32:
			if 'ABORTED' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 64:
			if 'UNKNOWN' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 128:
			if 'HELD' in job.phase:
				_registerJobrefForTable(rows, job)
				continue
		if bitmask & 256:
			if 'SUSPENDED' in job.phase:
				_registerJobrefForTable(rows, job)

	(conWidth, conHeight) = console.get_terminal_size()

	table = tt.Texttable(max_width=conWidth)
	table.set_deco(tt.Texttable.HEADER)
	table.set_cols_dtype(['t', 't', 't'])
	table.add_rows(rows)

	print "List of jobs on UWS service for user: '%s'" % usr
	print table.draw()
	print "%d jobs listed." % (len(rows)-1)

def _registerJobrefForTable(rows, job):
	jobId = job.reference.href.rsplit("/", 1)

	rows.append([jobId[1], job.id, ', '.join(job.phase)])

def showJob(url, usr, pwd, id):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)

	try:
		job = UWS.getJob(id)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise

	_printJob(job)

def newJob(url, usr, pwd, params={}, run=False):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)

	try:
		job = UWS.newJob(params)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise


	if run == True:
		#execute the job
		try:
			job = UWS.runJob(job.jobId)
		except UWSerror, e:
			if debug == False:
				print "An error occurred:\n   %s" % e.msg
				return
			else:
				print e.raw
				raise

	(conWidth, conHeight) = console.get_terminal_size()

	_printJob(job)

	print "\n"
	print "*" * (conWidth - 1)
	print "You can access this job with the id:\n"
	print "Job ID: %s" % job.jobId
	print "Command: uws -H %s --user=%s --password=YOUR_PASSWORD_HERE job show %s" % (url, usr, job.jobId)
	print "*" * (conWidth - 1)

def setParamsJob(url, usr, pwd, id, params={}):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)

	if len(params) == 0:
		try:
			job = UWS.getJob(id)
		except UWSerror, e:
			if debug == False:
				print "An error occurred:\n   %s" % e.msg
				return
			else:
				print e.raw
				raise
	else:
		try:
			job = UWS.setParamsJob(id, params)
		except UWSerror, e:
			if debug == False:
				print "An error occurred:\n   %s" % e.msg
				return
			else:
				print e.raw
				raise

	_printJob(job)


def runJob(url, usr, pwd, id):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)
	try:
		job = UWS.runJob(id)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise

	_printJob(job)

def abortJob(url, usr, pwd, id):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)
	try:
		job = UWS.abortJob(id)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise

	_printJob(job)

def deleteJob(url, usr, pwd, id):
	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)
	try:
		success = UWS.deleteJob(id)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise

	if success == True:
		print "Job %s successfully deleted!" % (id)

def resultsJob(url, usr, pwd, id, resultId, userfilebasename):
	def printProgress(totalSize, current):
		if totalSize == None:
			sys.stdout.write("\rDownloaded %d bytes" %current)    # or print >> sys.stdout, "\r%d%%" %i,
			sys.stdout.flush()
		else:
			sys.stdout.write("\r%d bytes" %current)    # or print >> sys.stdout, "\r%d%%" %i,
			sys.stdout.flush()

	UWSconn = UWSconnection.connection(url, usr, pwd)
	UWS = UWSbase.base(UWSconn)
	try:
		job = UWS.getJob(id)
	except UWSerror, e:
		if debug == False:
			print "An error occurred:\n   %s" % e.msg
			return
		else:
			print e.raw
			raise


	# if there are multiple result sets returned: force user to decide which ones to use?
	# or maybe rather let the service define a standard result? but how?
	if len(job.results) > 1 and resultId == None:
		print 'There are multiple results for this job, all of them are downloaded now.'
		print 'If this is not what you intended, please specify the id of your desired result like this: '
		print '\nuws job results ID RESULTID\n'
		print 'For RESULTID, you can choose from: ', ','.join([result.id for result in job.results])

		# return

	# set file base name to jobId or tablename (if available) or user provided filebasename
	filebasename = job.jobId
	for parameter in job.parameters:
		if parameter.id == 'table':
			filebasename = parameter.value
			break
			
	if userfilebasename != None:
		filebasename = userfilebasename

	retrievedSomething = False
	for result in job.results:
		if resultId == None or resultId == result.id:

			filename = filebasename + '.' + result.id 

			url = str(result.reference)

			print "Downloading %s into file '%s'" % (result.id, filename)
			UWSconn.downloadFile(url, usr, pwd, filename, callback=printProgress)
			print ""
			print "Finished downloading file '%s'\n" % (filename)
			retrievedSomething = True

	if not retrievedSomething:
		if resultId == None:
			print "The job with id '%s' has no results." % (job.jobId)
			print "Check with 'uws job show %s' the details, the job results may have been deleted." % (job.jobId)
		else:
			print "Result Id '%s' not available. Use 'uws job show %s' for a list of available results." % (resultId, job.jobId)

def _printJob(job):
	#format stuff
	rows = [["Field", "Value"]]
	rows.append(["Job id", job.jobId])

	if(job.runId):
		rows.append(["UWS run id", job.runId])

	rows.append(["Owner id", job.ownerId])
	rows.append(["Phase", ", ".join(job.phase)])

	if(job.quote):
		rows.append(["Quote", job.quote])

	rows.append(["Start time", job.startTime])
	rows.append(["End time", job.endTime])
	rows.append(["Execution duration", job.executionDuration])
	rows.append(["Destruction time", job.destruction])

	for param in job.parameters:
		rows.append(["Parameter " + param.id, param.value])

	for result in job.results:
		rows.append(["Result " + result.id, result.reference])

	try:
		if(job.errorSummary):
			rows.append(["Errors", "; ".join(job.errorSummary.messages)])
	except:
		pass

	for info in job.jobInfo:
		rows.append(["Job info", unicode(info)])

	(conWidth, conHeight) = console.get_terminal_size()

	fields = [row[0] for row in rows]   
	maxFieldLen = len(max(fields, key=len))

	table = tt.Texttable(max_width=conWidth)
	table.set_deco(tt.Texttable.HEADER)
	table.set_cols_dtype(['t', 't'])
	table.set_cols_width([maxFieldLen, conWidth - maxFieldLen - 4])
	table.add_rows(rows)
	print table.draw()

#checks validity of arguments and returns a list of arguments
def _checkJobParameterArgs(args):
	argsList = {}
	for arg in args:
		#valid arguments are of the form <paramter>=<value>
		currArgPair = arg.split("=", 1)
		if len(currArgPair) != 2:
			raise RuntimeError('Malformatted parameter found: %s' % (", ".join(currArgPair)))

		if currArgPair[0].lower() == "destruction":
			currArgPair[0] = "destruction"

		if currArgPair[0].lower() == "executionduration":
			currArgPair[0] = "executionDuration"

		argsList[currArgPair[0]] = currArgPair[1]

	return argsList

def main():
	parser = argparse.ArgumentParser(prog='uws')
	parser.add_argument('-H', '--host', help='URL to UWS service', required=True)
	parser.add_argument('-U', '--user', help='user name')
	parser.add_argument('--password', help='password')
	parser.add_argument('-P', action='store_true', help='hidden password (type at prompt)')
	parser.add_argument('-D', '--dbg', action='store_true', help='debug mode')

	subparsers = parser.add_subparsers(dest='command', help='commands for UWS')

	parser_list = subparsers.add_parser('list', help='list all jobs on the UWS service')
	parser_list.add_argument('-c', '--completed', action='store_true', help='show completed jobs')
	parser_list.add_argument('-p', '--pending', action='store_true', help='show pending jobs')
	parser_list.add_argument('-q', '--queued', action='store_true', help='show queued jobs')
	parser_list.add_argument('-e', '--executing', action='store_true', help='show executing jobs')
	parser_list.add_argument('-E', '--error', action='store_true', help='show jobs with errors')
	parser_list.add_argument('-a', '--aborted', action='store_true', help='show aborted jobs')
	parser_list.add_argument('--unknown', action='store_true', help='show unknown state jobs')
	parser_list.add_argument('--held', action='store_true', help='show held jobs')
	parser_list.add_argument('--suspended', action='store_true', help='show suspended jobs')

	parser_job = subparsers.add_parser('job', help='access a given job on the UWS service')

	jobSubparsers = parser_job.add_subparsers(dest='jobCommand', help='commands for manipulating jobs')
	parser_job_show = jobSubparsers.add_parser('show', help='show the specific job')
	parser_job_show.add_argument('id', help='job id')

	parser_job_new = jobSubparsers.add_parser('new', help='create a new job')
	parser_job_new.add_argument('-r', '--run', action='store_true', help='immediately submits the job on creation')
	parser_job_new.add_argument('jobParams', nargs='*', help='unspecified list of UWS service parameters in the form' + 
															' "<parameter>=<value>" - ' + 
															'Default parameters are: ' +
															'destruction (Destruction time of the job), ' + 
															'executionDuration (Execution duration of the job in seconds)')

	parser_job_set = jobSubparsers.add_parser('set', help='set parameters for the specific job')
	parser_job_set.add_argument('id', help='job id')
	parser_job_set.add_argument('jobParams', nargs='*', help='unspecified list of UWS service parameters in the form' + 
															' "<parameter>=<value>" - ' + 
															'Default parameters are: ' +
															'destruction (Destruction time of the job), ' + 
															'executionDuration (Execution duration of the job in seconds)')

	parser_job_run = jobSubparsers.add_parser('run', help="run the specific job if its state is pending")
	parser_job_run.add_argument('id', help='job id')

	parser_job_abort = jobSubparsers.add_parser('abort', help="aborts the execution of a specific job")
	parser_job_abort.add_argument('id', help='job id')

	parser_job_abort = jobSubparsers.add_parser('delete', help="delete a specific job")
	parser_job_abort.add_argument('id', help='job id')

	parser_job_results = jobSubparsers.add_parser('results', help="download results of a specific job")
	parser_job_results.add_argument('id', help='job id')
	parser_job_results.add_argument('resultid', nargs='?', help='result id (e.g. for specifying the format, optional)')
	parser_job_results.add_argument('-f', '--filebasename', help='basename of output file (optional), will be appended with resultid')

	args = parser.parse_args()

	if args.dbg == True:
		debug = True

	if args.P == True:
		if args.password != None:
			print "Error: You cannot use -P and --password together!"
			sys.exit(1)

		args.password = getpass.getpass("Enter password: ")

	if args.command == "list":
		bitmask = 0
		if args.completed:
			bitmask = bitmask | 1
		if args.pending:
			bitmask = bitmask | 2
		if args.queued:
			bitmask = bitmask | 4
		if args.executing:
			bitmask = bitmask | 8
		if args.error:
			bitmask = bitmask | 16
		if args.aborted:
			bitmask = bitmask | 32
		if args.unknown:
			bitmask = bitmask | 64
		if args.held:
			bitmask = bitmask | 128
		if args.suspended:
			bitmask = bitmask | 256

		listJobs(args.host, args.user, args.password, bitmask)

	if args.command == "job":
		if args.jobCommand == "show":
			showJob(args.host, args.user, args.password, args.id)
		elif args.jobCommand == "new":
			#parse the job parameters and store in argument list
			jobParamsList = _checkJobParameterArgs(args.jobParams)

			newJob(args.host, args.user, args.password, jobParamsList, args.run)
		elif args.jobCommand == "set":
			#parse the job parameters and store in argument list
			jobParamsList = _checkJobParameterArgs(args.jobParams)

			setParamsJob(args.host, args.user, args.password, args.id, jobParamsList)
		elif args.jobCommand == "run":
			runJob(args.host, args.user, args.password, args.id)
		elif args.jobCommand == "abort":
			abortJob(args.host, args.user, args.password, args.id)
		elif args.jobCommand == "delete":
			deleteJob(args.host, args.user, args.password, args.id)
		elif args.jobCommand == "results":
			resultsJob(args.host, args.user, args.password, args.id, args.resultid, args.filebasename)
		else:
			print "Error: Unknown command %s\n" % (args.jobCommand)

if __name__ == '__main__':
	main()
