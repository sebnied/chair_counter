import re
import itertools


def find_target_row(room_name: str, layout_grid: list):
    target_row = None
    for y, row in enumerate(layout_grid):
        if room_name in row:
            target_row = y
            break
    return target_row


def find_chairs_in_row(row: str, chair_labels: list):
    return [char for char in row if char in chair_labels]


def split_row(row: list):
    # Updated pattern to include |, +, /, and \\ as delimiters
    parts = re.split(r'[|/+]', row)

    return parts[1:-1]


def get_room_index(room_label: str, cleaned_row: list):
    for index, string in enumerate(cleaned_row):
        if room_label in string:
            return index
    return -1


def update_room_index(row, room_index, rooms):
    if len(row) > rooms:
        for i, room in enumerate(row):
            if ("-" in room) and (i <= room_index) and (room_index < rooms):
                room_index += 1
    if len(row) < rooms and (room_index != 0):
        room_index -= rooms - len(row)
    return room_index


def count_chairs_single_direction(direction: str, room_name: str, chairs_in_room: list, layout_grid: list,
                                  chair_labels: list):

    assert direction in ['up', 'down'], "Direction must be either 'up' or 'down'"

    if direction == 'up':
        row = find_target_row(room_name, layout_grid)
    elif direction == 'down':
        row = find_target_row(room_name, layout_grid) + 1
    cleaned_target_row = split_row(layout_grid[find_target_row(room_name, layout_grid)])
    room_index = get_room_index(room_name, cleaned_target_row)
    rooms = len(cleaned_target_row)

    while True:
        cleaned_row = split_row(layout_grid[row])
        room_index = update_room_index(cleaned_row, room_index, rooms)
        if "-" in cleaned_row[room_index]:
            break
        rooms = len(cleaned_row)
        chairs_in_room.append(find_chairs_in_row(cleaned_row[room_index], chair_labels))
        if direction == 'up':
            row -= 1
        elif direction == 'down':
            row += 1

    return chairs_in_room


def count_chairs(room_name: str, layout_grid: list, chair_labels: list):
    chairs_in_room = list()
    chairs_in_room = count_chairs_single_direction('up', room_name, chairs_in_room, layout_grid, chair_labels)
    chairs_in_room = count_chairs_single_direction('down', room_name, chairs_in_room, layout_grid, chair_labels)
    return list(itertools.chain.from_iterable(chairs_in_room))


class ChairCounter:
    def __init__(
            self,
            floor_plan: str = 'rooms.txt',
            types_of_chairs: list = ['W', 'P', 'S', 'C']
    ):
        with open(floor_plan, 'r') as file:
            self.floor_plan = file.read()
        self.types_of_chairs = types_of_chairs
        self.room_labels = re.findall(r'\((.*?)\)', self.floor_plan)

    def count_all_chairs(self):
        chairs_dict = dict()
        expanded_floor_plan = self.floor_plan.splitlines()
        for room_label in self.room_labels:
            chairs_dict[room_label] = count_chairs(room_label, expanded_floor_plan, self.types_of_chairs)
        return chairs_dict


if __name__ == '__main__':

    chair_counter = ChairCounter()
    counted = chair_counter.count_all_chairs()

    # Output message print
    print(f"total:")
    total_chairs = [item for sublist in counted.values() for item in sublist]
    print(", ".join([f'{chair}: {total_chairs.count(chair)}' for chair in chair_counter.types_of_chairs]))

    for room_name in sorted(counted.keys()):
        print(f"{room_name}:")
        message = [f'{chair}: {counted[room_name].count(chair)}' for chair in chair_counter.types_of_chairs]
        print(", ".join(message))
