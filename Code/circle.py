import matplotlib.pyplot as plt

circle = plt.Circle((0,0),5, fill=False)

fig, ax = plt.subplots()
ax.add_artist(circle)
ax.set_xlim((-10, 10))
ax.set_ylim((-10, 10))
plt.show()
