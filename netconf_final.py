from ncclient import manager
from xml.dom.minidom import parseString
import xmltodict

xe = {
    'ip':'192.168.118.138',
    'port':'830',
    'username':'admin',
    'password':'cisco'
}

user_choice = input("Hey there, welcome to CSR Configuration utility...\n1. Interface Configuration\n2. Interface Details\nPlease Enter Your Choice: ")

if user_choice == str(1):
    netconf_template = '''
    <config>
        <interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <description>{desc}</description>
                <type xmlns:ianaift = "urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>true</enabled>
                <ipv4 xmlns = "urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip}</ip>
                        <netmask>{mask}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    '''

    new_loopback = {
        'interface':'Loopback' + input("Enter the Loopback Interface Number: "),
        'description':input("Enter the description: "),
        'ip':input("Enter the ip address: "),
        'mask':input("Enter the mask: ")
    }

    #Supply the user details into the xml template
    interface_payload = netconf_template.format(
        name = new_loopback['interface'],
        desc = new_loopback['description'],
        ip = new_loopback['ip'],
        mask = new_loopback['mask']
    )

    with manager.connect(
        host = xe['ip'],
        port = xe['port'],
        username = xe['username'],
        password = xe['password'],
        hostkey_verify = False
        ) as abc:

        query = abc.edit_config(interface_payload, target = "running")
        print(query)

        print("Your Interface is created")

elif user_choice == str(2):
    netconf_filter = '''
    <filter>
        <interfaces xmlns = "urn:ietf:params:xml:ns:yang::ietf-interfaces">
            <interface>

            </interface>
        </interfaces>
    </filter>
    '''
    with manager.connect(
        host = xe['ip'],
        port = xe['port'],
        username = xe['username'],
        password = xe['password'],
        hostkey_verify = False
        ) as abc:

        query = abc.get_config(filter = netconf_filter, source = "running")

    dictout = xmltodict.parse(query.xml)
    all_interfaces = dictout['rpc-reply']['data']['interfaces']['interface']

    for interface in all_interfaces:
        try:
            ip = interface['ipv4']['address']['ip']
        except:
            ip = "Not Configured"
        print("The {}'s is enabled status is {} and the IP address is {}".format(
            interface['name'],
            interface['enabled'],
            ip
        ))

else:
    print("User input not valid")
    pass







