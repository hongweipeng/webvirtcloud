import time
import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from computes import models as computes_models
from vrtManager.connection import connection_manager
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.instance import wvmInstance
from vrtManager import util

scheduler = BackgroundScheduler()

def snap_crontab():
    computes = computes_models.Compute.objects.all()
    for compute in computes:
        # 忽略不可连接的宿主
        if connection_manager.host_is_up(compute.type, compute.hostname) is not True:
            continue

        conn = wvmHostDetails(compute.hostname, compute.login, compute.password, compute.type)
        instances = conn.get_instances()  # ['name1', 'name2']
        conn.close()

        for vname in instances:
            conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           vname)

            if conn.get_status() != 1:
                print("%s status is %s, skip" % (vname, conn.get_status()))
                continue

            snapshot_list = conn.instance.snapshotListNames(0)
            snap_coll = []         # [{'created': <int>, 'snap':snap_obj}, ...]
            # 收集快照信息
            for snapshot_name in snapshot_list:
                snap = conn.instance.snapshotLookupByName(snapshot_name, 0)
                snap_time_create = util.get_xml_path(snap.getXMLDesc(0), "/domainsnapshot/creationTime")
                snap_coll.append({
                    'created': int(snap_time_create),
                    'snap': snap
                })

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
    print("end snap_crontab")


scheduler.add_job(snap_crontab, 'cron', hour=5, minute=20, max_instances=1)
# scheduler.add_job(snap_crontab, 'interval', minutes=100, max_instances=1)

#snap_crontab()

