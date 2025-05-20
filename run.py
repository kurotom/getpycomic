# -*- coding: utf-8 -*-
"""
"""

from src.controller import GetPyComic


def algo(i, manga):
    t = GetPyComic(web=webs[i], show=False)

    r = t.search(search=manga)

    c = t.get_chapters(comic=r[0])

    t.close_scraper()

    t.save_comic()


    t.to_json()


    t.to_load()

    chapters = {
        1: [1, 37]
    }

    x = t.sorter_chapters_by_volumes(chapters_by_volume=chapters)

    t.to_cbz()


webs = ["tmomanga", "zonatmo", "novelcool"]

# for i in range(len(webs)):
#     manga = "kami no ibutsu" # one shot
#     algo(i, manga)
#     print()


# # t = GetPyComic(web=webs[1])
t = GetPyComic(web=webs[1], show=False)
# # t = GetPyComic(show=False)
# # t = GetPyComic(setup=False)
#
manga = "seto no hanayome"
manga = "link click"
# manga = "The Reason Why Raeliana Ended Up At The Duke\'s Mansion"
# manga = "Kanojo"
# manga = "golden boy"
# manga = "girls bravo"
# manga = "usagi drop"
# manga = "ese chico..."
# manga = "look back"
# manga = "The Gods Lie"
# manga = "Hwaja"
# manga = "kono sub"
# manga = "kansei pianist"
# manga = "kami no ibutsu" # one shot
# manga = "--"

manga = "good ending"

print("> ", manga)

r = t.search(search=manga)
print('-> SEARCH ', r)
# #
c = t.get_chapters(comic=r[0])
# # print("chapters ", c, type(c), r[0])
# # print(id(t.get_current_comic) == id(c) == id(r[0]))
# # print(id(t.get_current_comic), id(c), id(r[0]))
# # print(r[0].chapters[0].link, r[0].chapters[0])
# #
t.close_scraper()

t.save_comic()


t.to_json()


t.to_load()
print("> loaded", t.get_current_comic)

# chapters = {
#     1: [1, 6],
#     2: [7, 12],
#     3: [13, 18],
#     4: [19, 24.1],
#     5: [25, 30],
#     6: [31, 36],
#     7: [37, 42],
#     8: [43, 49],
#     9: [50, 56],
#     10: [56.01, 62]
# }
#
# chapters = {
#     1: [1, 37]
# }
# chapters = None
# chapters = {
#     1: [2, 1],
#     2: [3, 4]
# }

# chapters = {
#     1: (1, 19),
#     2: (20, 38.5),
#     3: (39, 57.5),
#     4: (58, 76.5),
#     5: (77, 95),
#     6: (95.5, 114),
#     7: (114.5, 133),
#     8: (134, 152.5),
#     9: (153, 171),
#     10: (172, 190),
#     11: (191, 209),
#     12: (209.5, 229),
#     13: (230, 247),
#     14: (247.5, 266),
#     15: (267, 285),
#     16: (286, 304),
#     17: (305, 323),
#     18: (324, 342),
#     19: (343, 361.5),
#     20: (362, 380),
#     21: (381, 399),
#     22: (400, 418)
# }

chapters = {
    1: (1, 8),
    2: (9, 16),
    3: (17, 26),
    4: (27, 36),
    5: (37, 46),
    6: (47, 56),
    7: (57, 66),
    8: (67, 76),
    9: (77, 86),
    10: (87, 96),
    11: (97, 106),
    12: (107, 116),
    13: (117, 126),
    14: (127, 136),
    15: (137, 146),
    16: (147, 156)
}


x = t.sorter_chapters_by_volumes(chapters_by_volume=chapters)
print('---> ', x, x.volumes)

# for k, v in x.volumes.items():
#     print('> ', k, v.list_chapters)
#     # print('> ', k, v, v[0].images)

t.to_cbz()

t.close_scraper()
