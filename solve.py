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
        self.workers = []
        for worker, skill in workers:
            worker.working = True
            worker.skill_working_on = skill
            self.workers.append(worker)

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
        for p in range(P):
            line = in_file.readline().strip().split(" ")
            name = line[0]
            D, S, B, R = map(int, line[1:])
            skills = []
            s = set()
            for _ in range(R):
                skill_name, level = in_file.readline().strip().split(" ")
                #assert skill_name not in s, f'{name}{p}{s}{skill_name}'
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
        #print(project.name)
        if project.time_worked > 0 or project.best < day_counter:
            #print('floop')
            continue
        # do we have bois for problem
        work_pair = [[worker, True] for worker in workers]
        picked_list = []
        for skill, level in project.skills:
            #print('a', skill, level)
            picked = False
            picked_i = 0
            for i, (worker, available) in enumerate(work_pair):
                #print('b',worker.skills, available)
                if not available or worker in people_set:
                    continue
                if skill in worker.skills:
                    if worker.skills[skill] >= level:
                        picked = True
                        picked_i = i
                        break
            if picked:
                work_pair[picked_i][1] = False
                picked_list.append((worker, skill+'@'+str(level)))
            #print(picked_list)
        #print(project.name, len(project.skills))
        if len(picked_list) == len(project.skills):
            people_set.update([worker for worker, _ in picked_list])
            people.append(picked_list)
            output_projects.append(project)
        else:
            pass
            #print('wtf')

    return output_projects, people


def update(projects):
    p = []
    done=[]
    for proj in projects:
        if proj.is_done():
            done.append(proj)
            for worker in proj.workers:
                # update their skills
                if (
                    int(worker.skill_working_on.split('@')[1])
                    == worker.skills[worker.skill_working_on.split('@')[0]]
                ):
                    worker.skills[worker.skill_working_on.split('@')[0]] += 1
                worker.working = False
        else:
            proj.time_worked += 1
            p.append(proj)
    return p, done


def solve(contrib, proj):
    day_counter = 0
    sorted_proj = sorted(proj, key=lambda x: x.rating, reverse=True)
    projects_being_worked_on = []
    output=[]
    while True:
        #print("boop")
        projects, people = get_next_possible_projects(contrib, sorted_proj, day_counter)
        #print(f" printing projects {projects}")
        #print(f" printing people {people}")
        if projects == [] and projects_being_worked_on == []:
            break
        for project, workers in zip(projects, people):
            project.assign_workers(workers)
            projects_being_worked_on.append(project)

        #print(projects_being_worked_on)
        projects_being_worked_on, projects_done = update(projects_being_worked_on)
        for project in projects_done:
            output.append([project.name]+project.workers)
        day_counter += 1
    return output

def write_file(filename, answer):
    with open(f'output_data/{filename}', 'w') as out_file:
        out_file.write(str(len(answer))+'\n')
        for n in answer:
            out_file.write(n[0]+'\n')
            out_file.write(' '.join([a.name for a in n[1:]])+'\n')



if __name__ == "__main__":
    input_folder = pathlib.Path("input_data")
    for input_file in input_folder.iterdir():
        print(f"Reading file {input_file}")

        contributors, projects = read_data(input_file)

        answer = solve(contributors, projects)
        #print(answer)
        #assert False, "sweet jesus we did it"
        write_file(input_file.name.split('.')[0] + ".out", answer)
