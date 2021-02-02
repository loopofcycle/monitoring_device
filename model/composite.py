import time
from abc import ABC, abstractmethod

class Component(ABC):
	def __init__(self, name):
		self.name = name
		self.parent = self
		self.value = None
		self.updated = time.time()

	def __str__(self):
		return self.name

	def get_composite(self):
		return None
	

class Composite(Component):

	def __init__(self, name):
		self.tree = []
		super().__init__(name)

	def get_composite(self):
		return self.tree

	def add(self, component):
		component.parent = self
		self.tree.append(component)
	 
	def remove(self, component):
		self.tree.remove(component)
