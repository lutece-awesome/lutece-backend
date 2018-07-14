# Set the paginator number
PER_PAGINATOR_COUNT = 10

# Set the number of problem/status one page should be shown
PER_PAGE_COUNT = 15

# User per page count
USER_PER_PAGE_COUNT = 10

# Set the source code max-length
MAX_SOURCECORE_LENGTH = 65535

# basic checker from testlib.h
CHECKER_LIST = {
    'wcmp': 'compare sequences of tokens',
    'acmp': 'compare two doubles, maximal absolute error = 1.5E-6',
    'caseicmp': 'Single int64 checker with testcase-support',
    'casencmp': 'Many int64s checker with testcase-support',
    'casewcmp': 'Tokens checker with testcase-support',
    'dcmp': 'compare two doubles, maximal absolute or relative error = 1E-6',
    'fcmp': 'compare files as sequence of lines',
    'hcmp': 'compare two signed huge integers',
    'icmp': 'compare two signed int',
    'lcmp': 'compare files as sequence of tokens in lines' ,
    'ncmp': 'compare ordered sequences of signed int numbers' ,
    'rcmp': 'compare two doubles, maximal absolute error = 1.5E-6' ,
    'rcmp4': 'compare two sequences of doubles, max absolute or relative error = 1E-4' ,
    'rcmp6': 'compare two sequences of doubles, max absolute or relative  error = 1E-6' ,
    'rcmp9': 'compare two sequences of doubles, max absolute or relative error = 1E-9' ,
    'rncmp': 'compare two sequences of doubles, maximal absolute error = 1.5E-5' ,
    'uncmp': 'compare unordered sequences of signed int numbers',
}

# The RECENT info number
RECENT_NUMBER = 4