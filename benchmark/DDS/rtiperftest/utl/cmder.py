#!/usr/bin/python3
import sys
import subprocess
import utl
import argparse
import json
import time


USER = 'pi'

cmd_logger = utl.get_logger('cmd_logger', 'CMDExec.log')

def execute_cmd(server, cmd, unblock=False):
    if not unblock:
        try:
            result = utl.exec_rmt_cmd(user=USER, address=server, cmd=cmd)    
            cmd_logger.info('Executing command\n %s \nin server %s.' % (cmd, server))
            cmd_logger.info('\nExecution result:\n')
            cmd_logger.info(result[0])
            cmd_logger.error(result[1])
        except Exception as ex:
            cmd_logger.error('Some errors happened while executing command: \n %s' % str(ex))
    else:
        cmd_logger.info('Executing command\n %s \nin server %s.' % (cmd, server))
        cmd = 'nohup ssh %s %s > CMDExec.log 2>&1 &' % (server, cmd)
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for executing commands in Siemens Raspberry Pis(Workers).")
    parser.add_argument('-a', '--all', action='store_true', default=False, help='execute the given command on s1-s10')
    parser.add_argument('-s', '--server', action='store', type=str, help='execute command on a server rather s1-s10')
    parser.add_argument('-l', '--list', help='a list of servers separated by comma, from s1-s10', type=str, default='', required=False)
    parser.add_argument('-c', '--cmd', type=str, required=True, help='command you want to execute')
    parser.add_argument('-u', '--unblock', default=True, action='store_true', help="run commands in unblock mode")

    args = parser.parse_args()
    unblock = args.unblock

    servers = []
    with open('server_list.json') as f:
        servers = json.load(f)
    
    if args.all:
        for svr in servers['raspberry'].values():
            execute_cmd(svr, args.cmd, unblock)
            time.sleep(0.3)
    elif args.list != '':
        hosts = args.list.split(',')
        for svr in hosts:
            execute_cmd(servers['raspberry'][svr], args.cmd, unblock)
            time.sleep(0.3)
    else:
        if args.server == '':
            cmd_logger.error('Please specify server address or run commands on all servers.')
        else:
            execute_cmd(args.server, args.cmd)