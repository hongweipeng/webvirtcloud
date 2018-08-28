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
from vrtManager import util
import mimetypes

compute = computes_models.Compute.objects.get(pk=1)


conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           'win08-teach')



snapshot_list = conn.instance.snapshotListNames(0)
#print(snapshot_list)
snap_coll = []         # [{'created': <int>, 'snap':snap_obj}, ...]
# 收集快照信息
for snapshot_name in snapshot_list:
    snap = conn.instance.snapshotLookupByName(snapshot_name, 0)
    snap_time_create = util.get_xml_path(snap.getXMLDesc(0), "/domainsnapshot/creationTime")
    snap_time_create = int(snap_time_create)
    snap_coll.append({
        'created': int(snap_time_create),
        'snap': snap,
        'datetime': datetime.datetime.fromtimestamp(snap_time_create)
    })
print(len(snap_coll))

# 若快照数量高于7个，删除旧的快照
if len(snap_coll) >= 7:
    snap_coll = sorted(snap_coll, reverse=True, key=lambda d:d['created'])
    for item in snap_coll[7:]:
        snap = item['snap']
        snap.delete(0)

# 创建一个新的快照
snap_name = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
conn.create_snapshot(snap_name)
conn.close()





