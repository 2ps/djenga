import platform
import os


__all__ = [ 'get_memory_usage', 'get_peak_memory_usage' ]


def get_memory_usage():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
    except ImportError:
        return None


def get_peak_memory_usage():
    os_name = platform.platform(terse=True).lower()
    if 'windows' in os_name:
        try:
            from wmi import WMI
            w = WMI('.')
            result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
            return int(result[0].WorkingSet)
        except ImportError:
            return None
    try:
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except ImportError:
        return None
