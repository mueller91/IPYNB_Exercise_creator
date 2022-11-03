#!/usr/bin/python3
# Nicolas Müller, <nicolas.mueller@aisec.fraunhofer.de>
import copy
import json
import sys

TOKEN_EXERCISE = '#!!exercise'
TOKEN_SOLUTION = '#!!solution'

if __name__ == "__main__":
    # assert input is ok
    assert len(sys.argv) == 2, f"Usage: .make_notebook.py exmaple.ipynb"
    nb_file = sys.argv[1]
    assert str(nb_file).endswith('.ipynb'), f"{nb_file} is no ipynb!"

    # load
    with open(nb_file, 'r+') as f:
        file = json.load(f)

    # setup targets
    file_exercise = copy.deepcopy(file)
    file_solution = copy.deepcopy(file)
    file_exercise['cells'] = []
    file_solution['cells'] = []

    cnt_solution = 0
    cnt_exercise = 0
    cnt_all = 0
    cnt_empty = 0

    # start parsing
    for x in file['cells']:
        source = x['source']
        cnt_all += 1
        # cell not empty
        if len(source) > 0:
            first_line = source[0]
            first_line_without_token = first_line.replace(TOKEN_SOLUTION, '').replace(TOKEN_EXERCISE, '').strip()
            x['source'][0] = first_line_without_token
            if first_line.startswith(TOKEN_EXERCISE):
                file_exercise['cells'] += [x]
                cnt_exercise += 1
            elif first_line.startswith(TOKEN_SOLUTION):
                file_solution['cells'] += [x]
                cnt_solution += 1
            else:
                file_exercise['cells'] += [x]
                file_solution['cells'] += [x]
                cnt_exercise += 1
                cnt_solution += 1
        # cell empty
        else:
            cnt_empty += 1
            file_exercise['cells'] += []
            file_solution['cells'] += []

    #log
    ex_file = nb_file.replace('.ipynb', '_exercise.ipynb')
    sol_file = nb_file.replace('.ipynb', '_solution.ipynb')
    print(f"[SUCCESS].\n\nProcessed {nb_file}.\n"
          f"Found {cnt_all} cells, of which \n- {cnt_exercise} are used in the exercise, and \n- {cnt_solution} in the solution.\n"
          f"- {cnt_empty} cells are empty.\n"
          f"Written to \n- {ex_file}, and \n- {sol_file}.")

    # done, write to disk
    with open(ex_file, 'w') as g:
        json.dump(file_exercise, g)
    with open(sol_file, 'w') as h:
        json.dump(file_solution, h)
