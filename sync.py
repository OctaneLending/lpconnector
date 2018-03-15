import os,sys

from dotenv import load_dotenv
from ldap_server import LDAPServer

def main(argv):
    load_dotenv()
    LDAP_SERVER = os.getenv("LDAP_SERVER")
    LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
    LDAP_USER = os.getenv("LDAP_BINDING_USER_UID")
    LDAP_PWD = os.getenv("LDAP_BINDING_USER_PWD")
    ldapServer = LDAPServer(LDAP_SERVER, LDAP_BASE_DN, LDAP_USER, LDAP_PWD)
    ldapServer.bindToServer()
    print ldapServer.getAllUsers()

if __name__ == "__main__":
    main(sys.argv)

