from pathlib import Path

class Images:

    janet_wave = r'https://i.imgur.com/OgqS9fj.gif'
    clap = r'https://gfycat.com/unknowndeadhorseshoecrab'

    cactus_list = [r'https://i.imgur.com/BPcfzNy.gif',
                   r'https://i.imgur.com/bFeXQEU.gif',
                   r'https://i.imgur.com/MzTEjDu.gif',
                   r'https://i.imgur.com/FF8lx1b.gif']


staff_ids = {
    'kinney': 315783211479465984,
    'indy': 82331305387241472,
    'celtic': 292348913568972800,
    'errilhl': 368695809518075918,
    'fasder': 399878320113713152,
    'sdl:': 381320988736094210
}


class Files:

    @staticmethod
    def get_rules():
        with open('texts/rules.txt', 'r') as f:
            return f.readlines()

    @staticmethod
    def get_facts(filename):
        with open(f'facts/{filename.lower()}.txt', 'r') as f:
            facts = f.readlines()

        facts_str = '```'
        for i, fact in enumerate(facts):
            facts_str += f'{i}: {fact} \n'
        facts_str += '```'

        if facts_str == '``````':
            facts_str = '```No facts to display```'

        return facts, facts_str

    @staticmethod
    def write_facts(filename, facts: list):
        with open(f'facts/{filename.lower()}.txt', 'w', encoding='utf-8') as file:
            for fact in facts:
                file.write(fact)

    @staticmethod
    def create_file(filename):
        file_path = Path(f'facts/{filename.lower()}.txt')

        if not file_path.parent.exists():
            file_path.parent.mkdir()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('')

    @staticmethod
    def add_fact(filename, fact: str):
        with open(f'facts/{filename.lower()}.txt', 'a+', encoding='utf-8') as file:
            file.write(fact + '\n')
