from dataclasses import dataclass
from datetime import datetime

import requests

REQUEST_TIMEOUT = 30


@dataclass(frozen=True)
class Credentials:
    host: str
    user: str
    password: str


def _build_session(creds: Credentials) -> requests.Session:
    session = requests.Session()
    session.auth = requests.auth.HTTPDigestAuth(creds.user, creds.password)
    return session


def _get(creds: Credentials, url: str) -> str:
    with _build_session(creds) as session:
        res = session.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        return res.text


def get_system_info(creds: Credentials) -> str:
    url = f"http://{creds.host}/cgi-bin/magicBox.cgi?action=getSystemInfo"
    return _get(creds, url)


def get_config_sip(creds: Credentials) -> str:
    url = f"http://{creds.host}/cgi-bin/configManager.cgi?action=getConfig&name=SIP"
    return _get(creds, url)


def get_current_time(creds: Credentials) -> str:
    url = f"http://{creds.host}/cgi-bin/global.cgi?action=getCurrentTime"
    return _get(creds, url)


def set_current_time(creds: Credentials) -> str:
    now = datetime.today()
    current_datetime = f"{now.strftime('%Y-%m-%d')}%20{now.strftime('%H:%M:%S')}"
    url = (
        f"http://{creds.host}/cgi-bin/global.cgi"
        f"?action=setCurrentTime&time={current_datetime}"
    )
    return _get(creds, url)


def reboot(creds: Credentials) -> str:
    url = f"http://{creds.host}/cgi-bin/magicBox.cgi?action=reboot"
    return _get(creds, url) + "\n"
