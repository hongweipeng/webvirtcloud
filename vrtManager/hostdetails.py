import time
from vrtManager.connection import wvmConnect
from vrtManager.util import get_xml_path



def cpu_version(doc):
    for info in doc.xpath('/sysinfo/processor/entry'):
        elem = info.xpath('@name')[0]
        if elem == 'version':
            return info.text
    return 'Unknown'


class wvmHostDetails(wvmConnect):
    def get_memory_usage(self):
        """
        Function return memory usage on node.
        """
        # get_all_mem = self.wvm.getInfo()[1] * 1048576
        get_freemem = self.wvm.getMemoryStats(-1, 0)
        if type(get_freemem) == dict:
            # free = (get_freemem.values()[0] +
            #         get_freemem.values()[2] +
            #         get_freemem.values()[3]) * 1024
            # percent = (100 - ((free * 100) / get_all_mem))
            # usage = (get_all_mem - free)
            # mem_usage = {'usage': usage, 'percent': percent}
            free = (get_freemem['free'] +
                    get_freemem['buffers'] +
                    get_freemem['cached'])
            percent = 100 - (free * 100 / get_freemem['total'])
            usage = (get_freemem['total'] - free) * 1024
            mem_usage = {'usage': usage, 'percent': percent}
        else:
            mem_usage = {'usage': None, 'percent': None}
        return mem_usage

    def get_cpu_usage(self):
        """
        Function return cpu usage on node.
        """
        prev_idle = 0
        prev_total = 0
        diff_usage = None

        #if type(cpu) == dict:
        for num in range(2):
            cpu = self.wvm.getCPUStats(-1, 0)
            idle = cpu['idle']
            total = sum(cpu.values())
            diff_idle = idle - prev_idle
            diff_total = total - prev_total
            diff_usage = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10
            prev_total = total
            prev_idle = idle
            if num == 0:
                time.sleep(1)
            else:
                if diff_usage < 0:
                    diff_usage = 0
        #else:
        #    return {'usage': None}
        return {'usage': diff_usage}

    def get_node_info(self):
        """
        Function return host server information: hostname, cpu, memory, ...
        """
        info = []
        info.append(self.wvm.getHostname()) # hostname
        info.append(self.wvm.getInfo()[0]) # architecture
        info.append(self.wvm.getInfo()[1] * 1048576) # memory
        info.append(self.wvm.getInfo()[2]) # cpu core count
        info.append(get_xml_path(self.wvm.getSysinfo(0), func=cpu_version)) # cpu version
        info.append(self.wvm.getURI()) #uri
        return info

    def hypervisor_type(self):
        """Return hypervisor type"""
        return get_xml_path(self.get_cap_xml(), "/capabilities/guest/arch/domain/@type")
