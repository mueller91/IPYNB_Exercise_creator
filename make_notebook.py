#!/usr/bin/python3
# Nicolas Müller, <nicolas.mueller@aisec.fraunhofer.de>

import argparse
import copy
import json
import os.path
from pathlib import Path


def _clean(x, tokens):
    """clean a first line"""
    for t in tokens:
        x = x.replace(str(t) + "\n", '')
        x = x.replace(t, "")
    return x


if __name__ == "__main__":
    """Run the parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help="The input .ipynb file.")
    parser.add_argument('-e', '--out_exercise', help="Optional, where to write output exercise to.")
    parser.add_argument('-s', '--out_solution', help="Optional, where to write output solution to.")
    parser.add_argument('--token_exercise', default='#!!exercise', help="Optional, use another token to mark exercise cells in the ipynb file.")
    parser.add_argument('--token_solution', default='#!!solution', help="Optional, use another token to mark solution cells in the ipynb file.")
    args = parser.parse_args()

    # assert input is ok
    nb_file = args.filename
    assert os.path.exists(nb_file)
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
            first_line_without_token = _clean(first_line, tokens=[args.token_exercise, args.token_solution])
            x['source'][0] = first_line_without_token
            if first_line.startswith(args.token_exercise):
                file_exercise['cells'] += [x]
                cnt_exercise += 1
            elif first_line.startswith(args.token_solution):
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

    # get outfile paths
    if args.out_exercise is None:
        ex_file = nb_file.replace('.ipynb', '_exercise.ipynb')
    else:
        ex_file = args.out_exercise
        assert str(ex_file).endswith('.ipynb'), f"{ex_file} must end with .ipynb, please specify valid filename!"
        assert Path(ex_file).parent.exists(), f"Folder for {ex_file} does not exist. Please specify a path that exists!"

    # get outfile paths
    if args.out_solution is None:
        sol_file = nb_file.replace('.ipynb', '_solution.ipynb')
    else:
        sol_file = args.out_solution
        assert str(ex_file).endswith('.ipynb'), f"{ex_file} must end with .ipynb, please specify valid filename!"
        assert Path(ex_file).parent.exists(), f"Folder for {ex_file} does not exist. Please specify a path that exists!"

    # write to disk
    with open(ex_file, 'w') as g:
        json.dump(file_exercise, g)
    with open(sol_file, 'w') as h:
        json.dump(file_solution, h)

    # log
    print(f"[SUCCESS].\n\nProcessed {nb_file}.\n"
          f"Found {cnt_all} cells, of which \n- {cnt_exercise} are used in the exercise, and \n- {cnt_solution} in the solution.\n"
          f"- {cnt_empty} cells are empty.\n"
          f"Written to \n- Exercise: {ex_file}, and \n- Solution: {sol_file}.")

