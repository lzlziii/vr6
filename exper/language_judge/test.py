s = """
130     33   5   1   5   2   0     10
1830     82  43  16  13   8  10     58
171     85   0   4   0   2   1      6
25      1   0   0   0   1   1      1
198     26   6   0   2   3   3      6
"""

cnt = 0
for i in s.split():
    if i.isnumeric():
        print(i)
        cnt += int(i)

print(cnt)