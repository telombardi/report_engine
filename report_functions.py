from datetime import datetime
import os
import pkg_resources
import platform
import psutil
from psutil._common import bytes2human
import re
import sys
import socket
import uuid

def get_python_version() -> str:
  return sys.version

def getdate() -> str:
  return datetime.today().strftime('%Y-%m-%d')

def gethostname() -> str:
  return socket.gethostname()

def getsystemtype() -> str:
  return platform.system()

def getmac() -> str:
  return ':'.join(re.findall('..','%012x' % uuid.getnode()))

def getinterfaces() -> list:
  net_return = list()
  net_temp = ''
  af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
  }
  nets = psutil.net_if_addrs()
  for nic, addrs in nets.items():
    for addr in addrs:
      net_temp=nic + ','+af_map.get(addr.family, addr.family)+','+addr.address
      net_return.append(net_temp)
  return net_return

def getip() -> list:
  ip_list = []
  for interface in psutil.net_if_addrs():
    if psutil.net_if_addrs()[interface][0].address:
      if psutil.net_if_addrs()[interface][0].address != '127.0.0.1':
        ip_list.append(psutil.net_if_addrs()[interface][0].address)
  return ip_list      

def getuname() -> str:
  return platform.platform()

def get_cpu_block() -> str:
  return psutil.cpu_percent(interval=1)

def get_cpu_nonblock() -> str:
  return psutil.cpu_percent(interval=None)

def get_cpu_avg_loads() -> tuple:
  return psutil.getloadavg()

def get_cpu_times() -> tuple:
  return psutil.cpu_times()

def get_total_mem() -> str:
  return bytes2human(psutil.virtual_memory().total)

def get_used_mem_bytes() -> int:
  return psutil.virtual_memory().used

def get_used_mem() -> str:
  return bytes2human(psutil.virtual_memory().used)

def get_available_mem_bytes() -> int:
  return psutil.virtual_memory().available  

def get_available_mem() -> str:
  return bytes2human(psutil.virtual_memory().available)

def get_percent_mem() -> str:
  return psutil.virtual_memory().percent

def get_disk_usage_total() -> str:
  return bytes2human(psutil.disk_usage('/').total)

def get_disk_usage_used_bytes() -> int:
  return psutil.disk_usage('/').used
  
def get_disk_usage_used() -> str:
  return bytes2human(psutil.disk_usage('/').used)

def get_disk_usage_free_bytes() -> int:
  return psutil.disk_usage('/').free

def get_disk_usage_free() -> str:
  return bytes2human(psutil.disk_usage('/').free)

def get_disk_usage_percent() -> str:
  return psutil.disk_usage('/').percent  

def get_mount_points() -> list:
  mounts = []
  templ = '%-17s,%8s,%8s,%8s,%5s%%,%9s,%s'
  for part in psutil.disk_partitions(all=False):
    usage = psutil.disk_usage(part.mountpoint)
    line = templ % (part.device,bytes2human(usage.total),bytes2human(usage.used),bytes2human(usage.free),int(usage.percent),part.fstype,part.mountpoint,)
    mounts.append(line)
  return mounts
    
def get_net_listeners() -> list:
  print('Executed function.')
  net_list = []
  try:
    print('In try...')
    lc = psutil.net_connections('inet')
    print(lc)
    for c in lc:
      print(c)
      (ip, port) = c.laddr
      if ip == '0.0.0.0' or ip == '::':
        if c.type==socket.SOCK_STREAM and c.status==psutil.CONN_LISTEN:
          proto_s = 'tcp'
        elif c.type==socket.SOCK_DGRAM:
          proto_s = 'udp'
        else:
          continue
        pid_s = str(c.pid) if c.pid else '(unknown)'
        msg = 'PID {} is listening on port {}/{} for all IPs.'
        msg = msg.format(pid_s,port,proto_s)
        net_list.append(msg)
    
  except PermissionError as pe:
    print('Permission Denied.')
    print(pe)
  except psutil.AccessDenied as ae:
    print('Access Denied.')
    print(ae)
  except:
    print('Error')

  finally:
    return net_list    

def get_python_packages() -> list:
  installed_packages = pkg_resources.working_set
  installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
  return installed_packages_list
    
def get_process_information():
  p = psutil.Process()
  with p.oneshot():
    p.cpu_percent()

    
def get_dnf_packages() -> list:
  base = dnf.Base()
  base.fill_sack()
  q=base.sack_query()
  i=q.installed()
  packages = list(i)
  return packages

if __name__=='__main__':
  
  # Print each package and its version in the sorted list.
  for m in get_python_packages():
    print(m)
      
    
  #print(getinterfaces())
  #for key in getinterfaces():
  #  print(key, '->', getinterfaces()[key])
  #print(getmac())
  #print(get_mount_points())
  #print(get_cpu_block())
  #print(get_cpu_nonblock())
