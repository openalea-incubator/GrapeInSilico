import scenarios.hyshoot_vberry.sim_with_preprocessed_inputs as hydroshoot_sim
import vberry
from vberry.virtual_berry import virtual_berry
import pandas as pd
from hydroshoot import io
import matplotlib.pyplot as plt

inputs = io.HydroShootInputs(
    path_project=hydroshoot_sim.path_project,
    user_params=None,
    scene=hydroshoot_sim.scene,
    write_result=True,
    path_output_file=hydroshoot_sim.path_output,
    path_weather=hydroshoot_sim.path_weather,
    gdd_since_budbreak=1000.)

useful_weather = pd.DataFrame({})

for date in inputs.params.simulation.date_range:
    useful_weather = pd.concat([useful_weather, inputs.weather[inputs.weather.index == date]])

DATA_input = pd.DataFrame({})

Tps = [i for i in range(96,96+len(useful_weather))]

useful_weather[['Tac','hs']]

DATA_input = useful_weather[['Tac','hs']]
DATA_input.insert(0,"Tps",Tps)

# HS est megapascal,  VB est en bar.

Original_Input_Data = pd.read_csv(vberry.data_samples.input_data(), sep='\t')
Original_Input_Data = Original_Input_Data.set_index('Tps')

useful_cp=Original_Input_Data[0:len(DATA_input)]['Cp']
DATA_input.insert(3, "Cp", useful_cp.values.tolist())
DATA_input = DATA_input.set_index('Tps')

def simulation(grape_vertex,DATA_in=DATA_input.copy()):
    psi_grape_bar = hydroshoot_sim.summary_results(grape_vertex).psi_grape * 10

    print(DATA_in)
    DATA_in.insert(3, "PTLx", psi_grape_bar.values.tolist())
    DATA_in = DATA_in.rename(columns={'Tac': 'Temp', 'hs': 'RH'})

    return(virtual_berry(DATA_in.reset_index()))

result1=simulation(9)

result2=simulation(34,DATA_in=DATA_input.copy()) # we have to put the copy command again explicitely otherwise it does not make a new copy of the table, but rather reuses the one it made earlier !
result3=simulation(82,DATA_in=DATA_input.copy())
result4=simulation(106,DATA_in=DATA_input.copy())
# %gui qt5

result1.plot(x="Tps",y="FFW",color="#4CAF50",linestyle="-",alpha=0.5,  linewidth = '1')
plt.show()
plt.plot(result2["Tps"],result2["FFW"],color='r', linestyle='-', alpha=0.5,  linewidth = '0.8')

plt.plot(result3["Tps"],result3["FFW"],color='k', linestyle=':', alpha=0.9,  linewidth = '1.8')

plt.plot(result4["Tps"],result4["FFW"],color='m', linestyle=':', alpha=0.5,  linewidth = '1')

plt.ylim(0.025, 0.095)
plt.xticks(list(range(193))[96:193:24],[-0.30,-0.12,-0.89,-0.20,""])


z=plt.axvline(x = 140, color = 'b', label = 'axvline - full height')