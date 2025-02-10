import subprocess


def bisect(repo_path, start, end, command):
    inp = f"git rev-list --ancestry-path {start}..{end}"
    commits = subprocess.check_output(inp, cwd=repo_path).decode().strip().split("\n")

    l = 0
    r = len(commits) - 1

    while l < r:
        mid = (l + r + 1) // 2
        commit_check = commits[mid]

        print(f"commit {commit_check}:")

        subprocess.run(f"git checkout --quiet {commit_check}")

        if subprocess.run(command, cwd=repo_path).returncode != 0:
            print(f"---Bad commit---\n")
            l = mid
        else:
            print(f"---Good commit---\n")
            r = mid - 1

    return commits[l]


print(bisect(".", "7b769469377d42241caa6824725aa78352f6e906", "3db4b31bbf87540be5893842a7ad9812425c5a1d", "python main.py"))
print("You're not a sigma legend :(")

"""
commit 39e66bfeb30e5236b4ed65295c03468189033240:
Still a beta...
---Good commit---

commit 38a0bcaab7c9151b168772474b1eae5a329e8c93:
You're so sigma
---Bad commit---

commit e5cb20712011ff21171b6b27eadc60384e7f8426:
Still a beta...
---Good commit---

38a0bcaab7c9151b168772474b1eae5a329e8c93
You're not a sigma legend :(

Process finished with exit code 0
"""