try:
    from apinkcore.tests.test_api import suite
except ImportError:
    from .test_api import suite

__all__ = ['suite']
