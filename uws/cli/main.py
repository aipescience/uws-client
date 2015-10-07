import getpass
import sys

from functools import wraps
import texttable as tt
from uws.lib.terminalsize import terminalsize as console

import cli_parser
from uws import UWS

debug = True


def handle_error(handler):
    @wraps(handler)
    def handle(self, *args, **kwargs):
        try:
            return handler(self, *args, **kwargs)
        except UWS.UWSError as e:
            if not debug:
                print "An error occurred:\n   %s" % e.msg
                return
            else:
                print e.raw
                raise
    return handle


@handle_error
def list_jobs(url, user_name, password, phases, after=None, last=None):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    filters = {}
    if phases:
        filters['phases'] = phases
    if after:
        filters['after'] = after
    if last:
        filters['last'] = last

    jobs = uws_client.get_job_list(filters)

    job_phases = UWS.models.JobPhases

    # we will apply client side filtering anyways, since we are not
    # sure that a UWS service is version 1.1 and supports server side
    # filtering.
    rows = [["ID", "Job name", "Status"]]
    for job in jobs.job_reference:
        if not phases or jobs.version == "1.1":
            _register_job_reference_for_table(rows, job)
        else:
            if job_phases.COMPLETED in phases and job_phases.COMPLETED in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.PENDING in phases and job_phases.PENDING in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.QUEUED in phases and job_phases.QUEUED in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.EXECUTING in phases and job_phases.EXECUTING in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.ERROR in phases and job_phases.ERROR in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.ABORTED in phases and job_phases.ABORTED in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.UNKNOWN in phases and job_phases.UNKNOWN in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.HELD in phases and job_phases.HELD in job.phase:
                    _register_job_reference_for_table(rows, job)
            if job_phases.SUSPENDED in phases and job_phases.SUSPENDED in job.phase:
                    _register_job_reference_for_table(rows, job)
            # add ARCHIVED phase as well for services with version 1.0 that already support this
            if job_phases.ARCHIVED in phases and job_phases.ARCHIVED in job.phase:
                    _register_job_reference_for_table(rows, job)
    (console_width, console_height) = console.get_terminal_size()

    table = tt.Texttable(max_width=console_width)
    table.set_deco(tt.Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.add_rows(rows)

    print "List of jobs on UWS service for user: '%s'" % user_name
    print table.draw()
    print "%d jobs listed." % (len(rows) - 1)


def _register_job_reference_for_table(rows, jobref):
    if (jobref.reference.href is not None):
        job_id = jobref.reference.href.rsplit("/", 1)[1]
    else:
        # The 'xlink:href' attribute is optional, an explicite link is not 
        # required. Therefore, if no link is given, then assume that the 
        # provided jobref-id from the short description is the same as the 
        # unique job_id in these cases (otherwise one could NOT use the job 
        # list to get the job_ids, which would not make any sense).
        # See xml schema described in 
        # http://www.ivoa.net/documents/UWS/20150626/PR-UWS-1.1-20150626.pdf): 
        job_id = jobref.id

    rows.append([job_id, jobref.id, ', '.join(jobref.phase)])


@handle_error
def show_job(url, user_name, password, id):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    job = uws_client.get_job(id)

    _print_job(job)


@handle_error
def show_phase(url, user_name, password, id):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    phase = uws_client.get_phase(id)

    print(phase)


@handle_error
def new_job(url, user_name, password, parameters={}, run=False):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    job = uws_client.new_job(parameters)

    if run:
        # execute the job
        job = uws_client.run_job(job.job_id)

    (console_width, console_height) = console.get_terminal_size()

    _print_job(job)

    print "\n"
    print "*" * (console_width - 1)
    print "You can access this job with the id:\n"
    print "Job ID: %s" % job.job_id
    print "Command: uws -H %s --user %s --password YOUR_PASSWORD_HERE job show %s" % (url, user_name, job.job_id)
    print "*" * (console_width - 1)


@handle_error
def set_parameters_job(url, user_name, password, id, parameters={}):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    if len(parameters) == 0:
        job = uws_client.get_job(id)
    else:
        job = uws_client.set_parameters_job(id, parameters)

    _print_job(job)


@handle_error
def run_job(url, user_name, password, id):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    job = uws_client.run_job(id)

    _print_job(job)


@handle_error
def abort_job(url, user_name, password, id):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    job = uws_client.abort_job(id)

    _print_job(job)


@handle_error
def delete_job(url, user_name, password, id):
    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    success = uws_client.delete_job(id)

    if success:
        print "Job %s successfully deleted!" % (id)


@handle_error
def results_job(url, user_name, password, id, result_id, user_file_base):
    def print_progress(total_size, current):
        if total_size:
            sys.stdout.write("\r%d bytes" % current)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
        else:
            sys.stdout.write("\rDownloaded %d bytes" % current)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()

    uws_client = UWS.client.Client(url=url, user=user_name, password=password)

    job = uws_client.get_job(id)

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
            uws_client.connection.download_file(url, user_name, password, filename, callback=print_progress)
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
        # valid arguments are of the form <parameter>=<value>
        argument_pair = argument.split("=", 1)
        if len(argument_pair) != 2:
            raise RuntimeError('Malformatted parameter found: %s' % (", ".join(argument_pair)))

        if argument_pair[0].lower() == "destruction":
            argument_pair[0] = "destruction"

        if argument_pair[0].lower() == "executionduration":
            argument_pair[0] = "executionDuration"

        argument_list[argument_pair[0]] = argument_pair[1]

    return argument_list


def _check_joblist_after(argument):
    # TODO: should check here for proper time format or only when validating parameters later on?
    return argument


def _check_joblist_last(argument):
    #try:
    #    nlast = int(argument)
    #except ValueError:
    #    sys.exit("Error: Value for 'last' argument must be an integer: %s" % (str(argument)))
    #return nlast
    # checks will be done in _validate_and_parse_filters
    return argument


def main():
    global debug
    parser = cli_parser.build_argparse()
    arguments = parser.parse_args()

    if arguments.dbg:
        debug = True

    if arguments.P:
        if arguments.password:
            print "Error: You cannot use -P and --password together!"
            sys.exit(1)

        arguments.password = getpass.getpass("Enter password: ")

    phases = []
    if arguments.command == "list":
        if arguments.completed:
            phases.append(UWS.models.JobPhases.COMPLETED)
        if arguments.pending:
            phases.append(UWS.models.JobPhases.PENDING)
        if arguments.queued:
            phases.append(UWS.models.JobPhases.QUEUED)
        if arguments.executing:
            phases.append(UWS.models.JobPhases.EXECUTING)
        if arguments.error:
            phases.append(UWS.models.JobPhases.ERROR)
        if arguments.aborted:
            phases.append(UWS.models.JobPhases.ABORTED)
        if arguments.unknown:
            phases.append(UWS.models.JobPhases.UNKNOWN)
        if arguments.held:
            phases.append(UWS.models.JobPhases.HELD)
        if arguments.suspended:
            phases.append(UWS.models.JobPhases.SUSPENDED)
        if arguments.archived:
            phases.append(UWS.models.JobPhases.ARCHIVED)

        after = None
        if arguments.after:
            after = _check_joblist_after(arguments.after)

        last = None
        if arguments.last:
            last = _check_joblist_last(arguments.last)

        list_jobs(arguments.host, arguments.user, arguments.password, phases, after, last)

    if arguments.command == "job":
        if arguments.job_command == "show":
            show_job(arguments.host, arguments.user, arguments.password, arguments.id)
        elif arguments.job_command == "phase":
            show_phase(arguments.host, arguments.user, arguments.password, arguments.id)
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
