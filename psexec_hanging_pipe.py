import sys
import argparse
from impacket.dcerpc.v5 import transport
from impacket.examples.utils import parse_target

if __name__ == '__main__':
	# parse commandline arguments
	parser = argparse.ArgumentParser(add_help = True, description = "Check host for psexec hanging named pipe `RemCom_communicaton`")
	parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
	options = parser.parse_args()
	domain, username, password, remoteName = parse_target(options.target)

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	# configure creds, port, host, ect
	port = 445
	stringbinding = r'ncacn_np:%s[\pipe\svcctl]' % remoteName
	rpctransport = transport.DCERPCTransportFactory(stringbinding)
	rpctransport.set_dport(port)
	rpctransport.setRemoteHost(remoteName)
	rpctransport.set_credentials(username, password, '', '', '', None)
	rpctransport.set_kerberos(False, None)

	# connect to dcerpc and get smb conn
	dce = rpctransport.get_dce_rpc()
	dce.connect()
	s = rpctransport.get_smb_connection()
	s.setTimeout(100000)

	# WaitNamedPipeA for vulnerable hanging pipe
	# https://github.com/kavika13/RemCom/blob/master/RemComSvc/RemComSvc.cpp#L77
	tid = s.connectTree('IPC$')
	try:
		s.waitNamedPipe(tid,"RemCom_communicaton")
	except:
		print("Not Vulnerable")
		sys.exit()

	print("Vulnerable: Hanging Pipe Found!")
