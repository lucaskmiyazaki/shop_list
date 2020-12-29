from food import Food

class Menu:
	def __init__(self, dish_list):
		self.menu = []
		self.dish_list = dish_list

	def get_list(self):
		for dish_name in self.dish_list:
			meal = Food(dish_name)
			self.menu.append(meal.get_list())

		return {'menu': self.menu}