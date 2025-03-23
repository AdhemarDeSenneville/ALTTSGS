import re





def split_text(
        text, 
        rtf = 1.5,
        min_length=10, 
        obj_length=200,
        max_length=500,
        split_pattern=r'\.|\n',
        verbose = False
    ):
    

    # 1. Split by the pattern Trim whitespace and discard empty segments from the ends
    raw_segments = re.split(split_pattern, text)
    segments = [seg.strip() for seg in raw_segments if seg.strip()]

    for chunk in segments:
        if verbose: print(len(chunk), chunk)

        
    warmup = True
    final_chunk_list = []
    
    current_char_count = 0
    current_char_objectitive = min_length
    maximum_char_objectitive = min_length
    current_chunk = []

    for segment in segments:
        words = re.split(r'\s+', segment)
        number_words = len(words)

        if verbose: print(' = = = = = = = = = = = = Number of words',number_words, 'Number of chars', len(segment))

        for i, word in enumerate(words):

            current_char_count += len(word)
            current_chunk += [word]

            
            if current_char_count >= current_char_objectitive or i+1 == number_words:
                
                if verbose: print('Split:', current_chunk)
                if verbose: print('current_char_count:', current_char_objectitive,current_char_count)
                if current_char_count * rtf > obj_length and warmup:
                    warmup = False
                    if verbose: print('END OF WARMUP')


                if warmup:

                    maximum_char_objectitive = max(maximum_char_objectitive, current_char_count)
                    current_char_objectitive = maximum_char_objectitive * rtf            
                    final_chunk_list.append(' '.join(current_chunk))

                    current_char_count = 0
                    current_chunk = []
                
                else:
                    current_char_objectitive = obj_length     
                    final_chunk_list.append(' '.join(current_chunk))

                    current_char_count = 0
                    current_chunk = []

    
    return "\n".join(final_chunk_list)



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
            if len(current) + 1 + len(word) <= max_len:
                current += " " + word
            else:
                sub_segments.append(current)
                current = word
    # Append whatever remains
    if current:
        sub_segments.append(current)
    return sub_segments

def split_text_old(text, min_length=10, max_length=500, split_pattern=r'\.|\n'):
    """
    Split text by a specified pattern (default='.') ensuring each piece is:
      - At least min_length characters (merge small ones with neighbors),
      - At most max_length characters (split large ones by spaces),
      - Returns a list of final sub-texts.
    """

    rtf = 1.2
    smaller_input = 10


    # 1. Split by the pattern Trim whitespace and discard empty segments from the ends
    raw_segments = re.split(split_pattern, text)
    segments = [seg.strip() for seg in raw_segments if seg.strip()]

    # 2. Split further if a segment is longer than max_length
    expanded_segments = []
    for seg in segments:
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
            if i + 1 < len(expanded_segments):
                merged = current_seg + " " + expanded_segments[i + 1]
                final_segments.append(merged.strip())
                i += 2 
            else:
                final_segments.append(current_seg)
                i += 1
        else:
            final_segments.append(current_seg)
            i += 1

    return "\n".join(final_segments)
