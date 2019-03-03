from random import randint

# Variables used to travel in different directions
up, down, left, right = 0, 1, 2, 3
all_directions = [up, down, left, right]
x_offset = [0, 0, -1, 1]
y_offset = [-1, 1, 0, 0]


class Swag:
  
  def __init__(self, swag_list = []):
    self.swag = swag_list
    self.count = len(swag_list)

  def get_swag(self):
    return self.swag

  def add_to_swag(self, item):
    self.swag.append(item)

  def select_random_swag(self):
    return self.swag[randint(0, self.count - 1)]

  def sort_swag(self):
    """
    Use radix sort to sort the collected swag based on the ASCII equivalent
    of the starting lower-case letter of the swag's description.
    For example, 'apple' starts with 'a', and the ASCII value of 'a' is 97.
    This will work because the ASCII values increase in order as we traverse
    the alphabet from 'a' to 'z'.
    """
    swag_conversion = {}
    for item in self.swag:
      swag_conversion.update({ord(item[0]) : item})
    being_sorted = [ord(item[0]) for item in self.swag]
    max_val = max(being_sorted)
    max_exp = len(str(max_val))
    for exp in range(max_exp):
      pos = exp + 1
      index = -pos
      digits = [[] for i in range(10)]
      for ascii_val in being_sorted:
        # See if the ASCII value needs to be left-padded with a zero.
        ascii_val_as_a_string = str(ascii_val)
        try:
          digit = ascii_val_as_a_string[index]
        except IndexError:
          digit = 0
        digit = int(digit)
        digits[digit].append(ascii_val)
      being_sorted = []
      for numeral in digits:
        being_sorted.extend(numeral)
      sorted_swag = Swag([swag_conversion[key] for key in being_sorted])
    return sorted_swag

  def print_swag(self):
    print('\nYour swag:\n')
    swag_count = 0
    current_item = None
    item_count = 0
    for item in self.swag:     
      swag_count += 1
      if current_item != None:
        if item != current_item:
          print('{0} ({1})'.format(current_item, item_count))
          current_item = item
          item_count = 1
        else:
          item_count += 1
      else:
        current_item = item
        item_count = 1
    if item_count > 0:
      print('{0} ({1})'.format(current_item, item_count))
    if swag_count > 0:
      print('\nCongratulations!  You have collected {0} items.'.format(swag_count))
    else:
      print('You did not collect any swag.  We wish you more success next time.')


class Maze:
  
  def __init__(self, vertical_dimension = 0, horizontal_dimension = 0, dispersed_swag = Swag()):

    self.m, self.n = vertical_dimension, horizontal_dimension
    self.swag = dispersed_swag
    self.collected_swag = Swag()
    self.grid = []
    for i in range(self.m):
      row = []
      for j in range(self.n):
        row.append('wall')
      self.grid.append(row)
    self.neighbors = []
    self.start_i, self.start_j = randint(0, self.m - 1), randint(0, self.n-1)
    self.grid[self.start_i][self.start_j] = 'start'
    self.mow(self.start_i, self.start_j)
    self.explore_maze()

  def mow(self, i, j):
    directions = all_directions.copy()
    while directions:
      directions_index = randint(0, len(directions) - 1)
      cells_to_mow = 3
      direction = directions.pop(directions_index)
      new_i, new_j = i + y_offset[direction]*cells_to_mow, j + x_offset[direction]*cells_to_mow
      if new_i < 0 or new_j < 0:
        continue
      try:
        new_cell = self.grid[new_i][new_j]
      except IndexError:
        continue
      if new_cell == 'wall':
        if x_offset[direction] != 0:
          x_step  = int(x_offset[direction]/abs(x_offset[direction]))
          x_start = j + x_step
          x_stop  = j + x_offset[direction]*cells_to_mow + x_step
          for next_j in range(x_start, x_stop, x_step):
            self.grid[i][next_j] = 'empty'
        if y_offset[direction] != 0:
          y_step  = int(y_offset[direction]/abs(y_offset[direction]))
          y_start = i + y_step
          y_stop  = i + y_offset[direction]*cells_to_mow + y_step
          for next_i in range(y_start, y_stop, y_step):
            self.grid[next_i][j] = 'empty'
        self.mow(new_i, new_j)
   
  def explore_maze(self):
    grid_copy  = [row[:] for row in self.grid]
    self.neighbors  = [[[] for col in row] for row in self.grid]
    bfs_queue  = [[self.start_i, self.start_j]]
    directions = all_directions.copy()
    while bfs_queue:
      i, j = bfs_queue.pop(0)
      if not ( i == self.start_i and j == self.start_j ):
        if randint(1, 10) == 5:
          self.grid[i][j] = self.swag.select_random_swag()
      grid_copy[i][j] = 'visited'
      for direction in directions:
        explore_i, explore_j = i + y_offset[direction], j + x_offset[direction]
        if explore_i < 0 or explore_j < 0:
          continue
        try:
          new_cell = self.grid[explore_i][explore_j]
        except IndexError:
          continue
        if new_cell != 'wall' and grid_copy[explore_i][explore_j] != 'visited':
          bfs_queue.append([explore_i, explore_j])
        if new_cell != 'wall':
          self.neighbors[i][j].append([explore_i, explore_j])
    self.grid[i][j] = 'end'
    
  def print_maze(self):
    border_char = '#'
    horizontal_border = border_char
    for i in range(self.n + 1):
      horizontal_border += border_char
    print(horizontal_border)
    for row in self.grid:
      printable_row = border_char
      for cell in row:
        if cell == 'wall':
          char = '|'
        elif cell == 'empty':
          char = ' '
        else:
          char = cell[0]
        printable_row += char
      printable_row += border_char
      print(printable_row)
    print(horizontal_border)

  def solve_maze(self):
    self.dfs([self.start_i, self.start_j])

  def dfs(self, current_cell, visited = None):
    cell_content = self.grid[current_cell[0]][current_cell[1]]
    if visited is None:
      visited = []
    visited.append(current_cell)
    if cell_content not in ['start', 'end']:
      if cell_content in self.swag.get_swag():
        self.collected_swag.add_to_swag(cell_content)
      self.grid[current_cell[0]][current_cell[1]] = '*'
    if cell_content == 'end':  # We made it to the end!
      return visited
    neighbors = self.neighbors[current_cell[0]][current_cell[1]]
    for neighbor in neighbors:
      if neighbor not in visited:
        path = self.dfs(neighbor, visited)
        if path:
          return path

  def print_collected_swag(self):
    self.collected_swag.sort_swag().print_swag()


#################################################################################
fall_swag = Swag(['three musketeers', 'candy corn', 'raisinettes', 'donut', 'gourd', 'hershey kisses', 'apple', 'm&ms', 'pumpkin'])      
corn_maze = Maze(25, 75, fall_swag)
corn_maze.print_maze()
print('\nHere is your maze.  How much swag can you find as you make your way to the end?')
input('Press enter to continue.\n')
corn_maze.solve_maze()
print('\nHere is how you found your way through the maze.\n')
corn_maze.print_maze()
input('\nPress enter to see the cool swag you collected!\n')
corn_maze.print_collected_swag()





