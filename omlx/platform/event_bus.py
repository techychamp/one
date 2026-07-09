# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass, field
import datetime
import uuid
import logging
from typing import Callable, DefaultDict, List
from collections import defaultdict

logger = logging.getLogger("omlx.platform.event_bus")

@dataclass(frozen=True)
class PlatformEvent:
    name: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data: dict = field(default_factory=dict)

class PlatformEventBus:
    def __init__(self) -> None:
        self._listeners: DefaultDict[str, List[Callable[[PlatformEvent], None]]] = defaultdict(list)
        self._events: List[PlatformEvent] = []

    def subscribe(self, event_name: str, listener: Callable[[PlatformEvent], None]) -> None:
        self._listeners[event_name].append(listener)

    def publish(self, event: PlatformEvent) -> None:
        self._events.append(event)
        logger.debug("Publishing event %s: %s", event.name, event.data)
        for listener in list(self._listeners[event.name]):
            try:
                listener(event)
            except Exception as e:
                logger.error("Error in event listener for %s: %s", event.name, e)
        for listener in list(self._listeners["*"]):
            try:
                listener(event)
            except Exception as e:
                logger.error("Error in wildcard listener: %s", e)
