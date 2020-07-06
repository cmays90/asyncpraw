from json import dumps

from pytest import raises

from asyncpraw.models import (
    SubredditWidgets,
    SubredditWidgetsModeration,
    Widget,
    WidgetModeration,
    Subreddit,
)
from asyncpraw.models.reddit.widgets import WidgetEncoder
from asyncpraw.models.base import AsyncPRAWBase

from ... import UnitTest


class TestWidgetEncoder(UnitTest):
    def test_bad_encode(self):
        data = [
            1,
            "two",
            SubredditWidgetsModeration(
                Subreddit(self.reddit, display_name="subreddit"), self.reddit
            ),
        ]
        with raises(TypeError):
            dumps(data, cls=WidgetEncoder)  # should throw TypeError

    def test_good_encode(self):
        data = [
            1,
            "two",
            AsPRAWBase(self.reddit, _data={"_secret": "no", "3": 3}),
            AsyncPRAWBase(self.reddit, _data={"_secret": "no", "3": 3}),
            self.reddit.subreddit("four"),
        ]
        assert '[1, "two", {"3": 3}, "four"]' == dumps(data, cls=WidgetEncoder)


class TestWidgets(UnitTest):
    def test_subredditwidgets_mod(self):
        sw = SubredditWidgets(Subreddit(self.reddit, "fake_subreddit"))
        assert isinstance(sw.mod, SubredditWidgetsModeration)

    def test_widget_mod(self):
        w = Widget(self.reddit, {})
        assert isinstance(w.mod, WidgetModeration)
        assert w.mod.widget == w
