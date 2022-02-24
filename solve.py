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
    def __init__(self, days, score, best, roles):
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


if __name__ == "__main__":
    input_folder = pathlib.Path("input_data")
    for input_file in input_folder.iterdir():
        print(f"Reading file {input_file}")

        read_data(input_file)
