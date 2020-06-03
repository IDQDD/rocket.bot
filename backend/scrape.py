# this module provides functions that connect to network switches and request arp and mac tables.
# It's using the scrapli library under the hood
from scrapli.driver.core import IOSXEDriver, NXOSDriver, JunosDriver
from scrapli.helper import textfsm_parse

def PrepareConnObject(host):
# platform independent data
    my_device = { 
        'host': host['hostname'],
        'auth_username': host['username'],
        'auth_password': host.get('password', "")
    }   

    ssh_map = { 
        'auth_strict_key': False, 
        'ssh_config_file': True, 
        'auth_private_key': host.get('auth_private_key', ""), 
    }
    
    telnet_map = { 
        'transport': 'telnet', 
        'port': 23 
    }

    if host.get('data') and host['data'].get('transport') == 'telnet': 
        my_device = { **my_device, **telnet_map }
        return my_device
    
    my_device = { **my_device, **ssh_map }

    if host['platform'] == 'huawei':
    # custom driver's options for huawei gears
        from scrapli.driver.network_driver import PrivilegeLevel
        PRIVS = {    
        'privilege_exec': (
            PrivilegeLevel(r'^(\\n)?<.+>$', 'privilege_exec', '', '', '', False, '', )),
        'configuration': (
            PrivilegeLevel(r'^(\\n)?\[.+\]>$', 'configuration', 'privilege_exec', 'quit', 'system-view', False, '', )),
        }

        def huawei_disable_paging(conn):
            conn.channel.send_input(channel_input='screen-length 0 temporary')

        huawei_opts = {        
            'privilege_levels': PRIVS,
            'on_open': huawei_disable_paging,
            'transport': 'paramiko',
            "timeout_socket": 20,
            "timeout_transport": 20,
        }
        my_device = { **my_device, **huawei_opts }

    return my_device


def QuerySwitch(my_device, platform, custom_textfsm=None):    

    conn = platform['driver'](**my_device)    
   
    conn.open()
    response = conn.send_command(platform['cmd'])
    
    if custom_textfsm:
        return textfsm_parse(custom_textfsm, response.result)
    return response.textfsm_parse_output()


def get_port_by_mac(host, mac, vlan=None):
    platform_map = {
        'ios': {
            'driver': IOSXEDriver,
            'cmd': f'sh mac address-table address {mac} vlan {vlan}' if vlan else f'sh mac address-table address {mac}',
        },
        'nxos': {
            'driver': NXOSDriver,
            'cmd': f'sh mac address-table vlan {vlan} address {mac}' if vlan else f'sh mac address-table address {mac}',
        },
        'junos': {
            'driver': JunosDriver,
            'cmd': f'sh ethernet-switching table vlan {vlan} | match {mac}',
        },
        'huawei': {
            'driver': IOSXEDriver,
            'cmd': f'display mac-address {mac} vlan {vlan}' if vlan else f'display mac-address {mac}'
        }
    }

    my_device = PrepareConnObject(host)

    platform = host['platform']
    if platform == 'junos':
        custom_textfsm = 'textfsm/juniper_show_ethernet-switching_table.textfsm'
    elif platform == 'huawei':
        custom_textfsm = 'textfsm/huawei_display_mac-address.textfsm'
    else:
        custom_textfsm = None

    res = QuerySwitch(my_device, platform_map[platform], custom_textfsm)

    if res:
        port_map = {
            'ios': 'destination_port',
            'nxos': 'ports',
            'junos': 'interface',
            'huawei': 'if'
        }
        
        # Juniper has no VLAN id info in the output. returning one from the input
        if platform == 'junos':
            return {'port': res[0][port_map[platform]], 'vlan': vlan}
        else:
            return {'port': res[0][port_map[platform]], 'vlan': res[0]['vlan']}

    else:
        return None


def get_mac_by_ip(host, ip):
# supports ios and nxos platforms only
    platform_map = {
        'ios': {
            'driver': IOSXEDriver,
            'cmd': f'sh ip arp {ip}',       
        },
        'nxos': {
            'driver': NXOSDriver,
            'cmd': f'sh ip arp {ip}',        
        },
        'huawei': {
            'driver': IOSXEDriver,
            'cmd': f'display arp network {ip}'
        }
    }

    my_device = PrepareConnObject(host)

    platform = host['platform']

    if platform == 'huawei':
        custom_textfsm = 'textfsm/huawei_display_arp_network.textfsm'
    else:
        custom_textfsm = None

    res = QuerySwitch(my_device, platform_map[platform], custom_textfsm)
    
    if res:
        print(f"res = {res}")

        mac = res[0]['mac']

        if platform == 'huawei':
            return { 'mac': mac, 'vlan': None }
            
        vlan = int(''.join(x for x in res[0]['interface'] if x.isdigit())) # transform Vlan221 to 221
        return { 'mac': mac, 'vlan': vlan }
    else:
        return None
