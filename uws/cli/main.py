# -*- coding: utf-8 -*-
import argparse
import getpass
import sys

import texttable as tt
from uws.lib.terminalsize import terminalsize as console

from uws import UWS

debug = False


def list_jobs(url, user_name, password, bitmask):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)

    try:
        jobs = uws_client.get_job_list()
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    rows = [["ID", "Job name", "Status"]]
    for job in jobs.job_reference:
        if bitmask == 0:
            _register_job_reference_for_table(rows, job)
        if bitmask & 1:
            if 'COMPLETED' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 2:
            if 'PENDING' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 4:
            if 'QUEUED' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 8:
            if 'EXECUTING' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 16:
            if 'ERROR' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 32:
            if 'ABORTED' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 64:
            if 'UNKNOWN' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 128:
            if 'HELD' in job.phase:
                _register_job_reference_for_table(rows, job)
                continue
        if bitmask & 256:
            if 'SUSPENDED' in job.phase:
                _register_job_reference_for_table(rows, job)

    (console_width, console_height) = console.get_terminal_size()

    table = tt.Texttable(max_width=console_width)
    table.set_deco(tt.Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.add_rows(rows)

    print "List of jobs on UWS service for user: '%s'" % user_name
    print table.draw()
    print "%d jobs listed." % (len(rows) - 1)


def _register_job_reference_for_table(rows, job):
    job_id = job.reference.href.rsplit("/", 1)

    rows.append([job_id[1], job.id, ', '.join(job.phase)])


def show_job(url, user_name, password, id):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)

    try:
        job = uws_client.get_job(id)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    _print_job(job)


def new_job(url, user_name, password, parameters={}, run=False):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)

    try:
        job = uws_client.new_job(parameters)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    if run:
        # execute the job
        try:
            job = uws_client.run_job(job.job_id)
        except UWS.UWSerror as e:
            if not debug:
                print "An error occurred:\n   %s" % e.msg
                return
            else:
                print e.raw
                raise

    (console_width, console_height) = console.get_terminal_size()

    _print_job(job)

    print "\n"
    print "*" * (console_width - 1)
    print "You can access this job with the id:\n"
    print "Job ID: %s" % job.job_id
    print "Command: uws -H %s --user=%s --password=YOUR_PASSWORD_HERE job show %s" % (url, user_name, job.job_id)
    print "*" * (console_width - 1)


def set_parameters_job(url, user_name, password, id, parameters={}):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)

    if len(parameters) == 0:
        try:
            job = uws_client.get_job(id)
        except UWS.UWSerror as e:
            if not debug:
                print "An error occurred:\n   %s" % e.msg
                return
            else:
                print e.raw
                raise
    else:
        try:
            job = uws_client.set_parameters_job(id, parameters)
        except UWS.UWSerror as e:
            if not debug:
                print "An error occurred:\n   %s" % e.msg
                return
            else:
                print e.raw
                raise

    _print_job(job)


def run_job(url, user_name, password, id):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)
    try:
        job = uws_client.run_job(id)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    _print_job(job)


def abort_job(url, user_name, password, id):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)
    try:
        job = uws_client.abort_job(id)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    _print_job(job)


def delete_job(url, user_name, password, id):
    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)
    try:
        success = uws_client.delete_job(id)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    if success:
        print "Job %s successfully deleted!" % (id)


def results_job(url, user_name, password, id, result_id, user_file_base):
    def print_progress(total_size, current):
        if total_size:
            sys.stdout.write("\r%d bytes" % current)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
        else:
            sys.stdout.write("\rDownloaded %d bytes" % current)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()

    uws_connection = UWS.connection.Connection(url, user_name, password)
    uws_client = UWS.base.BaseUWSClient(uws_connection)
    try:
        job = uws_client.get_job(id)
    except UWS.UWSerror as e:
        if not debug:
            print "An error occurred:\n   %s" % e.msg
            return
        else:
            print e.raw
            raise

    # if there are multiple result sets returned: force user to decide which ones to use?
    # or maybe rather let the service define a standard result? but how?
    if len(job.results) > 1 and not result_id:
        print 'There are multiple results for this job, all of them are downloaded now.'
        print 'If this is not what you intended, please specify the id of your desired result like this: '
        print '\nuws job results ID RESULTID\n'
        print 'For RESULTID, you can choose from: ', ','.join([result.id for result in job.results])

    # set file base name to job_id or tablename (if available) or user provided file_base
    file_base = job.job_id
    for parameter in job.parameters:
        if parameter.id == 'table':
            file_base = parameter.value
            break

    if user_file_base:
        file_base = user_file_base

    retrieved = False
    for result in job.results:
        if not result_id or result_id == result.id:

            filename = file_base + '.' + result.id

            url = str(result.reference)

            print "Downloading %s into file '%s'" % (result.id, filename)
            uws_connection.download_file(url, user_name, password, filename, callback=print_progress)
            print ""
            print "Finished downloading file '%s'\n" % (filename)
            retrieved = True

    if not retrieved:
        if result_id:
            print "Result Id '%s' not available. Use 'uws job show %s' for a list of available results." % (result_id, job.job_id)
        else:
            print "The job with id '%s' has no results." % (job.job_id)
            print "Check with 'uws job show %s' the details, the job results may have been deleted." % (job.job_id)


def _print_job(job):
    # format stuff
    rows = [["Field", "Value"]]
    rows.append(["Job id", job.job_id])

    if(job.run_id):
        rows.append(["UWS run id", job.run_id])

    rows.append(["Owner id", job.owner_id])
    rows.append(["Phase", ", ".join(job.phase)])

    if(job.quote):
        rows.append(["Quote", job.quote])

    rows.append(["Start time", job.start_time])
    rows.append(["End time", job.end_time])
    rows.append(["Execution duration", job.execution_duration])
    rows.append(["Destruction time", job.destruction])

    for param in job.parameters:
        rows.append(["Parameter " + param.id, param.value])

    for result in job.results:
        rows.append(["Result " + result.id, result.reference])

    try:
        if(job.error_summary):
            rows.append(["Errors", "; ".join(job.error_summary.messages)])
    except:
        pass

    for info in job.job_info:
        rows.append(["Job info", unicode(info)])

    (console_width, console_height) = console.get_terminal_size()

    fields = [row[0] for row in rows]
    max_field_len = len(max(fields, key=len))

    table = tt.Texttable(max_width=console_width)
    table.set_deco(tt.Texttable.HEADER)
    table.set_cols_dtype(['t', 't'])
    table.set_cols_width([max_field_len, console_width - max_field_len - 4])
    table.add_rows(rows)
    print table.draw()


# checks validity of arguments and returns a list of arguments
def _check_job_parameter_args(arguments):
    argument_list = {}
    for argument in arguments:
        # valid arguments are of the form <paramter>=<value>
        argument_pair = argument.split("=", 1)
        if len(argument_pair) != 2:
            raise RuntimeError('Malformatted parameter found: %s' % (", ".join(argument_pair)))

        if argument_pair[0].lower() == "destruction":
            argument_pair[0] = "destruction"

        if argument_pair[0].lower() == "executionduration":
            argument_pair[0] = "executionDuration"

        argument_list[argument_pair[0]] = argument_pair[1]

    return argument_list


def main():
    global debug
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

    job_subparsers = parser_job.add_subparsers(dest='job_command', help='commands for manipulating jobs')
    parser_job_show = job_subparsers.add_parser('show', help='show the specific job')
    parser_job_show.add_argument('id', help='job id')

    parser_job_new = job_subparsers.add_parser('new', help='create a new job')
    parser_job_new.add_argument('-r', '--run', action='store_true', help='immediately submits the job on creation')
    parser_job_new.add_argument('job_parameters', nargs='*', help='unspecified list of UWS service parameters in the form' +
                                                                  ' "<parameter>=<value>" - ' +
                                                                  'Default parameters are: ' +
                                                                  'destruction (Destruction time of the job), ' +
                                                                  'executionDuration (Execution duration of the job in seconds)')

    parser_job_set = job_subparsers.add_parser('set', help='set parameters for the specific job')
    parser_job_set.add_argument('id', help='job id')
    parser_job_set.add_argument('job_parameters', nargs='*', help='unspecified list of UWS service parameters in the form' +
                                                                  ' "<parameter>=<value>" - ' +
                                                                  'Default parameters are: ' +
                                                                  'destruction (Destruction time of the job), ' +
                                                                  'executionDuration (Execution duration of the job in seconds)')

    parser_job_run = job_subparsers.add_parser('run', help="run the specific job if its state is pending")
    parser_job_run.add_argument('id', help='job id')

    parser_job_abort = job_subparsers.add_parser('abort', help="aborts the execution of a specific job")
    parser_job_abort.add_argument('id', help='job id')

    parser_job_abort = job_subparsers.add_parser('delete', help="delete a specific job")
    parser_job_abort.add_argument('id', help='job id')

    parser_job_results = job_subparsers.add_parser('results', help="download results of a specific job")
    parser_job_results.add_argument('id', help='job id')
    parser_job_results.add_argument('result_id', nargs='?', help='result id (e.g. for specifying the format, optional)')
    parser_job_results.add_argument('-f', '--file_base', help='basename of output file (optional), will be appended with result_id')

    arguments = parser.parse_args()

    if arguments.dbg:
        debug = True

    if arguments.P:
        if arguments.password:
            print "Error: You cannot use -P and --password together!"
            sys.exit(1)

        arguments.password = getpass.getpass("Enter password: ")

    if arguments.command == "list":
        bitmask = 0
        if arguments.completed:
            bitmask = bitmask | 1
        if arguments.pending:
            bitmask = bitmask | 2
        if arguments.queued:
            bitmask = bitmask | 4
        if arguments.executing:
            bitmask = bitmask | 8
        if arguments.error:
            bitmask = bitmask | 16
        if arguments.aborted:
            bitmask = bitmask | 32
        if arguments.unknown:
            bitmask = bitmask | 64
        if arguments.held:
            bitmask = bitmask | 128
        if arguments.suspended:
            bitmask = bitmask | 256

        list_jobs(arguments.host, arguments.user, arguments.password, bitmask)

    if arguments.command == "job":
        if arguments.job_command == "show":
            show_job(arguments.host, arguments.user, arguments.password, arguments.id)
        elif arguments.job_command == "new":
            # parse the job parameters and store in argument list
            job_parameters = _check_job_parameter_args(arguments.job_parameters)

            new_job(arguments.host, arguments.user, arguments.password, job_parameters, arguments.run)
        elif arguments.job_command == "set":
            # parse the job parameters and store in argument list
            job_parameters = _check_job_parameter_args(arguments.job_parameters)

            set_parameters_job(arguments.host, arguments.user, arguments.password, arguments.id, job_parameters)
        elif arguments.job_command == "run":
            run_job(arguments.host, arguments.user, arguments.password, arguments.id)
        elif arguments.job_command == "abort":
            abort_job(arguments.host, arguments.user, arguments.password, arguments.id)
        elif arguments.job_command == "delete":
            delete_job(arguments.host, arguments.user, arguments.password, arguments.id)
        elif arguments.job_command == "results":
            results_job(arguments.host, arguments.user, arguments.password, arguments.id, arguments.result_id, arguments.file_base)
        else:
            print "Error: Unknown command %s\n" % (arguments.job_command)

if __name__ == '__main__':
    main()
