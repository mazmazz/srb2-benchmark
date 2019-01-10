# SRB2 Benchmark

Benchmark SRB2 using a series of EXEs and replay demos!

## Dependencies

* `pip install git+https://github.com/mazmazz/Gooey.git@mazmazz-demo`

## To Build

Use pyinstaller to build a one-file EXE. You must have Python 3.0 - 3.5 to use pyinstaller.
Install the Gooey dependency first, above. The EXE will be generated in `[srb2benchmark-root]/dist`.

* `pip install pyinstaller`
* `cd [srb2benchmark-root]`
* `pyinstaller build.spec`
* `pyinstaller build-cmd.spec`
    * See `build-cmd.spec` for a note on which lines to comment out in `srb2benchmark.py` before building.

## Arguments

Running `srb2benchmark.exe` without arguments will run a default series of tests:

* `32-bit/srb2win-v2123.exe` and `64-bit/srb2win-v2123.exe`
* Software only
* 640x400, 1280x800, and 1920x1200
* MAP01 and MAP02 replays
* One trial (no repeats)
* No savestate file to resume

For the following arguments, each argument must have an equal number of inputs,
representing one test per entry. Think of the arguments as a parallel struct.

* `-exe`
* `-id`
* `-nosoftware`
* `-opengl`
* `-perargs`

```
usage: srb2benchmark_cmd.exe [-h] [-cwd CWD] [-exe EXE [EXE ...]]
                             [-id ID [ID ...]]
                             [-nosoftware NOSOFTWARE [NOSOFTWARE ...]]
                             [-opengl OPENGL [OPENGL ...]]
                             [-perargs PERARGS [PERARGS ...]]
                             [-vidmode VIDMODE [VIDMODE ...]]
                             [-demo DEMO [DEMO ...]] [-trials TRIALS]
                             [-xargs XARGS] [-savestate SAVESTATE]
                             [-idtrialnum] [-idunique]

optional arguments:
  -h, --help            show this help message and exit
  -cwd CWD              Current working directory to start SRB2 from (i.e.,
                        your root SRB2 folder)
  -exe EXE [EXE ...]    Space-separated list of EXE filenames to test.
  -id ID [ID ...]       Space-separated list of IDs to associate with the
                        EXEs. # of IDs must match the # of EXEs.
  -nosoftware NOSOFTWARE [NOSOFTWARE ...]
                        Do not benchmark Software mode. Space-separated true
                        or false per EXE
  -opengl OPENGL [OPENGL ...]
                        Benchmark OpenGL mode. Space-separated true or false
                        per EXE
  -perargs PERARGS [PERARGS ...]
                        Command line arguments to add. Space-separated, quoted
                        strings per EXE.
  -vidmode VIDMODE [VIDMODE ...]
                        Space-separated list of vid_modes to test, for all
                        EXEs. 0 = 1920x1200; 9 = 1280x800; 15 = 640x400
  -demo DEMO [DEMO ...]
                        Space-separated list of demo filenames to benchmark,
                        relative to the CWD.
  -trials TRIALS        Number of trials per test
  -xargs XARGS          Command line arguments to add to every run.
  -savestate SAVESTATE  File to save testing state and resume on subsequent
                        runs.
  -idtrialnum           Add trial number to ID
  -idunique             Make trial IDs unique (add UTC datetime to ID string)
```
