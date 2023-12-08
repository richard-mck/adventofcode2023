"""
After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you
have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this
example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left
element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of
instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6
steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

from collections import namedtuple
from re import findall
from math import lcm

from common_functions import load_input

Node = namedtuple("Node", "name left right")


def parse_nodes(data: list[str]) -> dict:
    result = {}
    for row in data:
        nodes = findall("\w+", row)
        result[nodes[0]] = Node(nodes[0], nodes[1], nodes[2])
    return result


def reached_goal(nodes: list[Node]) -> bool:
    true_tally = [True for node in nodes if node.name.endswith("Z")]
    return len(true_tally) == len(nodes)


def get_next_node(node: Node, direction: str) -> str:
    if direction == "L":
        return node.left
    if direction == "R":
        return node.right


if __name__ == "__main__":
    sample = load_input("example_a.txt")
    instructions = sample[0].rstrip()
    print(instructions)
    nodes = parse_nodes(sample[2:])
    goal = nodes["AAA"]
    tally = 0
    while goal.name != "ZZZ":
        for instruction in instructions:
            tally += 1
            next_node = get_next_node(nodes[goal.name], instruction)
            goal = nodes[next_node]
    print(tally)
    # part 2!
    print("Part 2!")
    tally = 0
    sample = load_input("example_2.txt")
    instructions = sample[0].rstrip()
    print(f"Instructions {instructions}")
    nodes = parse_nodes(sample[2:])
    check_nodes = [nodes[node] for node in nodes if nodes[node].name.endswith("A")]
    print(f"Starting nodes: {check_nodes}")
    z_factors = []
    for node in check_nodes:
        tally = 0
        while not reached_goal([node]):
            for instruction in instructions:
                next_round = get_next_node(node, instruction)
                node = nodes[next_round]
                tally += 1
        z_factors.append(tally)
    print(z_factors)
    print(lcm(*z_factors))
    pass
