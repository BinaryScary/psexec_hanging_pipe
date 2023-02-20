# psexec_hanging_pipe
A quick script to detect hanging RemComSvc pipes left from impacket's psexec.py tool

## Vulnerability Information
Impacket's psexec.py tool installs an [open source version](https://github.com/kavika13/RemCom) of the RemCom service on the target host. This service creates multiple NamedPipes, each with an empty DACL allow `Everyone` read/write. Due to the lack of permissions any low-privilege attacker with access to the target can connect to this named pipe and gain code execution as `nt authority\system`.

## Usage
```
usage: psexec_hanging_pipe.py [-h] target

Check host for psexec hanging named pipe `RemCom_communicaton`

positional arguments:
  target      [[domain/]username[:password]@]<targetName or address>

optional arguments:
  -h, --help  show this help message and exit
```
