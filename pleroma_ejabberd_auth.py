import sys
import struct
import http.client
from base64 import b64encode
import logging


PLEROMA_HOST = "127.0.0.1"
PLEROMA_PORT = "4000"
AUTH_ENDPOINT = "/api/v1/accounts/verify_credentials"
USER_ENDPOINT = "/api/v1/accounts"
LOGFILE = "/var/log/ejabberd/pleroma_auth.log"

logging.basicConfig(filename=LOGFILE, level=logging.INFO)


def create_connection():
    return http.client.HTTPConnection(PLEROMA_HOST, PLEROMA_PORT)


def verify_credentials(user: str, password: str) -> bool:
    user_pass_b64 = b64encode("{}:{}".format(
        user, password).encode('utf-8')).decode("ascii")
    params = {}
    headers = {
        "Authorization": "Basic {}".format(user_pass_b64)
    }

    try:
        conn = create_connection()
        conn.request("GET", AUTH_ENDPOINT, params, headers)

        response = conn.getresponse()
        if response.status == 200:
            return True

        return False
    except Exception as e:
        logging.error("Can not connect: %s", str(e))
        return False


def does_user_exist(user: str) -> bool:
    try:
        conn = create_connection()
        conn.request("GET", "{}/{}".format(USER_ENDPOINT, user))

        response = conn.getresponse()
        if response.status == 200:
            return True

        return False
    except Exception as e:
        logging.error("Can not connect: %s", str(e))
        return False


def auth(username: str, server: str, password: str) -> bool:
    return verify_credentials(username, password)


def isuser(username, server):
    return does_user_exist(username)


def read():
    (pkt_size,) = struct.unpack('>H', bytes(sys.stdin.read(2), encoding='utf8'))
    pkt = sys.stdin.read(pkt_size)
    cmd = pkt.split(':')[0]
    if cmd == 'auth':
        username, server, password = pkt.split(':', 3)[1:]
        write(auth(username, server, password))
    elif cmd == 'isuser':
        username, server = pkt.split(':', 2)[1:]
        write(isuser(username, server))
    elif cmd == 'setpass':
        # u, s, p = pkt.split(':', 3)[1:]
        write(False)
    elif cmd == 'tryregister':
        # u, s, p = pkt.split(':', 3)[1:]
        write(False)
    elif cmd == 'removeuser':
        # u, s = pkt.split(':', 2)[1:]
        write(False)
    elif cmd == 'removeuser3':
        # u, s, p = pkt.split(':', 3)[1:]
        write(False)
    else:
        write(False)


def write(result):
    if result:
        sys.stdout.write('\x00\x02\x00\x01')
    else:
        sys.stdout.write('\x00\x02\x00\x00')
    sys.stdout.flush()


if __name__ == "__main__":
    logging.info("Starting pleroma ejabberd auth daemon...")
    while True:
        try:
            read()
        except Exception as e:
            logging.error(
                "Error while processing data from ejabberd %s", str(e))
