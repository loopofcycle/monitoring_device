import json, os, time
from model.models import System
tree_json_path = os.path.join('/home/pi/projects/monitoring/settings/structure.json')

tree_dict = json.load(open(tree_json_path))

if __name__ == '__main__':
	sys = System('alfascan_kazan')
	sys.create_tree(tree_dict)
	while True:
		sys.update()
		sys.log()
		sys.send()
		sys.show_tree()
		time.sleep(5)
