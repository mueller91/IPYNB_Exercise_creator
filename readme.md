## ipynb Exercise Creator

When you make an ipynb, you might want to have a single file which provides both the training notebook, as well
as the solution.
This script presents a way to create these:

```
./make_notebook.py example.ipynb
```

This will create example_exercise.ipynb as well as example_solution.ipynb.

### Usage
Start cell to be included only in the exercise with `!!exercise`, and solution cells with `!!solution`.
Cells without such markers will be included in both output files.