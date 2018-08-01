import logging


__all__  = [
    'ZeepHttpsFilter',
    'CeleryRestoringFilter',
]


class ZeepHttpsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        result: bool = record.name.startswith('zeep.wsdl.bindings')
        result &= record.levelno == logging.WARNING
        result &= record.msg.startswith('Forcing soap:address location')
        return not result


class CeleryRestoringFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        result = record.name.startswith('celery.redirected')
        result &= record.msg.startswith('Restoring')
        result &= record.msg.endswith('unacknowledged message(s)')
        return not result
