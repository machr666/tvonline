import base64
import uuid

f = open('cookiesecret.txt','w+')
f.write(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
f.close
