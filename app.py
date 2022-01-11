import math
import re
import collections


class BotBalancer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.read_instuctions()
        self.bins = None

    def read_instuctions(self):
        with open(self.input_file) as f:
            self.instructions = f.readlines()

    def parse_values(self):
        return [(int(val.group(1)), val.group(2))
                for line in self.instructions
                if (val := re.match(r'value (\d+) goes to (bot \d+)', line))]

    def parse_allocations(self):
        return [alloc.groups()
                for line in self.instructions
                if (alloc := re.match(r'(bot \d+) gives low to (\w+ \d+) and high to (\w+ \d+)', line))]

    def setup_bins(self, allocations):
        bins = collections.defaultdict(lambda: lambda x: x)

        def config_bot(low_recipient, high_recipient):
            def awaiting_first_chip(a):
                def awaiting_second_chip(b):
                    low_chip, high_chip = sorted((a, b))
                    bins[low_recipient] = bins[low_recipient](low_chip)
                    bins[high_recipient] = bins[high_recipient](high_chip)
                    return low_chip, high_chip

                return awaiting_second_chip

            return awaiting_first_chip

        for bot, low, high in allocations:
            bins[bot] = config_bot(low, high)

        return bins

    def part1(self):
        bins = self.setup_bins(self.parse_allocations())

        for val, bot in self.parse_values():
            bins[bot] = bins[bot](val)
        return next(bot for bot, allocated in bins.items() if allocated == (17, 61))

    def part2(self):
        self.bins = self.setup_bins(self.parse_allocations())

        for val, bot in self.parse_values():
            self.bins[bot] = self.bins[bot](val)

        return math.prod(self.bins['output {}'.format(i)] for i in range(3))


Sample_Input = BotBalancer('input.txt')
print(Sample_Input.part1())
print(Sample_Input.part2())
