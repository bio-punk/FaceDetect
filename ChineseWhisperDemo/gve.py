import networkx
from matplotlib import pyplot as plot
import random
from collections import Counter

def get_max_color(x, e, G):
	color_list = [G.node[x]['color']]
	for (v1, v2) in e:
		if (v1 == x):
			color_list.append(G.node[v2]['color'])
		if (v2 == x):
			color_list.append(G.node[v1]['color'])
	color_counts = Counter(color_list)
	(top_color, top_color_count) = color_counts.most_common(1)[0]
	return top_color


G = networkx.Graph()
node_list=range(1,12)
G.add_nodes_from(node_list, color='#ff0000')
edge_list = [
(6,7), (6,8), (6,10), (6,11), (9,10), (9,11), 
(1,2), (1,3), (1,4), (1,5), (1,11), (2, 4), (2,5), (2, 3), (3, 4), (3, 5), (4, 5), (7,10), (10,11), (11,8), (8,9), (9,7)]

G.add_edges_from(edge_list)

G.node[1]['color'] = '#ff0000'
G.node[2]['color'] = '#FFC0CB'
G.node[3]['color'] = '#C71585'
G.node[4]['color'] = '#800080'
G.node[5]['color'] = '#BC8F8F'
G.node[6]['color'] = '#0000FF'
G.node[7]['color'] = '#778899'
G.node[8]['color'] = '#5F9EA0'
G.node[9]['color'] = '#40E0D0'
G.node[10]['color'] = '#006400'
G.node[11]['color'] = '#DAA520'

node_color=[G.node[v]['color'] for v in G]
networkx.draw(G, with_labels=True, node_color=node_color, pos=networkx.circular_layout(G), font_color='#ffffff')
plot.text(0.5, 1, 'chinese whisper Clan: 0')
plot.show()

random.shuffle(node_list)

for cwNum in range(4):
	for now_node in node_list:
		color = get_max_color(now_node, edge_list, G)
		G.node[now_node]['color'] = color

	node_color=[G.node[v]['color'] for v in G]
	networkx.draw(G, with_labels=True, node_color=node_color, pos=networkx.circular_layout(G), font_color='#ffffff')
	plot.text(0.5, 1, 'chinese whisper Clan: {}'.format(cwNum + 1))
	plot.show()
