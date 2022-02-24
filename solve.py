import pathlib


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.working = False
        self.skill_working_on = None


class Project:
    @property
    def rating(self):
        return self.score - self.days

    def is_done(self):
        return self.time_worked == self.days

    def assign_workers(self, workers):
        for worker, skill in workers:
            worker.working = True
            worker.skill_working_on = skill

    def __init__(self, name, days, score, best, roles, skills):
        self.name = name
        self.days = days
        self.score = score
        self.best = best
        self.roles = roles
        self.skills = skills
        self.time_worked = 0
        self.workers = []
        self.sneaky_skills = {a: b for a, b in skills}


def read_data(filename):
    with open(f"{filename}", "r") as in_file:
        C, P = map(int, in_file.readline().strip().split(" "))
        contributors = []
        for _ in range(C):
            contrib_name, N = in_file.readline().strip().split(" ")
            N = int(N)
            skills = {}
            for _ in range(N):
                skill_name, level = in_file.readline().strip().split(" ")
                level = int(level)
                skills[skill_name] = level
            contributors.append(Contributor(contrib_name, skills))
        projects = []
        for _ in range(P):
            line = in_file.readline().strip().split(" ")
            name = line[0]
            D, S, B, R = map(int, line[1:])
            skills = []
            s = set()
            for _ in range(R):
                skill_name, level = in_file.readline().strip().split(" ")
                assert skill_name not in s, "rip"
                s.add(skill_name)
                level = int(level)
                skills.append((skill_name, level))
            projects.append(Project(name, D, S, B, R, skills))
    return contributors, projects


def get_next_possible_projects(workers, projects, day_counter):
    # return list of projects and list of lists of workers
    output_projects = []
    people = []
    people_set = set()

    for project in projects:
        if project.time_worked > 0 or project.best > day_counter:
            continue
        # do we have bois for problem
        work_pair = [[worker, True] for worker in workers]
        picked_list = []
        for skill, level in project.skills:
            picked = False
            picked_i = 0
            for i, (worker, available) in enumerate(work_pair):
                if not available or worker in people_set:
                    continue
                if skill in worker.skills:
                    if worker.skills[skill] >= level:
                        picked = True
                        picked_i = i
            if picked:
                work_pair[picked_i][1] = False
                picked_list.append((worker, skill))
        if len(picked_list) == len(project.skills):
            people_set.update([worker for worker, _ in picked_list])
            people.append(picked_list)
            output_projects.append(project)

    return projects, people


def update(projects):
    p = []
    for proj in projects:
        if proj.is_done:
            for worker in proj.workers:
                # update their skills
                if (
                    proj.sneaky_skills[worker.skil_working_on]
                    == worker.skills[worker.skill_working_on]
                ):
                    worker.skills[worker.skill_working_on] += 1
                worker.working = False
        else:
            proj.time_worked += 1
            p.append(proj)
    return p


def solve(contrib, proj):
    day_counter = 0
    sorted_proj = sorted(proj, key=lambda x: x.rating, reverse=True)
    projects_being_worked_on = []
    while True:
        print("boop")
        projects, people = get_next_possible_projects(contrib, sorted_proj, day_counter)
        print(f" printing projects {projects}")
        print(f" printing people {people}")
        if projects == [] and projects_being_worked_on == []:
            break
        for project, workers in zip(projects, people):
            project.assign_workers(workers)
            projects_being_worked_on.append(project)

        projects_being_worked_on = update(projects_being_worked_on)
        day_counter += 1


def write_file(filename, answer):
    pass


if __name__ == "__main__":
    input_folder = pathlib.Path("input_data")
    for input_file in input_folder.iterdir():
        print(f"Reading file {input_file}")

        contributors, projects = read_data(input_file)
        print(contributors)
        print(projects)

        answer = solve(contributors, projects)
        print(answer)
        assert False, "sweet jesus we did it"
        write_file(input_file.split(".")[0] + ".out", answer)
