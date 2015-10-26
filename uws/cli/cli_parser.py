# -*- coding: utf-8 -*-
import argparse


def build_argparse():
    parser = argparse.ArgumentParser(prog='uws')
    parser.add_argument('-H', '--host', help='URL to UWS service', required=True)
    parser.add_argument('-U', '--user', help='user name')
    parser.add_argument('--password', help='password')
    parser.add_argument('-P', action='store_true', help='hidden password (type at prompt)')
    parser.add_argument('-D', '--dbg', action='store_true', help='debug mode')

    subparsers = parser.add_subparsers(dest='command', help='commands for UWS')
    build_list_argparse(subparsers)
    build_job_argparse(subparsers)

    return parser


def build_list_argparse(subparsers):
    parser_list = subparsers.add_parser('list', help='list all jobs on the UWS service')
    parser_list.add_argument('-c', '--completed', action='store_true', help='show completed jobs')
    parser_list.add_argument('-p', '--pending', action='store_true', help='show pending jobs')
    parser_list.add_argument('-q', '--queued', action='store_true', help='show queued jobs')
    parser_list.add_argument('-e', '--executing', action='store_true', help='show executing jobs')
    parser_list.add_argument('-E', '--error', action='store_true', help='show jobs with errors')
    parser_list.add_argument('-a', '--aborted', action='store_true', help='show aborted jobs')
    parser_list.add_argument('-A', '--archived', action='store_true', help='[UWS1.1] show (deleted) jobs archived on the server')
    parser_list.add_argument('--unknown', action='store_true', help='show unknown state jobs')
    parser_list.add_argument('--held', action='store_true', help='show held jobs')
    parser_list.add_argument('--suspended', action='store_true', help='show suspended jobs')
    parser_list.add_argument('--after', action='store', help='[UWS1.1] show only jobs started after given UTC time or local time + timezone')
    parser_list.add_argument('--last', action='store', help='[UWS1.1] show only most recently started jobs')

    return parser_list


def build_job_argparse(subparsers):
    parser_job = subparsers.add_parser('job', help='access a given job on the UWS service')

    job_subparsers = parser_job.add_subparsers(dest='job_command', help='commands for manipulating jobs')
    parser_job_show = job_subparsers.add_parser('show', help='show the specific job')
    parser_job_show.add_argument('id', help='job id')
    parser_job_show.add_argument('-w', '--wait', nargs='?', const='-1', default=None, help='[UWS1.1] wait for phase change before returning, but at most the specified amount of seconds or infinitely, if no value is given')
    parser_job_show.add_argument('-s', '--phase', help='[UWS1.1] required phase while waiting')

    parser_job_phase = job_subparsers.add_parser('phase', help='show the phase of specific job')
    parser_job_phase.add_argument('id', help='job id')

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

    return parser_job_results
