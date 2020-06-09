# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = event_wrapper_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")
EventType = TypeVar("EventType")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Event:
    type: str
    channel: str
    user: str
    text: str
    ts: str
    event_ts: str
    channel_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        channel = from_str(obj.get("channel"))
        user = from_str(obj.get("user"))
        text = from_str(obj.get("text"))
        ts = from_str(obj.get("ts"))
        event_ts = from_str(obj.get("event_ts"))
        channel_type = from_str(obj.get("channel_type"))
        return Event(type, channel, user, text, ts, event_ts, channel_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["channel"] = from_str(self.channel)
        result["user"] = from_str(self.user)
        result["text"] = from_str(self.text)
        result["ts"] = from_str(self.ts)
        result["event_ts"] = from_str(self.event_ts)
        result["channel_type"] = from_str(self.channel_type)
        return result


@dataclass
class EventWrapper:
    token: str
    team_id: str
    api_app_id: str
    event: Event
    type: str
    authed_users: List[str]
    event_id: str
    event_time: int

    @staticmethod
    def from_dict(obj: Any) -> 'EventWrapper':
        assert isinstance(obj, dict)
        token = from_str(obj.get("token"))
        team_id = from_str(obj.get("team_id"))
        api_app_id = from_str(obj.get("api_app_id"))
        event = Event.from_dict(obj.get("event"))
        type = from_str(obj.get("type"))
        authed_users = from_list(from_str, obj.get("authed_users"))
        event_id = from_str(obj.get("event_id"))
        event_time = from_int(obj.get("event_time"))
        return EventWrapper(token, team_id, api_app_id, event, type, authed_users, event_id, event_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["token"] = from_str(self.token)
        result["team_id"] = from_str(self.team_id)
        result["api_app_id"] = from_str(self.api_app_id)
        result["event"] = to_class(Event, self.event)
        result["type"] = from_str(self.type)
        result["authed_users"] = from_list(from_str, self.authed_users)
        result["event_id"] = from_str(self.event_id)
        result["event_time"] = from_int(self.event_time)
        return result


def event_wrapper_from_dict(s: Any) -> EventWrapper:
    return EventWrapper.from_dict(s)


def event_wrapper_to_dict(x: EventWrapper) -> Any:
    return to_class(EventWrapper, x)
