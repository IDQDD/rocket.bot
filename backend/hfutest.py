import logging
import time
from scrapli.driver import GenericDriver
from scrapli.driver.core import IOSXEDriver
from scrapli.driver.network_driver import PrivilegeLevel
logging.basicConfig(filename="scrapli.log", level=logging.DEBUG)
logger = logging.getLogger("scrapli")

PRIVS = {
    "exec": (PrivilegeLevel(r"^[a-z0-9.\-_@()/:]{1,32}>$", "exec", "", "", "", False, "",)),
    "privilege_exec": (
        PrivilegeLevel(
            r"^[a-z0-9.\-_@/:]{1,32}#$",
            "privilege_exec",
            "exec",
            "disable",
            "enable",
            True,
            "Password:",
        )
    ),
    "configuration": (
        PrivilegeLevel(
            r"^(\\n)?[a-z0-9.\-_@/:]{1,32}\(conf[a-z0-9.\-@/:]{0,32}\)#$",
            "configuration",
            "privilege_exec",
            "end",
            "configure terminal",
            False,
            "",
        )
    ),
}

def main():  

    mydevice = {
        "host": "sw-nfu",
        "auth_username": "backup",
        "auth_password": "cheeFee1",
        "auth_strict_key": False,        
        "ssh_config_file": True,     
        #"transport": "paramiko",   
        'privilege_levels': PRIVS,
    }
     
    conn = IOSXEDriver(**mydevice)
    conn.open()
    print(conn.get_prompt())
    print(conn.send_command("show ver").result)
    conn.close()

if __name__ == "__main__":
    main()