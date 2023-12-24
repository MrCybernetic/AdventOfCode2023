from typing import List


class Workflows:
    def __init__(self, path: str) -> None:
        self.rules = {}
        self.parts = []
        with open(path) as f:
            text = f.read()
            rules_part = text.split('\n\n')[0]
            parts_part = text.split('\n\n')[1]
            for rule in rules_part.split('\n'):
                rule_set = RuleSet(rule)
                self.rules[rule_set.name] = rule_set
            for part in parts_part.split('\n'):
                self.parts.append(Part(part))

    def get_accepted_parts_ratings(self) -> int:
        accepted_part_ratings = 0
        for part in self.parts:
            ruleset = self.rules["in"]
            for rule in self.rules:
                for letter in ["x", "m", "a", "s"]:
                    value_to_compare = getattr(part, letter)
                    operator = getattr(ruleset, letter)["operator"]

        return accepted_part_ratings


class RuleSet:
    def __init__(self, rule: str) -> None:
        self.name: str = rule.split('{')[0]
        rules_raw: List[str] = rule.split('{')[1].split('}')[0].split(',')
        self.rules = []
        for rule in rules_raw:
            if rule[0] == 'x':
                x = {}
                x["letter"] = "x"
                x["operator"] = rule[1]
                x["value_to_compare"] = int(rule.split(':')[0][2:])
                x["result"] = rule.split(':')[1]
                self.rules.append(x)
            elif rule[0] == 'm':
                m = {}
                m["letter"] = "m"
                m["operator"] = rule[1]
                m["value_to_compare"] = int(rule.split(':')[0][2:])
                m["result"] = rule.split(':')[1]
                self.append(m)
            elif rule[0] == 'a':
                a = {}
                a["letter"] = "a"
                a["operator"] = rule[1]
                a["value_to_compare"] = int(rule.split(':')[0][2:])
                a["result"] = rule.split(':')[1]
                self.rules.append(a)
            elif rule[0] == 's':
                s = {}
                s["letter"] = "s"
                s["operator"] = rule[1]
                s["value_to_compare"] = int(rule.split(':')[0][2:])
                s["result"] = rule.split(':')[1]
                self.rules.append(s)
        self.default: str = rules_raw[-1]

    def __repr__(self) -> str:
        return f"Rule({self.name}, {self.rules}, {self.default})"


class Part:
    def __init__(self, part: str) -> None:
        self.x: int = int(part.split('{')[1].split(',')[0].split('=')[1])
        self.m: int = int(part.split('{')[1].split(',')[1].split('=')[1])
        self.a: int = int(part.split('{')[1].split(',')[2].split('=')[1])
        self.s: int = int(part.split('{')[1].split(',')[3].split('=')[1].split('}')[0])

    def get_rating(self) -> int:
        return self.x + self.m + self.a + self.s

    def __repr__(self) -> str:
        return f"Part({self.x}, {self.m}, {self.a}, {self.s})"


def main():
    # Part 1
    workflows = Workflows("J19/test.txt")
    print(workflows.get_accepted_part_ratings())


if __name__ == "__main__":
    main()
