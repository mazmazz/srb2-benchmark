# SRB2 Benchmark

## Arguments

```
srb2benchmark.exe [-h] [-cwd CWD] [-exe EXE [EXE ...]]
                  [-id ID [ID ...]]
                  [-nosoftware NOSOFTWARE [NOSOFTWARE ...]]
                  [-opengl OPENGL [OPENGL ...]]
                  [-vidmode VIDMODE [VIDMODE ...]]
                  [-demo DEMO [DEMO ...]] [-trials TRIALS] [-unique]
```

## Dependencies

* `pip install git+https://github.com/mazmazz/Gooey.git@mazmazz-demo`

## To Build

Use pyinstaller to build a one-file EXE. You must have Python 3.0 - 3.5 to use pyinstaller.
Install the above dependency first. The EXE will be generated in `[srb2benchmark-root]/dist`.

According to `build.spec`, the console window is disabled by default, which prevents command line
arguments from being used. Set `console=True` in `build.spec` to change this behavior.

* `pip install pyinstaller`
* `cd [srb2benchmark-root]`
* `pyinstaller build.spec`
