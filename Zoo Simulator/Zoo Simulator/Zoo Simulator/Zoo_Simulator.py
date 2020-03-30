from Tkinter  import *
from random   import seed
from random   import uniform

def generate_number(low, high):
	seed()
	return uniform(low, high)

class Animal(object):
	max_health = 100.00
	health     = 100.00
	is_dead    = False

	def hunger(self, min_health):
		if not self.is_dead:
			self.health -= generate_number(0, 20)

			if self.health < min_health: 
				self.is_dead = True

	def feed(self):
		self.health += generate_number(10, 25)
		if self.health > self.max_health:
			self.health = self.max_health

class Monkey(Animal):
	name       = "Monkey"
	min_health = 30

	def hunger(self):
		super(Monkey, self).hunger(self.min_health)

class Giraffe(Animal):
	name       = "Giraffe"
	min_health = 50

	def hunger(self):
		super(Giraffe, self).hunger(self.min_health)

class Elephant(Animal):
	name             = "Elephant"
	min_health       = 70
	time_has_elapsed = False

	def hunger(self):
		if not self.is_dead:
			self.health -= generate_number(0, 20)
		
			if self.health < self.min_health:
				if self.time_has_elapsed:
					self.is_dead = True

				else:
					self.time_has_elapsed = True

	def feed(self):
		super(Elephant, self).feed()
		self.time_has_elapsed = False

class Zoo:
	time = 00.00
	animals = []

	def __init__(self):
		for i in range(15):
			if i < 5:
				self.animals.append(Monkey())
			elif i < 10:
				self.animals.append(Giraffe())
			else:
				self.animals.append(Elephant())

	def feed(self):
		for animal in self.animals:
			animal.feed()

	def next_hour(self):
		for animal in self.animals:
			animal.hunger()

		self.time += 01.00
		if self.time > 23.00:
			self.time = 00.00

class App(Frame):
	health_values = []

	def __init__(self, parent, zoo):
		Frame.__init__(self, parent)
		self.parent = parent
		self.zoo    = zoo

		self.time = StringVar(self)
		self.time.set('%.2f' % self.zoo.time)

		self.setup()

	def setup(self):
		self.parent.title("Zoo Simulator")

		top_frame = Frame(self.parent)
		Label(top_frame, text = "Time: ").pack(side = LEFT)
		Label(top_frame, textvariable = self.time).pack(side = LEFT)
		top_frame.pack(side = TOP)

		grid_frame = Frame(self.parent)
		Label(grid_frame, text = "Monkeys",   width = 10).grid(row = 0, column = 0)
		Label(grid_frame, text = "Giraffes",  width = 10).grid(row = 0, column = 1)
		Label(grid_frame, text = "Elephants", width = 10).grid(row = 0, column = 2)

		for i, animal in enumerate(self.zoo.animals):
			self.health_values.append(StringVar())
			self.health_values[i].set('%.2f' % animal.health + '%')

			if animal.name == "Monkey":
				Label(grid_frame, textvariable = self.health_values[i]).grid(row = i + 1, column = 0)

			elif animal.name == "Giraffe":
				Label(grid_frame, textvariable = self.health_values[i]).grid(row = i - 4, column = 1)

			elif animal.name == "Elephant":
				Label(grid_frame, textvariable = self.health_values[i]).grid(row = i - 9, column = 2)
				
		grid_frame.pack(expand = True)

		bottom_frame = Frame(self.parent)
		Button(bottom_frame, text = "Feed Animals",    command = self.feed_clicked).pack(side = LEFT, pady = 5)
		Button(bottom_frame, text = "Advance 1 Hour",  command = self.advance_time_clicked).pack(side = LEFT, pady = 5)
		bottom_frame.pack(side = BOTTOM)

	def run(self):
		self.mainloop()

	def update_values(self):
		self.time.set('%.2f' % self.zoo.time)

		for i, animal in enumerate(self.zoo.animals):
			if animal.is_dead:
				self.health_values[i].set("DEAD")
			else:
				self.health_values[i].set('%.2f' % animal.health + '%')

	def feed_clicked(self):
		self.zoo.feed()
		self.update_values()

	def advance_time_clicked(self):
		self.zoo.next_hour()
		self.update_values()

if __name__ == "__main__":
	App(Tk(), Zoo()).run()