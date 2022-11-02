try:
    from .env import GeneralConfig
    from .env import GamefiConfig
    from .env import TOKENConfig
except ImportError as e:
    print(f"import configurations error: {str(e)}")
    from .test import GeneralConfig
    from .test import GamefiConfig
    from .test import TOKENConfig
