# getpycomic

Searches and obtains the manga/comic images and generates a *CBZ* file. Allows to group the chapters by volumes.

By default, it compiles 6 chapters per volume or if you want to know the volumes and chapters, see [https://comick.io](https://comick.io).

Supported pages:
  * [tmomanga](https://tmomanga.com/)
  * [zonatmo](https://zonatmo.com/)
  * [novelcool](https://novelcool.com/)

To request new pages, make a new `issue` with `enhancement` tag.

> [!NOTE]
> This project aims to give you the possibility to take this entertainment wherever you go, even without an Internet connection.


# Installation

```bash
$ pip install getpycomic
```


# Usage

```bash
$ getpycomic --help
usage: getpycomic [-h] -n NAME_OR_PATH [NAME_OR_PATH ...] [-w {tmomanga,zonatmo,novelcool}] [-c CHAPTER] [-v VOLUMES [VOLUMES ...]] [--no-cbz]
                  [-e {selenium}] [-l {en,es,br,it,ru,de,fr}] [--preserve] [--no-download] [-s] [--verbose] [-i] [--debug] [--no-preserve]
                  [--size {original,small,medium,large}]

Gets manga/comic from web to CBZ files.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME_OR_PATH [NAME_OR_PATH ...], --name_or_path NAME_OR_PATH [NAME_OR_PATH ...]
                        Name of the manga/comic or path of the manga/comic downloaded
  -w {tmomanga,zonatmo,novelcool}, --web {tmomanga,zonatmo,novelcool}
                        Select website.
  -c CHAPTER, --chapter CHAPTER
                        Chapters: `all`, `1,5`, `5+` `1-5`. Default `all`.
  -v VOLUMES [VOLUMES ...], --volumes VOLUMES [VOLUMES ...]
                        Indicate how the chapters will be put together by volume in the CBZ file. By default, each volume has `6` chapters. For example:
                        1:[1,4],2:[5,9]
  --no-cbz              It only downloads chapters and does not create CBZ files.
  -e {selenium}, --engine {selenium}
                        Select engine to get data.
  -l {en,es,br,it,ru,de,fr}, --language {en,es,br,it,ru,de,fr}
                        Select language. Default is `es`.
  --preserve            All images files is deleted or not after create CBZ files.
  --no-download         It does not configure the motor and does not prepare it.
  -s, --show            Show engine or not. Default is no.
  --verbose             Displays messages of all operations.
  -i, --interactive     Interactive Prompt for manga/comics search. By default the first item found is used.
  --debug               Show more messages for debug.
  --no-preserve         Preserve manga/comic images. Default is true.
  --size {original,small,medium,large}
                        Select the size of the image.Default is `original`.

You can read your manga/comics wherever you want.
```

Image `--size`:
  * `original`: preserves original sizes.
  * `small`: 800x1200.
  * `medium`: 1000x1500.
  * `large`: 1200x1800.


# Examples

* gets all chapters and create volumes with 6 chapter.

```bash
$ getpycomic --name_or_path MANGA_NAME --web zonatmo
```

* gets all available chapters of "MANGA_NAME" from "zonatmo", all images are stored with `small` size and builds CBZ files with specific chapters.

```bash
$ getpycomic --name_or_path MANGA_NAME --web zonatmo --chapter all --size small --volumes 1: [1, 15],2: [16, 30],3: [31, 45],4: [46, 60],5: [61, 74]
```
