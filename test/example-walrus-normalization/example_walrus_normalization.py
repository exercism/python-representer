# Examples of walrus usage in user solutions

def slices(series, length):
    """
    Given a string of digits, output all the contiguous substrings of length `n`,
    in that string, in the order that they appear.
    """
    return [
        sub_str for i, _ in enumerate(series) 
        if len(sub_str := series[i:i+length]) == length   
        ]


def check_height(grid):
    """check that row count is a multiple of 4"""
    if (height := len(grid)) % 3:
        raise ValueError("grid rows not a multiple of 4")
    return height


def nswe_points(self, point):
    """return a set of four adjacent points"""
    nswe_offsets = set([(1, 0), (-1, 0), (0, -1), (0, 1)])
    return {
        neighbor
        for offset in nswe_offsets
        if self.on_the_board(neighbor := point + offset)
    }

