def _imp_replace(haystack, needle,  new_needle, iterations):
    xr,t = 0,0
    """internal implementation of replace function"""
    logic = False
    print("wow")
    while xr < len(haystack):
        if haystack[xr] == needle[t]:
            while t < iterations:
                re = haystack[xr:xr + len(needle)]
                if needle in re:
                    logic = True
                    haystack = haystack[:xr] + new_needle + haystack[len(needle) + xr:]
                t += 1
                xr += 1
            t = 0
        if logic:
            return haystack
        xr += 1

def replace_one(x, y,  mff):
    """replace single occurence of target string in main string"""
    return _imp_replace(x, y, mff,iterations = 1)


def replace_all(x, y,  mff):
    """replace all occurence of target string in main string"""
    return _imp_replace(x, y, mff, iterations = len(x))


def replace(main_string, target_string, repl_string,  n=1):
    """the main function"""
    xr, t = 0, 0
    if n == 0:
        return replace_one(main_string, target_string,  repl_string)
    if n == 1:
        return replace_all(main_string, target_string, repl_string)




print(replace("foobarzedbarz", "barz", "fu", n=1))
