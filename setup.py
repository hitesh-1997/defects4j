import os
import pandas as pd
import multiprocessing as mp
from tqdm import tqdm

# ======================

def setup_project(project_data):
    project, bug = project_data['project'], project_data['bug']
    command = f"defects4j checkout -p {project} -v {bug}f -w /tmp/repos/repo_{project}_fixed_{bug}"
    exit_code = os.system(command)
    if exit_code!= 0:
        print(f"Failed to checkout {project} {bug}")

def main():
    PROJECT_LIST = ['Lang', 'Chart']
    os.makedirs('/tmp/repos', exist_ok=True)

    project_bug_list = []
    for project in PROJECT_LIST:
        bug_data_path = os.path.join('./framework/projects', project, 'active-bugs.csv')
        bug_list = list(pd.read_csv(bug_data_path)['bug.id'])[:10]
        for bug in bug_list:
            project_bug_list.append({
                'project': project,
                'bug': bug
            })
    
    pool = mp.Pool(mp.cpu_count() - 1)
    with tqdm(total=len(PROJECT_LIST)) as pbar:
        for _ in pool.imap_unordered(setup_project, project_bug_list):
            pbar.update()

if __name__ == "__main__":
    main()
