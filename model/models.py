import json, time, os, logging, pprint
from datetime import datetime
from model.composite import Composite, Component
from model.mqtt.mqtt_pub_sub import Publisher, Subscriber

class Sensor(Component):

	def __init__(self, name, path):
		super().__init__(name)
		self.path = path
		self.subscriber = Subscriber()
		self.publisher = Publisher()
		self.update()

	def send(self):
		self.topic = self.parent.topic + '/' + self.name
		self.publisher.execute(self.topic, self.value)


	def receive(self):
		self.topic = self.parent.topic + '/' + self.name
		self.value = self.subscriber.execute(self.topic)
		print(f'{self.name} receiving from topic {self.topic}')

	def update(self):
		print(f'updating {self.name}')
		with open(self.path) as file:
			data = file.read()
			self.value = float(data)/1000

	def log(self):
		date = str(datetime.fromtimestamp(time.mktime(time.localtime())))
		file_path = os.path.join(
					os.path.abspath('/home/pi/projects/monitoring/log'),
					str(date[:10] + '_'  + self.name + '.json'))
		entry = { date: self.value }
		if os.path.isfile(file_path):
			data = json.load(open(file_path, mode='r'))
			result = {**data, **entry}
			#pprint.pprint(result)
			json.dump(result, open(file_path, 'w'), indent=2)

		if not os.path.isfile(file_path):
			json.dump(entry, open(file_path, 'w'), indent=2)

	def __str__(self):
		return self.name + ': ' + str(self.value)

class System(Composite):

	def create_tree(self, structure={}):
		print(f'\n---creating tree structure for {self}')
		for component, attr in structure.items():
			if attr['type'] == 'component':
				print('\n*** creating component', component)
				self.add(Sensor(attr['name'], attr['path']))
			if attr['type'] == 'composite':
				print('\n--- creating composite component', component)
				sys = System(attr['name'])
				sys.create_tree(attr['tree'])
				self.add(sys)
		return self

	def show_tree(self, indent = 1):
		if indent == 1: print('\n\t\t System tree\n')
		prefix = indent * '\t'
		for component in self.tree:
			print(f'{prefix} ...-{component.topic}: {component.value}')
			if component.get_composite():
				component.show_tree(indent= indent + 1)

	def receive(self):
		if self == self.parent:
			self.topic = '/' + self.name
		else:
			self.topic = self.parent.topic + '/' + self.name 
		for component in self.tree:
			component.receive()

	def update(self):
		print(f'updating {self}')
		for component in self.tree:
			component.update()

	def log(self):
		print(f'logging {self}')
		for component in self.tree:
			component.log()

	def send(self):
		if self == self.parent:
			self.topic = '/' + self.name
		else:
			self.topic = self.parent.topic + '/' + self.name
		for component in self.tree:
			component.send()
