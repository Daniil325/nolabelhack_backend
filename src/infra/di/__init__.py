from dishka import make_async_container

import importlib
import pkgutil
from pathlib import Path
from dishka import Provider

def load_providers():
    providers = []
    for _, module_name, _ in pkgutil.walk_packages([str(Path(__file__).parent)], prefix=f"{__name__}."):
        try:
            module = importlib.import_module(module_name)
            for item_name in dir(module):
                item = getattr(module, item_name)
                if isinstance(item, type) and issubclass(item, Provider) and item is not Provider:
                    providers.append(item())
        except ImportError as e:
            print(f"Failed to import {module_name}: {e}")
    return providers

providers = load_providers()

container = make_async_container(*providers)