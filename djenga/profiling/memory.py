
import os
import resource


__all__ = [ 'get_memory_usage', 'get_peak_memory_usage' ]


def get_memory_usage():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
    except ImportError:
        return None


def get_peak_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
