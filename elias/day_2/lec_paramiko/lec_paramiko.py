import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import stat
import time
from icecream import ic
import sys

ic.configureOutput(includeContext=True)

class MySSH:
    def __init__(self):
        self.client = None      # SSH Client Object
        self.scp_client = None  # SCP Client Object
        self.ftp_client = None  # SFTP Client Object

    ###############################################################
    # Check Connection
    ###############################################################
    def isAlive(self):
        if self.client is None:
            return False
        else:
            return self.client.get_transport().is_active()

    ###############################################################
    # Connect Host
    ###############################################################
    def connect(self, host, user_id, user_password, port=22, timeout=None):
        # 접속여부 확인
        if self.client is None:
            self.client = SSHClient()

            # 아래 코드를 추가해야만 'not found in known hosts'라는 예외가 발생하지 않음
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, port=port, username=user_id,
                                password=user_password, timeout=timeout)

            if self.isAlive():
                self.password = user_password
                return True
            else:
                return False

    ###############################################################
    # Disconnect
    ###############################################################
    def disconnect(self):
        if self.client is not None:
            self.client.close()

    ###############################################################
    # Execute Shell Command
    ###############################################################
    def exeCommand(self, command, isReturn=False):
        if self.isAlive():
            stdin, stdout, stderr = self.client.exec_command(command)
            if stdout.channel.recv_exit_status() != 0:
                return stderr.read()

            if isReturn is True:
                return stdout.readlines()
        else:
            ic('Client is not connected!!!')

    ###############################################################
    # Execute Shell Command as root (sudo command)
    ###############################################################
    def sudoCommand(self, command, isReturn=False):
        if self.isAlive():
            stdin, stdout, stderr = self.client.exec_command('sudo ' + command, get_pty=True)

            stdin.write(self.password + '\n')
            if stdout.channel.recv_exit_status() != 0:
                return stderr.read()

            if isReturn is True:
                return stdout.readlines()
        else:
            ic('Client is not connected')

    ################################################################
    # Get File From Host (SFTP)
    # srcFilePath: Server(host), dstFilePath: Local(PC, Client)
    ################################################################
    def getFromHost(self, srcFilePath, dstFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.get(srcFilePath, dstFilePath)

    ################################################################
    # Put File to Host (SFTP)
    # srcFilePath: Local(PC, Client), dstFilePath: Server(host)
    ################################################################
    def putToHost(self, srcFilePath, dstFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.put(srcFilePath, dstFilePath)

    ###############################################################
    # Rename file on Host (SFTP)
    # srcFilePath: Old Name, desFilePath: New Name
    ###############################################################
    def renameHostFile(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.rename(srcFilePath, dstFilePath)

    ###############################################################
    # Delete file on Host (SFTP)
    # filePath: Server(host)
    ###############################################################
    def deleteHostFile(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.remove(filePath)

    ###############################################################
    # Get file list on Host (SFTP)
    # filePath: Server(host)
    ###############################################################
    def getFileListFromHost(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir(filePath)

    #######################################################################
    # Get file list of host
    # srcFilePath: Server(host)
    ##############################################################
    def getFileAttrListFromHost(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir_attr(srcFilePath)

    ###############################################################
    # Delete folder of host
    # srcFilePath: Server(host)
    ###############################################################
    def deleteHostFolder(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()

        # # Only current folder only
        # file_list = self.getFileListFromHost(srcFilePath)
        # for file in file_list:
        #     file_path = os.path.join(srcFilePath, file)
        #     # srcFilePath /var/www  filename: log.txt -> /var/www/log.txt
        #     file_path = file_path.replace('\\', '/')
        #     self.deleteHostFile(file_path)

        # Delete all subfolder recursive
        file_attr_list = self.ftp_client.listdir_attr(srcFilePath)
        for file_attr in file_attr_list:
            path = os.path.join(srcFilePath, file_attr.filename)
            path = path.replace('\\', '/')
            # Path is Folder type
            if stat.S_ISDIR(file_attr.st_mode):
                self.deleteHostFolder(path)
            # Path is File type
            else:
                self.deleteHostFile(path)

        self.ftp_client.rmdir(srcFilePath)  # rm -rf target_folder

    ################################################################
    # Get File From Host with SCP
    # srcFilePath: Server(host), dstFilePath: Local(PC, Client)
    ################################################################
    def getFromHostWithSCP(self, srcFilePath, dstFilePath):
        if self.scp_client is None:
            self.scp_cleint = SCPClient(self.client.get_transport())
        self.scp_cleint.get(srcFilePath, dstFilePath)

    ###############################################################
    # Put file to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def putToHostWithSCP(self, srcFilePath, dstFilePath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcFilePath, dstFilePath)

    ###############################################################
    # Get folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def getFolderFromHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.get(srcDirPath, dstDirPath, recursive=True)

    ###############################################################
    # Put folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def putFolderToHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcDirPath, dstDirPath, recursive=True)


if __name__ == '__main__':
    ssh = MySSH()
    if ssh.connect('211.169.249.211', 'elias', '1111', timeout=5, port=22):
        ic('SSH is connected')

        # ###########################################################
        # # Process List 파일생성 (ps -ef > process_list.txt)
        # ###########################################################
        # ssh.exeCommand('ps -ef > process_list.txt')

        # ###########################################################
        # # 파일목록 가져오기 (ls -al)
        # ###########################################################
        # file_list = ssh.exeCommand('ls -al', isReturn=True)
        # for file in file_list:
        #     print(file, end='')

        ###########################################################
        # temp 폴더로 이동 후 process_list.txt 파일 생성
        ###########################################################
        # ssh.exeCommand('cd temp') # temp 폴더로 이동
        # ssh.exeCommand('ps -ef > process_list.txt') # proces_list.txt 파일 생성
    
        # ; --> 앞의 명령어가 실패해도, 뒤에 명령어를 실행
        # && --> 앞의 명령어가 성공했을대만 뒤에 명령어를 실행
        # & --> 앞의 명령어는 background로 실행하고 뒤에 명령어를 실행
        # ssh.exeCommand('cd temp && ps -ef > process_list.txt')

        ###########################################################
        # Shell Script 파일생성 후 실행권한을 주고 실행
        ###########################################################
        # ssh.exeCommand('echo "ps -ef > process_list.txt" > make_process_list.sh') # 쉘스크립트파일 생성
        # ssh.exeCommand('chmod +x ./make_process_list.sh')   # 실행 옵션추가
        # ssh.exeCommand('./make_process_list.sh') # 쉘스크립트 실행

        ###########################################################
        # sudo 커맨드 실행
        ###########################################################
        # ssh.exeCommand('sudo mkdir /lg/elias')
        # ssh.sudoCommand('mkdir /lg/elias')
        # ssh.sudoCommand('apt install nmap -y')
        # ssh.sudoCommand('./install.sh')

        ###########################################################
        # 서버로부터 파일 가져오기
        ###########################################################
        # ssh.getFromHost('./process_list.txt', './process_list.txt')

        ###########################################################
        # 서버로 파일 업로드하기
        ###########################################################
        # ssh.putToHost('./process_list.txt', './process_list_2.txt')

        ################################################################################
        # 서버에 있는 파일명 변경
        ###############################################################
        # ssh.renameHostFile('./process_list.txt', './process.txt')
        # ssh.renameHostFile('./temp', './temp2')

        # ################################################################################
        # # 서버에 있는 파일삭제
        # ###############################################################
        # ssh.deleteHostFile('./process.txt')

        # ################################################################################
        # # 서버의 폴더내 파일목록 가져오기
        # ###############################################################
        # file_list = ssh.getFileListFromHost('./temp')
        # # ic(file_list)
        # for file in file_list:
        #     print(file)

        # ################################################################################
        # # 서버의 폴더내 파일목록을 속성과 함께 가져오기
        # ###############################################################
        # file_list = ssh.getFileAttrListFromHost('./temp')
        # # ic(file_list)
        # for file in file_list:
        #     print(file)

        # ################################################################################
        # # 서버의 폴더삭제
        # ###############################################################
        # ssh.deleteHostFolder('./temp')

        ###########################################################
        # 서버로부터 파일 가져오기 with SCP
        ###########################################################
        # ssh.getFromHostWithSCP('./log.txt', './log.txt')

        # ######################################################################
        # # Put file to host with scp
        # ###############################################################
        # ssh.putToHostWithSCP('./process_list.txt', 'process_list_3.txt')

        # ######################################################################
        # # Get folder from host with scp
        # ###############################################################
        # ssh.getFolderFromHostSCP('temp', 'temp')

        # ######################################################################
        # # Put folder to host with scp
        # ###############################################################
        # ssh.putFolderToHostSCP('temp', 'temp2')

    else:
        ic('Connect fail')

























