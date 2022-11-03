## ipynb Exercise Creator

When you use ipynb notebooks for lectures and exercises, 
you might want to have a single notebook file from which you can easily compile both the training notebook,
as well as the solution.

This script presents a way to create these:

```
./make_notebook.py example.ipynb
```

This will create example_exercise.ipynb as well as example_solution.ipynb.

### Usage
You can mark a cell (either markdown or code) to be included either in the exercise, solution, or both.
To be included only in the exercise with `!!exercise`, and solution cells with `!!solution`.
Cells without such markers will be included in both output files.