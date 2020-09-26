from coffee.mqtt.topic import Topic

def test_property():
    t = Topic("foo/+bar")
    assert t.topic == "foo/+"
    t.topic = "foo/+/baz"
    assert t.topic == "foo/+"
    t.pattern = "foo/+bar/baz"
    assert t.pattern == "foo/+bar/baz"
    assert t.topic == "foo/+/baz"

def test_match():
    #"matches() supports patterns with no wildcards"
    t = Topic("foo/bar/baz")
    assert t.match("foo/bar/baz") == True
    #"matches() doesn't match different topics"
    assert t.match("baz/bar/foo") == False
    #"matches() supports patterns with # at the beginning"
    t = Topic("#")
    assert t.match("foo/bar/baz") == True
    #"matches() supports patterns with # at the end"
    t = Topic("foo/#")
    assert t.match("foo/bar/baz") == True
    #"matches() supports patterns with # at the end and topic has no children"
    t = Topic("foo/bar/#")
    assert t.match("foo/bar") == True
    #"matches() doesn't support # wildcards with more after them"
    t = Topic("#/bar/baz")
    assert t.match("foo/bar/baz") == False
    #"matches() supports patterns with + at the beginning"
    t = Topic("+/bar/baz")
    assert t.match("foo/bar/baz") == True
    #"matches() supports patterns with + at the end"
    t = Topic("foo/bar/+")
    assert t.match("foo/bar/baz") == True
    #"matches() supports patterns with + in the middle"
    t = Topic("foo/+/baz")
    assert t.match("foo/bar/baz") == True
    #"matches() supports patterns multiple wildcards"
    t = Topic("foo/+/#")
    assert t.match("foo/bar/baz") == True
    #"matches() supports named wildcards"
    t = Topic("foo/+something/#else")
    assert t.match("foo/bar/baz") == True
    #"matches() supports leading slashes"
    t = Topic("/foo/bar")
    assert t.match("/foo/bar") == True
    assert t.match("/bar/foo") == False

def test_extract():
    #"extract() returns empty object of there's nothing to extract"
    t = Topic("foo/bar/baz")
    res = t.extract("foo/bar/baz")
    assert res == {}
    #"extract() returns empty object if wildcards don't have label"
    t = Topic("foo/+/#")
    res = t.extract("foo/bar/baz")
    assert res == {}
    #"extract() returns object with an array for # wildcard"
    t = Topic("foo/#something")
    res = t.extract("foo/bar/baz")
    assert res == { "something": ["bar", "baz"] }
    #"extract() returns object with a string for + wildcard"
    t = Topic("foo/+hello/+world")
    res = t.extract("foo/bar/baz")
    assert res == { "hello": "bar", "world": "baz" }
    #"extract() parses params from all wildcards"
    t = Topic("+hello/+world/#wow")
    res = t.extract("foo/bar/baz/fizz")
    assert res == { "hello": "foo", "world": "bar", "wow": ["baz", "fizz"] }

def test_build():
    #"build() fills in pattern with both types of wildcards"
    t = Topic("foo/+hello/#world")
    assert t.build({
        "hello": "Hello",
        "world": ["the", "world", "wow"],
    }) == "foo/Hello/the/world/wow"
    #"fill() fills missing + params with undefined"
    t = Topic("foo/+hello")
    assert t.build({}) == "foo/undefined"
    #"build() ignores empty # params"
    t = Topic("foo/#hello")
    assert t.build({}) == "foo"
    #"build() ignores non-named # params"
    t = Topic("foo/#")
    assert t.build({}) == "foo"
    #"build() uses `undefined` for non-named + params"
    t = Topic("foo/+")
    assert t.build({}) == "foo/undefined"
