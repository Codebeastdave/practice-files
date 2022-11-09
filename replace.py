#print(''.join(["{0:0>8}".format(x.replace('b', '').replace('0', '000').replace('1', '111')) for x in  [str(bin(x)) for x in [ord(x) for x in input()]]]))
#print([int(bool(all([int(x) for x in [x for x in input().split(",")])))])

#print([list(x) for x in [x for x in input()]])

xtt =  "eoeeeoeeroe"
xetm= "e"
men = "4"
def replace(x, xe, me):
    try:
        trx , tron = 0,0
        xet = ''
        while trx < len(x):
            print(76)
            if x[trx] == xe[tron]:
                if len(xe)> 1:
                    print(81)
                    while tron < len(xe) - 1:
                        print(67)
                        if x[trx + 1] == xe[tron + 1]:
                            print(899)
                            xet = x[:trx] + me + x[trx + len(xe):]
                        tron += 1
                else:
                    print(34)
                    xet = x[:trx] + me + x[trx + len(xe):]
            trx += 1
        if xe in xet:
            print(1)
            return replace(xet, xe, me)
        return xet
    except RecursionError as err:
        print("Error: the target string is too long, you can slice the strings and run this function on those new strings, then join these strings together")


print(replace(xtt, xetm, men))