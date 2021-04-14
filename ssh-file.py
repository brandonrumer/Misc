#!/usr/bin/env python3
''' Summary: Connects to multiple hosts and uploads a file

Decription:
    This uses the hosts.txt file to connect to multiple ESXi hosts
    and copy the sshd_onfig file. This is used for STIG compliance. The
    sshd_config and hosts.txt file should be in the same directory as
    this python script.
'''


''' Importing built-in modules '''
import getpass
import csv

''' Importing external modules '''
import paramiko


__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Production"


def main():
    file = 'sshd_config'
    mypassword = getpass.getpass("Enter password: ")
    with open('hosts.txt','r') as infile:
        reader = csv.reader(infile)
        hosts = {rows[0] for rows in reader}
    
    for host in hosts:
        try:
            print(f'Connecting to {host}')
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(host,22,username='root',password=mypassword,timeout=4)
            sftp = s.open_sftp()
            sftp.put(file, f'/etc/ssh/{file}')
        except Exception:
            #  Yeah this is ugly but it'll work
            pass


if __name__ == '__main__':
    main()
