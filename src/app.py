import re
import collections
from db import Database


class BotBalancer:

    """

    This class aims to balance the load of the bots

    In order to use it you can import it in other modules and initialize it with input file directory

    """

    def __init__(self, input_file):

        """

        Initializes the class with the input file

        :param input_file: the input file containing the bots instructions

        """

        self.input_file = input_file
        self.read_instructions()
        self.bins = None
        self.database = Database()

    def read_instructions(self):

        """

        Reads the instructions from the input file

        :return: None

        """
        with open(self.input_file) as f:
            self.instructions = f.readlines()

    def parse_values(self):

        """

        Parses the values from the input file(A value given to specific bot)

        :return: list of tuples of bot and value

        """

        for line in self.instructions:
            if val := re.match(r"value (\d+) goes to bot (\d+)", line):
                self.database.execute(
                    f"""INSERT INTO allocations(chip,bot) VALUES({val.group(2)},{val.group(1)})"""
                )
                self.database.commit()
        return [
            (int(val.group(1)), val.group(2))
            for line in self.instructions
            if (val := re.match(r"value (\d+) goes to (bot \d+)", line))
        ]

    def parse_allocations(self):
        """

        Parses the allocations from the input file

        :return: Rules to give the chips to the other bots

        """

        return [
            alloc.groups()
            for line in self.instructions
            if (
                alloc := re.match(
                    r"(bot \d+) gives low to (\w+ \d+) and high to (\w+ \d+)", line
                )
            )
        ]

    def setup_bins(self, allocations):

        """

        Sets up the bins for the bots and logic to give the chips to the other bots

        :param allocations: Rules to give the chips to the other bots from method parse_allocations

        :return: bins for the bots

        """

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

    def part1(self, chip_val_1, chip_val_2):

        """

        This function gets chip values and returns the bot number handling the chips and comparing them

        :param chip_val_1: LOW valued chip

        :param chip_val_2: HIGH valued chip

        :return: Bot number handling the chips

        """

        bins = self.setup_bins(self.parse_allocations())

        for val, bot in self.parse_values():
            bins[bot] = bins[bot](val)
        for bot, chips in bins.items():
            if type(chips) == tuple:
                chip_1 = chips[0]
                chip_2 = chips[1]
                self.database.execute(
                    f"""INSERT INTO bots(bot_id,chip_1_value,chip_2_value) VALUES({bot.replace("bot",
                                                                                                                 "")},{chip_1},{chip_2})"""
                )
                self.database.commit()
            else:
                self.database.execute(
                    f"""INSERT INTO outputs(output_id,chip_value) VALUES({bot.replace("output", "")},{chips})"""
                )
                self.database.commit()
        return self.database.cursor.execute(
            f"""SELECT * FROM bots WHERE chip_1_value={chip_val_1} AND chip_2_value={chip_val_2}"""
        ).fetchall()[0][0]

    def part2(self, output_id_list):

        """

        This function gets the output id list and returns the product of the chips values

        :param output_id_list: List of output ids for example [1,2,3]

        :return: product of the chips values

        """

        output_id_list.sort()
        chip_values_list = self.database.cursor.execute(
            f"""SELECT chip_value FROM outputs WHERE output_id>={output_id_list[0]} AND 
        output_id <= {output_id_list[-1]}"""
        ).fetchall()
        result = 1

        for index, chip_value in enumerate(chip_values_list):
            result *= chip_value[0]
        return result


if __name__ == "__main__":
    Sample_Input = BotBalancer("input.txt")
    print(Sample_Input.part1(17, 61))
    print(Sample_Input.part2([0, 1, 2]))
