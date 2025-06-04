import re


def split_text(text, min_length=10, max_length=500, split_pattern="."):
    """Split *text* into manageable pieces.

    Parameters
    ----------
    text : str
        The text to be split.
    min_length : int, optional
        Minimum length for a segment. Shorter segments are merged with the
        following one.
    max_length : int, optional
        Maximum length for a segment. Longer segments are split by spaces.
    split_pattern : str, optional
        Regular expression used to split the initial text. By default it
        splits on a period. Newlines are always considered as delimiters.

    Returns
    -------
    str
        Newline separated string containing the final segments.
    """

    # 1. Split by the provided pattern (plus newlines)
    raw_segments = re.split(fr"{split_pattern}|\n", text)

    # Trim whitespace and discard empty segments from the ends
    segments = [seg.strip() for seg in raw_segments if seg.strip()]

    # 2. Split further if a segment is longer than max_length
    def split_long_segment(segment, max_len):
        """
        Given a string 'segment', split it by spaces so that
        each sub-segment is at most max_len characters.
        """
        words = segment.split()
        sub_segments = []
        current = ""
        for word in words:
            if not current:
                current = word
            else:
                # 1 extra character for the space before 'word'
                if len(current) + 1 + len(word) <= max_len:
                    current += " " + word
                else:
                    sub_segments.append(current)
                    current = word
        # Append whatever remains
        if current:
            sub_segments.append(current)
        return sub_segments

    expanded_segments = []
    for seg in segments:
        # If a segment is larger than max_length, split it by spaces
        if len(seg) > max_length:
            expanded_segments.extend(split_long_segment(seg, max_length))
        else:
            expanded_segments.append(seg)

    # 3. Merge segments smaller than min_length with the next one
    final_segments = []
    i = 0
    while i < len(expanded_segments):
        current_seg = expanded_segments[i]
        if len(current_seg) < min_length:
            # Merge with the next segment if possible
            if i + 1 < len(expanded_segments):
                merged = current_seg + " " + expanded_segments[i + 1]
                final_segments.append(merged.strip())
                i += 2  # Skip the next one, because we've merged it
            else:
                # It's the last segment and also short; just append it
                final_segments.append(current_seg)
                i += 1
        else:
            final_segments.append(current_seg)
            i += 1

    #return final_segments
    return "\n".join(final_segments)
