"""SNMP Monitor"""
from pysnmp.hlapi import *
from datetime import datetime
import time

class SNMPService:
    
    # SNMP OID (Object Identifiers)
    OID_SYSTEM_DESCRIPTION = '1.3.6.1.2.1.1.1.0'
    OID_SYSTEM_UPTIME = '1.3.6.1.2.1.1.3.0'
    OID_SYSTEM_NAME = '1.3.6.1.2.1.1.5.0'
    OID_INTERFACES_NUMBER = '1.3.6.1.2.1.2.1.0'
    
    # CPU Memory（Cisco）
    OID_CPU_5SEC = '1.3.6.1.4.1.9.2.1.56.0'  # Cisco CPU 5s
    OID_CPU_1MIN = '1.3.6.1.4.1.9.2.1.57.0'  # Cisco CPU 1min
    OID_MEMORY_USED = '1.3.6.1.4.1.9.9.48.1.1.1.5.1'  # Cisco memory used
    OID_MEMORY_FREE = '1.3.6.1.4.1.9.9.48.1.1.1.6.1'  # Cisco free memory
    
    # in out
    OID_IF_IN_OCTETS = '1.3.6.1.2.1.2.2.1.10'   
    OID_IF_OUT_OCTETS = '1.3.6.1.2.1.2.2.1.16'  
    OID_IF_OPER_STATUS = '1.3.6.1.2.1.2.2.1.8' 
    
    def __init__(self):
        pass
    
    def get_device_info(self, host, community='public', port=161):
     
        try:
            info = {}
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_SYSTEM_DESCRIPTION)))
            )
            
            if errorIndication or errorStatus:
                return None
            
            info['description'] = str(varBinds[0][1])
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_SYSTEM_NAME)))
            )
            
            if not errorIndication and not errorStatus:
                info['hostname'] = str(varBinds[0][1])
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_SYSTEM_UPTIME)))
            )
            
            if not errorIndication and not errorStatus:
                uptime_ticks = int(varBinds[0][1])
                uptime_seconds = uptime_ticks / 100
                info['uptime_seconds'] = uptime_seconds
                info['uptime_days'] = round(uptime_seconds / 86400, 2)
            
            info['timestamp'] = datetime.now().isoformat()
            info['host'] = host
            
            return info
            
        except Exception as e:
            print(f"SNMP Error getting device info from {host}: {e}")
            return None
    
    def get_cpu_usage(self, host, community='public', port=161):
       
        try:
            cpu_data = {}
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_CPU_5SEC)))
            )
            
            if not errorIndication and not errorStatus:
                cpu_data['cpu_5sec'] = int(varBinds[0][1])
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_CPU_1MIN)))
            )
            
            if not errorIndication and not errorStatus:
                cpu_data['cpu_1min'] = int(varBinds[0][1])
            
            cpu_data['timestamp'] = datetime.now().isoformat()
            
            return cpu_data if cpu_data else None
            
        except Exception as e:
            print(f"SNMP Error getting CPU from {host}: {e}")
            return None
    
    def get_memory_usage(self, host, community='public', port=161):
       
        try:
            memory_data = {}
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_MEMORY_USED)))
            )
            
            if not errorIndication and not errorStatus:
                memory_used = int(varBinds[0][1])
                memory_data['memory_used'] = memory_used
            else:
                return None
            
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(self.OID_MEMORY_FREE)))
            )
            
            if not errorIndication and not errorStatus:
                memory_free = int(varBinds[0][1])
                memory_data['memory_free'] = memory_free
            
                memory_total = memory_used + memory_free
                memory_data['memory_total'] = memory_total
                memory_data['memory_percent'] = round((memory_used / memory_total) * 100, 2)
            
            memory_data['timestamp'] = datetime.now().isoformat()
            
            return memory_data
            
        except Exception as e:
            print(f"SNMP Error getting memory from {host}: {e}")
            return None
    
    def get_interface_stats(self, host, interface_index=1, community='public', port=161):

        try:
            stats = {}
            
            oid_in = f"{self.OID_IF_IN_OCTETS}.{interface_index}"
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid_in)))
            )
            
            if not errorIndication and not errorStatus:
                stats['bytes_in'] = int(varBinds[0][1])
            

            oid_out = f"{self.OID_IF_OUT_OCTETS}.{interface_index}"
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid_out)))
            )
            
            if not errorIndication and not errorStatus:
                stats['bytes_out'] = int(varBinds[0][1])
            
            oid_status = f"{self.OID_IF_OPER_STATUS}.{interface_index}"
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid_status)))
            )
            
            if not errorIndication and not errorStatus:
                # 1=up, 2=down, 3=testing, 4=unknown, 5=dormant
                status_code = int(varBinds[0][1])
                status_map = {1: 'up', 2: 'down', 3: 'testing', 4: 'unknown', 5: 'dormant'}
                stats['status'] = status_map.get(status_code, 'unknown')
            
            stats['interface_index'] = interface_index
            stats['timestamp'] = datetime.now().isoformat()
            
            return stats if stats else None
            
        except Exception as e:
            print(f"SNMP Error getting interface stats from {host}: {e}")
            return None
    
    def get_all_metrics(self, host, community='public', port=161):
      
        try:
            metrics = {
                'host': host,
                'timestamp': datetime.now().isoformat()
            }
            
            device_info = self.get_device_info(host, community, port)
            if device_info:
                metrics['device_info'] = device_info
            
            cpu_usage = self.get_cpu_usage(host, community, port)
            if cpu_usage:
                metrics['cpu'] = cpu_usage
            
            memory_usage = self.get_memory_usage(host, community, port)
            if memory_usage:
                metrics['memory'] = memory_usage
            
            interface_stats = self.get_interface_stats(host, 1, community, port)
            if interface_stats:
                metrics['interface'] = interface_stats
            
            return metrics
            
        except Exception as e:
            print(f"Error getting all metrics from {host}: {e}")
            return None
    
    def walk_oid(self, host, oid, community='public', port=161, max_results=10):
       
        try:
            results = []
            
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in nextCmd(SnmpEngine(),
                                     CommunityData(community),
                                     UdpTransportTarget((host, port)),
                                     ContextData(),
                                     ObjectType(ObjectIdentity(oid)),
                                     lexicographicMode=False,
                                     maxRows=max_results):
                
                if errorIndication or errorStatus:
                    break
                
                for varBind in varBinds:
                    results.append({
                        'oid': str(varBind[0]),
                        'value': str(varBind[1])
                    })
            
            return results
            
        except Exception as e:
            print(f"SNMP Walk error on {host}: {e}")
            return None


if __name__ == '__main__':
    snmp = SNMPService()
    
    test_host = '192.168.1.1'
    
    print("=" * 60)
    print("SNMP Device Monitoring Test")
    print("=" * 60)
    
    print("\n1. Device Info:")
    device_info = snmp.get_device_info(test_host)
    if device_info:
        for key, value in device_info.items():
            print(f"   {key}: {value}")
    else:
        print("   ❌ Unable to connect to device")
    
    print("\n2. CPU Usage:")
    cpu = snmp.get_cpu_usage(test_host)
    if cpu:
        print(f"   5 sec avg: {cpu.get('cpu_5sec', 'N/A')}%")
        print(f"   1 min avg: {cpu.get('cpu_1min', 'N/A')}%")
    else:
        print("   ❌ CPU data not available")
    
    print("\n3. Memory Usage:")
    memory = snmp.get_memory_usage(test_host)
    if memory:
        print(f"   Used: {memory.get('memory_used', 0)} bytes")
        print(f"   Free: {memory.get('memory_free', 0)} bytes")
        print(f"   Usage: {memory.get('memory_percent', 0)}%")
    else:
        print("   ❌ Memory data not available")
    
    print("\n4. Interface Stats:")
    interface = snmp.get_interface_stats(test_host, interface_index=1)
    if interface:
        print(f"   Status: {interface.get('status', 'unknown')}")
        print(f"   Bytes In: {interface.get('bytes_in', 0)}")
        print(f"   Bytes Out: {interface.get('bytes_out', 0)}")
    else:
        print("   ❌ Interface data not available")
    
    print("\n" + "=" * 60)