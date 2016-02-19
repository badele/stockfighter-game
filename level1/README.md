# Level 1

## Usage

    Usage:
      level1 [-q=<qorder> | --qty=<qorder>] [-n=<nb> | --nb-loop=<nb>]
      level1 -h | --help

    Arguments:

    Options:
      -n=<nb> --nb-loop=<nb>        Loop number [default: 10]
      -q=<qorder> --qty=<qorder>    Stock quantity must be order [default: 100]
      -h --help                     Help usage

## Run

    cd level1
    run.py

    # Result
    Init game
    Init stockfighter
    ..........
    Stocks
       venue symbol                       quoteTime   bid   ask  bidSize  askSize  bidDepth  askDepth
    0  MBSEX   XYYP  2016-02-19T07:22:24.915274788Z  9469  9563     1250      595      3750      2065
    2  MBSEX   XYYP  2016-02-19T07:22:29.485855873Z   NaN  9920        0      613         0       613
    3  MBSEX   XYYP  2016-02-19T07:22:29.489230993Z   NaN  9824        0      613         0      1839
    5  MBSEX   XYYP  2016-02-19T07:22:34.491927369Z   NaN  9694        0       95         0      1937
    8  MBSEX   XYYP  2016-02-19T07:22:39.506255574Z  9466   NaN      147        0      4380         0
    Buy 100 stocks at 9466

