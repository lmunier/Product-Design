# -*-coding:Utf-8 -*

# File to return credentials stocked in another secured file

import re
import base64

def returnCred():
        # Get credentials from MySQL Python Agent config file
        fid = open('/home/ubuntu/pythonAgent.conf', 'r')
        ConfigFileBody = fid.read()
        fid.close()

        # Parse credentials
        mail = re.findall(r'MAIL\=(.*)\n', ConfigFileBody)[0]
        password = re.findall(r'PASS\=(.*)\n', ConfigFileBody)[0]

        my_password = base64.b64decode(password).decode('utf-8')

        return mail, my_password
