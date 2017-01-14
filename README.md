# SHA1-Record-Search
##About:
Searches for SHA1's that break records shown here: https://hashkiller.co.uk/hash-min-max.aspx

A newly found record can be submitted via the form on https://hashkiller.co.uk/hash-min-max.aspx

##Running:
Modify chars on line 8 for charcters to cycle through.
Modify "rand_length" on line 37 to suite search keyspace(default 8).
Modify "clear" on line 43, insert desired string between quoatation marks to be included as input message.
Alternatively swap (clear = combo+"") to (clear = ""+combo) if you want input string to be prefixed.
