from collections.abc import Iterable
from typing import Any

from aioinject import Provider

Providers = Iterable[Provider[Any]]
