import os
from urllib.parse import urlparse
import python_socks

def get_proxy():
    proxy_str = os.getenv("TG_PROXY")
    if not proxy_str:
        return None
    parsed = urlparse(proxy_str)
    if not parsed.scheme or not parsed.hostname or not parsed.port:
        return None

    scheme = parsed.scheme.lower()
    if scheme == "socks5":
        proxy_type = python_socks.ProxyType.SOCKS5
    elif scheme == "http":
        proxy_type = python_socks.ProxyType.HTTP
    else:
        return None

    proxy = {
        "proxy_type": proxy_type,
        "addr": parsed.hostname,
        "port": parsed.port,
        "rdns": True,
    }
    if parsed.username and parsed.password:
        proxy["username"] = parsed.username
        proxy["password"] = parsed.password
    return proxy
