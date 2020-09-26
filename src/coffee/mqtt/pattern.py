
class TopicPattern:
    _SEPARATOR = "/"
    _WILDCARD_MULTI = "#"
    _WILDCARD_SINGLE = "+"

    @staticmethod
    def matches(pattern, topic):
        pattern_segments = pattern.split(TopicPattern._SEPARATOR)
        topic_segments = topic.split(TopicPattern._SEPARATOR)

        pattern_len = len(pattern_segments)
        topic_len = len(topic_segments)

        for i in range(0, pattern_len):
            current_pattern = pattern_segments[i]
            pattern_wc = current_pattern[0] \
                            if 0 < len(current_pattern) else None
            current_topic = topic_segments[i] \
                            if i < len(topic_segments) else None

            if not current_topic and not current_pattern:
                continue

            if not current_topic and \
               current_pattern != TopicPattern._WILDCARD_MULTI:
                return False

            # Only allow # at end
            if pattern_wc == TopicPattern._WILDCARD_MULTI:
                return i == (pattern_len - 1)

            if pattern_wc != TopicPattern._WILDCARD_SINGLE and \
               current_pattern != current_topic:
                return False

        return pattern_len == topic_len

    @staticmethod
    def extract(pattern, topic):
        params = {}
        pattern_segments = pattern.split(TopicPattern._SEPARATOR)
        topic_segments = topic.split(TopicPattern._SEPARATOR)

        pattern_len = len(pattern_segments)

        for i in range(0, pattern_len):
            current_pattern = pattern_segments[i]
            pattern_wc = current_pattern[0] \
                            if 0 < len(current_pattern) else None

            if len(current_pattern) == 1:
                continue

            if pattern_wc == TopicPattern._WILDCARD_MULTI:
                params[current_pattern[1:]] = topic_segments[i:]
                break
            elif pattern_wc == TopicPattern._WILDCARD_SINGLE:
                params[current_pattern[1:]] = topic_segments[i]

        return params

    @staticmethod
    def clean(pattern):
        pattern_segments = pattern.split(TopicPattern._SEPARATOR)
        pattern_len = len(pattern_segments)

        cleaned_segments = []

        for i in range(0, pattern_len):
            current_pattern = pattern_segments[i]
            pattern_wc = current_pattern[0] \
                            if 0 < len(current_pattern) else None

            if pattern_wc == TopicPattern._WILDCARD_MULTI:
                cleaned_segments.append(TopicPattern._WILDCARD_MULTI)
            elif pattern_wc == TopicPattern._WILDCARD_SINGLE:
                cleaned_segments.append(TopicPattern._WILDCARD_SINGLE)
            else:
                cleaned_segments.append(current_pattern)

        return TopicPattern._SEPARATOR.join(cleaned_segments)

    @staticmethod
    def fill(pattern, params):
        pattern_segments = pattern.split(TopicPattern._SEPARATOR)
        pattern_len = len(pattern_segments)

        result = []

        for i in range(0, pattern_len):
            current_pattern = pattern_segments[i]
            pattern_wc = current_pattern[0] \
                            if 0 < len(current_pattern) else None
            pattern_param = current_pattern[1:]
            param_value = params.get(pattern_param, None)

            if pattern_wc == TopicPattern._WILDCARD_MULTI:
                # Check that it isn't undefined
                if param_value != None:
                    # Ensure it's an array
                    result.append(TopicPattern._SEPARATOR.join(
                        [] + param_value    if isinstance(param_value, list) \
                                            else [param_value]
                    ))
                # Since # wildcards are always at the end, break out of the loop
                break
            elif pattern_wc == TopicPattern._WILDCARD_SINGLE:
                # Coerce param into a string, missing params will be undefined
                result.append("" + param_value if param_value else "undefined")
            else:
                 result.append(current_pattern)

        return TopicPattern._SEPARATOR.join(result)
