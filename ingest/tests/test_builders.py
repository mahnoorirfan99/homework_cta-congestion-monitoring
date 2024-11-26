import functools

import cta
import cta.builders
import cta.builders.alert
import pytest


def test__constructAPI() -> None:
    baseURL: str = "https://google.com"
    partial: functools.partial = functools.partial(
        cta.builders._constructAPI,
        url=baseURL,
    )

    assert partial() == f"{baseURL}?"
    assert partial(test=1) == f"{baseURL}?test=1"
    assert partial(test=None) == f"{baseURL}?"
    assert partial(test1=1, test2=None) == f"{baseURL}?test1=1"
    assert partial(test1=1, test2=None, test3=3) == f"{baseURL}?test1=1&test3=3"

def test___safeJoin()   ->  None:
    partial: functools.partial = functools.partial(cta.builders._safeJoin)

    assert partial(data="test") == "test"
    assert partial(data="test", sep="&") == "test"

    assert partial(data=["test"]) == "test"
    assert partial(data=["test"], sep="&") == "test"
    assert partial(data=["foo", "bar"]) == "foo,bar"
    assert partial(data=["foo", "bar"], sep="&") == "foo&bar"

    assert partial(data=1) == None


def test_AlertAPIBuilder() -> None:
    partial: functools.partial = functools.partial(cta.builders.alert.AlertAPIBuilder)

    assert isinstance(partial(), cta.builders.alert.AlertAPIBuilder)
    assert partial().outputType == "json"
    assert partial(outputType="xml").outputType == "xml"

    with pytest.raises(ValueError):
        partial(outputType="test")


def test_AlertAPIBuilder_buildRouteStatusAPIURL():
    baseURL: str = "http://www.transitchicago.com/api/1.0/routes.aspx"
    builder: cta.builders.alert.AlertAPIBuilder = cta.builders.alert.AlertAPIBuilder()

    partial: functools.partial = functools.partial(builder.buildRouteStatusAPIURL)

    assert partial() == f"{baseURL}?outputType=json"

    assert partial(type="bus") == f"{baseURL}?outputType=json&type=bus"
    assert partial(type=["bus"]) == f"{baseURL}?outputType=json&type=bus"
    assert (
        partial(type=["bus", "train"]) == f"{baseURL}?outputType=json&type=bus%2Ctrain"
    )

    assert partial(routeid="test") == f"{baseURL}?outputType=json&routeid=test"
    assert partial(routeid=["test"]) == f"{baseURL}?outputType=json&routeid=test"
    assert (
        partial(routeid=["test", "bar"])
        == f"{baseURL}?outputType=json&routeid=test%2Cbar"
    )
