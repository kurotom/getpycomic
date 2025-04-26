# -*- coding: utf-8 -*-
"""
"""

from src.controller import GetPyComic


webs = ["tmomanga", "zonatmo"]
# t = GetPyComic(web=webs[1])
t = GetPyComic(web=webs[1], show=False)
# t = GetPyComic(show=False)
# # t = GetPyComic(setup=False)
#
manga = "seto no hanayome"
manga = "link click"
# manga = "Kanojo"
# manga = "golden boy"
# manga = "girls bravo"
# manga = "usagi drop"
# manga = "ese chico..."
# manga = "look back"
# manga = "The Gods Lie"
# manga = "Hwaja"
# manga = "kono"
# manga = "kansei pianist"

print("> ", manga)

r = t.search(search=manga)

print('-> SEARCH ', r)
#
c = t.get_chapters(comic=r[0])
print("chapters ", c, type(c), r[0])
print(id(t.get_current_comic) == id(c) == id(r[0]))
print(id(t.get_current_comic), id(c), id(r[0]))
print(r[0].chapters[0].link, r[0].chapters[0])
#
t.close_scraper()

# t.save_comic()
#
#
#
# t.to_pickle()
# t.to_json()
#
#
# t.to_load()
# print(t.get_current_comic)
#
# # chapters = {
# #     1: [1, 6],
# #     2: [7, 12],
# #     3: [13, 18],
# #     4: [19, 24.1],
# #     5: [25, 30],
# #     6: [31, 36],
# #     7: [37, 42],
# #     8: [43, 49],
# #     9: [50, 56],
# #     10: [56.01, 62]
# # }
#
# chapters = {
#     1: [1, 37]
# }
#
# x = t.sorter_chapters_by_volumes(chapters_by_volume=chapters)
#
# print('---> ', x)
#
# for k, v in x.volumes.items():
#     print('> ', k, v.list_chapters)
#     # print('> ', k, v, v[0].images)
#
# t.to_cbz()
