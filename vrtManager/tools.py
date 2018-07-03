import hashlib
from webvirtcloud.settings import WS_PORT
from webvirtcloud.settings import WS_PUBLIC_HOST
from webvirtcloud.settings import VNC_TOKENS_FILE

def set_proxy(token, vnc_host, vnc_port):
    vnc_token_lines = []
    with open(VNC_TOKENS_FILE, "r+") as f:
        for line in [l.strip() for l in f.readlines()]:
            if line and not line.startswith('#'):
                ttoken, target = line.split(': ')
                vnc_ip, _vnc_port = target.split(':')
                if vnc_ip == vnc_host and vnc_port == _vnc_port:
                    if token == ttoken:
                        break  # 已配置，跳过
                else:
                    vnc_token_lines.append(line)
        else:
            vnc_token_lines.append("%s: %s:%s" % (token, vnc_host, vnc_port))
            f.seek(0)
            f.truncate()  # 清空文件
            f.write("\n".join(vnc_token_lines))
    return True


def md5(line: str) -> str:
    return hashlib.md5(line.encode('latin1')).hexdigest()

if __name__ == '__main__':
    print(md5("jxkj123" + chr(163) + str(1) + "jxkj"))
