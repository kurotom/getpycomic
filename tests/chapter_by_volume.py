# -*- coding: utf-8 -*-
"""
"""

# chapters
chapters = [
    "1",
    "2",
    "2.1",
    "2.5",
    "3",
    "4",
    "5",
    "6",
    "6.1",
    "6.5",
    "7",
    "8",
    "9"
]



t = ChapterClassifierByVolume()


r = t.sorter(
    chapters=chapters,
    chapters_by_volume={
        1: "1-2",
        2: "3-4",
        3: "5-6",
        4: ""
    }
)
print(r)

r = t.sorter(
    chapters=chapters,
    chapters_by_volume={
        1: "1-2",
        2: "2-3",
        3: "3-4"
    }
)
print(r)

r = t.sorter(
    chapters=chapters,
    chapters_by_volume={
        1: [1,2],
        2: [3,4],
        3: [5,6],
        4: []
    }
)
print(r)

r = t.sorter(
    chapters=chapters,
    chapters_by_volume={
        1: [1,2],
        2: [3,4],
        3: [5,6]
    }
)

print(r)

# Not sequentially
r = t.sorter(
    chapters=chapters,
    chapters_by_volume={
        1: "1-2",
        3: "3-4"
    }
)
print(r)


# Empty
r = t.sorter(
    chapters=chapters
)
print(r)


# Empty
r = t.sorter()
print(r)
