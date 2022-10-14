"""
The client and domain model to work with schedule, stations and shows.
"""

from cro.schedule._client import Client as Client
from cro.schedule._domain import (
    Schedule as Schedule,
    Show as Show,
    Station as Station,
)


__all__ = tuple(["Client", "Station", "Show", "Schedule"])


__version__ = "1.0.1"
