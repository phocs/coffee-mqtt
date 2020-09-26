from coffee.mqtt.pattern import TopicPattern

def test_matches():
    #"matches() supports patterns with no wildcards"
    assert TopicPattern.matches("foo/bar/baz", "foo/bar/baz") == True
    #"matches() doesn't match different topics"
    assert TopicPattern.matches("foo/bar/baz", "baz/bar/foo") == False
    #"matches() supports patterns with # at the beginning"
    assert TopicPattern.matches("#", "foo/bar/baz") == True
    #"matches() supports patterns with # at the end"
    assert TopicPattern.matches("foo/#", "foo/bar/baz") == True
    #"matches() supports patterns with # at the end and topic has no children"
    assert TopicPattern.matches("foo/bar/#", "foo/bar") == True
    #"matches() doesn't support # wildcards with more after them"
    assert TopicPattern.matches("#/bar/baz", "foo/bar/baz") == False
    #"matches() supports patterns with + at the beginning"
    assert TopicPattern.matches("+/bar/baz", "foo/bar/baz") == True
    #"matches() supports patterns with + at the end"
    assert TopicPattern.matches("foo/bar/+", "foo/bar/baz") == True
    #"matches() supports patterns with + in the middle"
    assert TopicPattern.matches("foo/+/baz", "foo/bar/baz") == True
    #"matches() supports patterns multiple wildcards"
    assert TopicPattern.matches("foo/+/#", "foo/bar/baz") == True
    #"matches() supports named wildcards"
    assert TopicPattern.matches("foo/+something/#else", "foo/bar/baz") == True
    #"matches() supports leading slashes"
    assert TopicPattern.matches("/foo/bar", "/foo/bar") == True
    assert TopicPattern.matches("/foo/bar", "/bar/foo") == False


def test_extract():
    #"extract() returns empty object of there's nothing to extract"
    res = TopicPattern.extract("foo/bar/baz", "foo/bar/baz")
    assert res == {}
    #"extract() returns empty object if wildcards don't have label"
    res = TopicPattern.extract("foo/+/#", "foo/bar/baz")
    assert res == {}
    #"extract() returns object with an array for # wildcard"
    res = TopicPattern.extract("foo/#something", "foo/bar/baz")
    assert res == { "something": ["bar", "baz"] }
    #"extract() returns object with a string for + wildcard"
    res = TopicPattern.extract("foo/+hello/+world", "foo/bar/baz")
    assert res == { "hello": "bar", "world": "baz" }
    #"extract() parses params from all wildcards"
    res = TopicPattern.extract("+hello/+world/#wow", "foo/bar/baz/fizz")
    assert res == { "hello": "foo", "world": "bar", "wow": ["baz", "fizz"] }

def test_matches_extract():
    #"exec() returns None if it doesn't match",
    res = None if TopicPattern.matches("hello/world", "foo/bar/baz") == False \
               else TopicPattern.extract("hello/world", "foo/bar/baz")
    assert res == None
    #"exec() returns params if they can be parsed"
    res = None if TopicPattern.matches("foo/+hello/#world", "foo/bar/baz") == False \
               else TopicPattern.extract("foo/+hello/#world", "foo/bar/baz")
    assert res == { "hello": "bar", "world": ["baz"]}

def test_clean():
    #"clean() removes parameter names"
    assert TopicPattern.clean("hello/+param1/world/#param2") == "hello/+/world/#"
    #"clean() works when there aren't any parameter names"
    assert TopicPattern.clean("hello/+/world/#") == "hello/+/world/#"

def test_fill():
    #"fill() fills in pattern with both types of wildcards"
    assert TopicPattern.fill("foo/+hello/#world", {
        "hello": "Hello",
        "world": ["the", "world", "wow"],
    }) == "foo/Hello/the/world/wow"
    #"fill() fills missing + params with undefined"
    assert TopicPattern.fill("foo/+hello", {}) == "foo/undefined"
    #"fill() ignores empty # params"
    assert TopicPattern.fill("foo/#hello", {}) == "foo"
    #"fill() ignores non-named # params"
    assert TopicPattern.fill("foo/#", {}) == "foo"
    #"fill() uses `undefined` for non-named + params"
    assert TopicPattern.fill("foo/+", {}) == "foo/undefined"
