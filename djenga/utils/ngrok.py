import requests
import logging


__all__ = [
    'get_ngrok_url',
]
logger = logging.getLogger(__name__)


def get_ngrok_url():
    """
    Provides a handy helper to get the ngrok public url
    of our dev environment (during debug/testing).
    ngrok has an API that allows us to get our public
    url.  This helper function uses that api call to
    find our public URL and returns it (if ngrok is running).
    Returns None if the function cannot connect to ngrok
    :return: str
    """
    url = None
    response = None
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        data = response.json()
        url = data['tunnels'][0]['public_url']
        url = url.replace('http:', 'https:')
        logger.info('NGROK URL = %s', url)
    except:  # noqa: E722
        try:
            if response:
                content = response.content.decode('utf8')
                x = content.find('https')
                y = content.find('\\"', x + 1)
                url = content[x:y]
        except:  # noqa: E722
            pass
    return url
