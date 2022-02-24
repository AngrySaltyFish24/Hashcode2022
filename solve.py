from audioop import reverse
from distutils.file_util import write_file
import sys
import pathlib


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills


class Project:
    @property
    def rating(self):
        return self.score - self.days

    def __init__(self, name, days, score, best, roles):
        self.name = name
        self.days = days
        self.score = score
        self.best = best
        self.roles = roles


def read_data(filename):
    with open(f"{filename}", "r") as in_file:
        C, P = map(int, in_file.readline().strip().split(" "))
        contributors = []
        for c in range(C):
            contrib_name, N = in_file.readline().strip().split(" ")
            N = int(N)
            skills = []
            for n in range(N):
                skill_name, level = in_file.readline().strip().split(" ")
                level = int(level)
                skills.append(Skill(skill_name, level))
        contributors.append(Contributor(contrib_name, skills))
        projects = []
        for p in range(P):
            line = in_file.readline().strip().split(" ")
            name = line[0]
            D, S, B, R = map(int, line[1:])
            projects.append(Project(name, D, S, B, R))
    return contributors, projects

def solve(contrib, proj):
    sorted_proj = sorted(proj, key=lambda x: x.rating, reverse=True)

def write_file(filename, answer):
    pass

if __name__ == "__main__":
    input_folder = pathlib.Path("input_data")
    for input_file in input_folder.iterdir():
        print(f"Reading file {input_file}")

        contributors, projects = read_data(input_file)

        answer = solve(contributors, projects)

        write_file(input_file.split('.')[0]+'.out', answer)
