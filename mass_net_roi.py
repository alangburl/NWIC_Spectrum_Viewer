import matplotlib.pyplot as plt

net_counts=[0.88,0.28,0.24,0.27,0.27,0.22,0.19,0.15,0.09]
mass=[51.4,50.0,45,40,35,30,25,20,15]

err=[1.1,0.83,0.81,0.83,0.83,0.79,0.77,0.75,0.71]

plt.errorbar(mass, net_counts, yerr=err,linestyle='None',marker='*')
plt.xlabel('Mass (lbs)')
plt.ylabel('Net ROI Count Rate (cps)')
plt.savefig('Reflection_mass_roi.png',dpi=600)
plt.show()

net_counts=[0.41,0.18,0.17,0.16,0.14,0.12,0.13,0.08,0.05]
mass=[51.4,50.0,45,40,35,30,25,20,15]

err=[.81,0.65,0.65,0.64,0.64,0.62,0.60,0.57,0.54]
plt.figure(2)
plt.errorbar(mass, net_counts, yerr=err,linestyle='None',marker='*')
plt.xlabel('Mass (lbs)')
plt.ylabel('Net ROI Count Rate (cps)')
plt.savefig('transmission_mass_roi.png',dpi=600)
plt.show()