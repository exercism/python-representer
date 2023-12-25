
from itertools import chain, zip_longest, repeat


def recite(start, take=1):
    """Assemble verse list with separators via zip_longest."""

    end_at = start - take
    separate_by = (start-end_at) - 1

    verses = chain(make_verse(number) for number in range(start, end_at, -1))
    separators = repeat([''], separate_by)

    song = chain.from_iterable(item for item in 
                               chain(*zip_longest(verses, separators)) 
                               if item)
    return  list(song)


def make_verse(number):
    '''Yield verses according to number given.'''
    
    num_words = {0:"no", 1:'One', 2:"Two", 3:'Three', 4:"Four",5:'Five',
                 6:"Six",7:'Seven',8:"Eight",9:'Nine',10:"Ten"}

    number_verse = (f'{num_words[number]} green bottle'
                    f'{"s" if number > 1 else ""} hanging on the wall,')
    
    middle_verse = "And if one green bottle should accidentally fall,"
    
    ending_verse = (f"There'll be {num_words[number-1].lower()} green bottle"
                    f"{'s' if number-1 != 1 else ''} hanging on the wall.")

    return     [number_verse, number_verse, middle_verse, ending_verse]