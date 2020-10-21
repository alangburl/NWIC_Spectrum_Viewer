import matplotlib.pyplot as plt
import numpy as np
mass=[15,20,25,30,35,40,45,50]
trans=[1377,858,426,209,245,189,194,150]
ref=[1183,587,294,173,162,150,183,112]

mass=[str(i) for i in mass]
width=0.35
x = np.arange(len(mass))  # the label locations
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, trans, width, label='Transmission')
rects2 = ax.bar(x + width/2, ref, width, label='Reflection')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time to 99% detection probability')
ax.set_xlabel('Mass (lbs)')
# ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(mass)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

fig.tight_layout()
plt.savefig('combined.png',dpi=600)

plt.show()
