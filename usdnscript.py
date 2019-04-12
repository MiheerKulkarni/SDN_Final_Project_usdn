import xlrd
import re
import matplotlib.pyplot as plt
from math import sqrt

loc = ("loglistnerusdn.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

sheet.cell_value(0,0)

message = []
mote = []
for i in range(1,sheet.nrows):
    message.append(sheet.cell_value(i,2))
    mote.append(sheet.cell_value(i,1))

power = []
for msg in message:
    if '[STAT: SDN-STAT  ] PW' in msg:
        power.append(msg)

new = []

for p in power:
    pow = re.findall('\d+|\D+',p)
    for n in pow:
        new.append([int(s) for s in n.split() if s.isdigit()])
brac = []
for i in new:

    brac.append(",".join(map(str,i)))

power_list = []

for b in brac:
    s =int(b.strip() or 0)
    power_list.append(s)


sum =0
AvRTT = 0
energy_dict = {9:28.588,3:18.788,7:20.388,5:18.688,8:21.588,11:21.288,10:22.188,6:17.888,4:20.288,1:32.012}
rtt_dict = {9:198.69,3:196.89,7:196.78,5:196.89,8:196.81,11:196.85,1:187.12,10:196.84,6:191.79,4:196.88}
delay_dict = {6:230,11:160,10:230,4:234}
for j in power_list:
    if j >= 500:
        sum = sum + j

    else:
        AvRTT = AvRTT + j

mean_energy = sum/10
mean_energy = mean_energy/1000
AvRTT = AvRTT/10
sd_rtt = []
sd_energy = []
for pos in power_list:
    if pos >=500:
        sd_energy.append(sqrt(((pos - mean_energy)**2)/len(energy_dict)))
    else:
        sd_rtt.append(sqrt(((pos - AvRTT)**2)/len(rtt_dict)))

final_sd_energy =0
final_sd_rtt =0
for sd in sd_energy:
    final_sd_energy = sd + final_sd_energy

for sd in sd_rtt:
    final_sd_rtt = sd+final_sd_rtt


print("Average energy consumption is:" + str(mean_energy) + " J")
print("Average RTT is :" + str(AvRTT)+ "ms")
print("Standard Deviation of energy" + str(final_sd_energy/10000) + " J")
print("Standard Deviation of RTT" + str(final_sd_rtt/10000) + " ms")

plt.figure('Figure for energy consumption')
plt.bar(list(energy_dict.keys()),list(energy_dict.values()))
plt.xlabel('Motes')
plt.ylabel('Energy in (J)')
plt.show()

plt.figure('Figure for RTT')
plt.bar(list(rtt_dict.keys()),list(rtt_dict.values()))
plt.xlabel('Motes')
plt.ylabel('Round-Trip time (ms)')
plt.show()

total_delay = 0
sd_delay = []
for d in delay_dict.values():
    total_delay = total_delay + d



avg_delay = total_delay/len(delay_dict)
for sdd in delay_dict.values():
    sd_delay.append(sqrt(((int(sdd) - avg_delay)**2)/len(delay_dict)))

final_sd_delay = 0
for de in sd_delay:
    final_sd_delay = final_sd_delay + de

final_sd_delay = final_sd_delay/(len(sd_delay))

print("The average delay is: " +str(avg_delay) +"ms")
print("The standard deviation of delay is: " +str(final_sd_delay)+ "ms")

plt.figure('Figure for delay')
plt.bar(list(delay_dict.keys()),list(delay_dict.values()))
plt.xlabel('Motes')
plt.ylabel('Delay in (ms)')
plt.show()






