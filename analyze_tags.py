import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

f = open('tags_v4.csv', 'r')

tags = []

for line in f:
    line = line.split(',')
    
    for tag in line:
        if tag == '\n' or tag == '':
            continue
        tags.append(tag)

# Make tags lowercase
for i in range(len(tags)):
    tags[i] = tags[i].lower()

# count occurences of tabs und speicher in nem dict
sorted_by_occurence = [item for items, c in Counter(tags).most_common() for item in [items] * c]

dict_with_occurences = Counter(tags)
dict_with_occurences = {k: v for k, v in sorted(dict_with_occurences.items(), key=lambda item: item[1], reverse=True)}

counts = list(dict_with_occurences.values())
names = list(dict_with_occurences.keys())

max_index = 100 # defines number of tags displayed

fig, ax = plt.subplots()
fig.set_size_inches(15/2.52, 74/2.52)


font = {'size'   : 5}

plt.rc('font', **font)

plt.scatter([],[], label='Anzahl Videos: 32042', c='black')
plt.scatter([],[], label='Anzahl individueller Tags: ' + str(len(dict_with_occurences)), c='black')


plt.barh(names[:max_index],counts[:max_index], color='red')
plt.legend()
plt.tight_layout()
plt.savefig('tags_count.png', dpi=500)
plt.show()



class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        """
        Setup for bubble collapse.

        Parameters
        ----------
        area : array-like
            Area of the bubbles.
        bubble_spacing : float, default: 0
            Minimal spacing between bubbles after collapsing.

        Notes
        -----
        If "area" is sorted, the results might look weird.
        """
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        # calculate initial grid layout for bubbles
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) == np.ndarray else [idx_min]

    def collapse(self, n_iterations=50):
        """
        Move bubbles to the center of mass.

        Parameters
        ----------
        n_iterations : int, default: 50
            Number of moves to perform.
        """
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                # try to move directly towards the center of mass
                # direction vector from bubble to the center of mass
                dir_vec = self.com - self.bubbles[i, :2]

                # shorten direction vector to have length of 1
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                # calculate new bubble position
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                # check whether new bubble collides with other bubbles
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    # try to move around a bubble that you collide with
                    # find colliding bubble
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        """
        Draw the bubble plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
        labels : list
            Labels of the bubbles.
        colors : list
            Colors of the bubbles.
        """
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')


bubble_chart = BubbleChart(area=counts[:max_index],
                           bubble_spacing=5)

bubble_chart.collapse()

import random


fig, ax = plt.subplots()
fig.set_size_inches(40/2.52, 40/2.52)


counts = list(dict_with_occurences.values())
names = list(dict_with_occurences.keys())





def get_color(count):
    cmap = plt.cm.get_cmap('rainbow')

    colors = ['tab:red', 'tab:blue', 'tab:orange', 'tab:pink', 'tab:green', 'tab:purple', 'tab:brown', 'tab:olive', 'tab:cyan']
    return cmap((float(count)-np.min(counts)) /  (float(np.max(counts)-np.min(counts))))


fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
bubble_chart.plot(
    ax, names[:max_index], [get_color(count) for count in counts[:max_index]])
ax.axis("off")
ax.relim()
ax.autoscale_view()
ax.set_title('video tags in watch history', fontdict={'size': 20})
plt.tight_layout()
plt.savefig('tags_circles.png', dpi=500)
plt.show()
