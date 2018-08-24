import os
import datetime
import libvirt
from PIL import Image
import io
import django
import base64
os.environ['DJANGO_SETTINGS_MODULE'] = 'webvirtcloud.settings'
django.setup()
from computes import models as computes_models
from vrtManager.instance import  wvmInstance
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.connection import connection_manager
import mimetypes

compute = computes_models.Compute.objects.get(pk=1)


conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           'centos7-hwp-dev')
#print(type(conn.instance))
#print(dir(conn.instance))

st = conn.wvm.newStream(0)
mime = conn.instance.screenshot(st, 0)

def saver(stream, data, file_):
    return file_.write(data)


#ext = mimetypes.guess_extension(mime) or '.ppm'

with io.BytesIO() as f, io.BytesIO() as c:
    st.recvAll(saver, f)
    img = Image.open(f)
    img.save(c, format='PNG')
    byte_data = c.getvalue()
    base64_str = base64.b64encode(byte_data)
    print(base64_str.decode('utf8'))
    img.close()



ret = st.finish()




print(ret)
#
# conn.create_snapshot(datetime.datetime.now().strftime('%m-%d %H:%M:%S'))
# print(compute.name)

# d = [dict(name=1), dict(name=2)]
# sorted(d)

# def snap_crontab():
#     computes = computes_models.Compute.objects.all()
#     for compute in computes:
#         # 忽略不可连接的宿主
#         if connection_manager.host_is_up(compute.type, compute.hostname) is not True:
#             continue
#
#         # conn = wvmInstance(compute.hostname,
#         #                    compute.login,
#         #                    compute.password,
#         #                    compute.type,
#         #                    vname)
#         conn = wvmHostDetails(compute, compute.login, compute.password, compute.type)
#         instances = conn.get_instances()
#         # print(instances)
#         # print(type(instances[0]))
#
# snap_crontab()
