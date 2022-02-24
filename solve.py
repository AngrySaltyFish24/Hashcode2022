class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level

class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills





def read_data(filename):
    with open(f'input_data/{filename}', 'r') as in_file:
        C, P = map(in_file.readline().strip().split(' '), int)
        contributors = []
        for c in range(C):
            contrib_name, N = in_file.readline().strip().split(' ')
            N = int(N)
            skills = []
            for n in range(N):
                skill_name, level = in_file.readline().strip().split(' ')
                level = int(level)
                skills.append(Skill(skill_name, level))
        contributors.append(Contributor(contrib_name, skills))





if __name__ == "__main__":
