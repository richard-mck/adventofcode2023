"""
To start, each part is rated in each of four categories:

    x: Extremely cool looking
    m: Musical (it makes a noise when you hit it)
    a: Aerodynamic
    s: Shiny

Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has
a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is
true. The first rule that matches the part being considered is applied immediately, and the part moves on to the
destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex
were considering a specific part, it would perform the following steps in order:

    Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
    Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
    Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
    Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).

If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns.
If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a
few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}

The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to
sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following
workflows:

    {x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
    {x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
    {x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
    {x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
    {x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A

Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for
the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for
all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all
of the parts that ultimately get accepted?

To begin, get your puzzle input
"""


import operator

from common_functions import load_input, parse_data_on_empty_rows

ops = {"<": operator.lt, ">": operator.gt}


class Part(object):
    def __init__(self, raw_part: str):
        elements = raw_part.split(",")
        # Items within the part are always ordered x,m,a,s and have the form x=$INT
        self.x = int(elements[0].split("=")[1])
        self.m = int(elements[1].split("=")[1])
        self.a = int(elements[2].split("=")[1])
        # The S type always has a closing bracket
        self.s = int(elements[3].split("=")[1].replace("}", ""))
        self.sum = self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"Part(x:{self.x}, m:{self.m}, a:{self.a},s:{self.s})"


def evaluate_string_operation(instruction: str, part: Part) -> str or None:
    # Example operation a>3333:R
    part_value = getattr(part, instruction[0])
    action = instruction[1]
    next_step = instruction.split(":")
    required_value = int(next_step[0][2:])
    next_step = next_step[1]
    print(f"{instruction} -> {part_value} {action} {required_value} : {next_step}")
    if ops[action](part_value, required_value):
        return next_step
    return None


def convert_instructions(raw_instr: list[str]) -> dict[str, list[str]]:
    """Given a list of raw instructions, convert these to named steps and return a dict with names as keys"""
    result = {}
    # Example instruction rfg{s<537:gd,x>2440:R,A}
    for item in raw_instr:
        name_and_steps = item.split("{")
        name = name_and_steps[0]
        steps = name_and_steps[1][:-1]
        steps = steps.split(",")
        result[name] = steps
    return result


def evaluate_part(steps: dict[str, list[str]], part: Part) -> str or None:
    next_step = steps["in"]
    accept_reject = ["A", "R"]
    while next_step is not None:
        for item in next_step:
            # We have reached the "GOTO" portion of the instructions
            if item == next_step[-1] and item not in accept_reject:
                next_step = steps[item]
                continue
            elif item in accept_reject:
                return item
            # We're still iterating so we need to actually evalute the instructions
            result = evaluate_string_operation(item, part)
            if result in accept_reject:
                return result
            elif result is None:
                continue
            else:
                next_step = steps[result]
                break
    return None


if __name__ == "__main__":
    data = load_input("example.txt")
    print(data)
    parsed = parse_data_on_empty_rows(data)
    print(parsed)
    parts = [Part(i) for i in parsed[1]]
    print(parts)
    evaluate_string_operation("a>3333:R", parts[0])
    instructions = convert_instructions(parsed[0])
    print(instructions)

    accepted = []
    rejected = []
    for part in parts:
        workflow = evaluate_part(instructions, part)
        match workflow:
            case "A":
                accepted.append(part)
            case "R":
                rejected.append(part)
            case other:
                print(f"Error processing part {part}")
    print("Accepted: ", end="")
    print(accepted)
    print(f"Sum of accepted parts: {sum([i.sum for i in accepted])}")
    print("Rejected: ", end="")
    print(rejected)
