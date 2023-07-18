"""This is an example on running HydroShoot on a potted grapevine with a
simple shoot architecture.
"""

from json import load, dump
from pathlib import Path

from openalea.mtg import traversal, mtg
from openalea.mtg.mtg import MTG
from openalea.plantgl.all import Scene
from hydroshoot import architecture, display
from hydroshoot import io, initialisation

import vberry
from vberry.virtual_berry import virtual_berry
from vberry.data_samples import input_data


import pandas as pd

import scenarios.hyshoot_vberry.hs_wrapper as hs_wrapper


def build_mtg(path_file: Path, is_show_scene: bool = True) -> (mtg.MTG, Scene):
    grapevine_mtg = architecture.vine_mtg(file_path=path_file)

    for v in traversal.iter_mtg2(grapevine_mtg, grapevine_mtg.root):
        architecture.vine_phyto_modular(grapevine_mtg, v)
        architecture.vine_mtg_properties(grapevine_mtg, v)
        architecture.vine_mtg_geometry(grapevine_mtg, v)
        architecture.vine_transform(grapevine_mtg, v)

    # Display of the plant mock-up (result in 'fig_01_plant_mock_up.png')
    mtg_scene = display.visu(grapevine_mtg, def_elmnt_color_dict=True, scene=Scene(), view_result=is_show_scene)
    return grapevine_mtg, mtg_scene


def preprocess_inputs(grapevine_mtg: MTG, path_project_dir: Path, psi_soil: float, gdd_since_budbreak: float,
                      scene: Scene):
    inputs = io.HydroShootInputs(g=grapevine_mtg, path_project=path_project_dir, user_params=None,
                                 path_weather=path_project / 'meteo.input', scene=scene, psi_soil=psi_soil,
                                 gdd_since_budbreak=gdd_since_budbreak)
    io.verify_inputs(g=grapevine_mtg, inputs=inputs)
    grapevine_mtg = initialisation.init_model(g=grapevine_mtg, inputs=inputs)

    static_data = {'form_factors': {s: grapevine_mtg.property(s) for s in ('ff_sky', 'ff_leaves', 'ff_soil')}}
    static_data.update({'Na': grapevine_mtg.property('Na')})

    dynamic_data = {}
    inputs_hourly = io.HydroShootHourlyInputs(psi_soil=inputs.psi_soil_forced, sun2scene=inputs.sun2scene)
    for date_sim in inputs.params.simulation.date_range:
        inputs_hourly.update(
            g=grapevine_mtg, date_sim=date_sim, hourly_weather=inputs.weather[inputs.weather.index == date_sim],
            psi_pd=inputs.psi_pd, params=inputs.params)

        grapevine_mtg, diffuse_to_total_irradiance_ratio = initialisation.init_hourly(
            g=grapevine_mtg, inputs_hourly=inputs_hourly, leaf_ppfd=inputs.leaf_ppfd,
            params=inputs.params)

        dynamic_data.update({grapevine_mtg.date: {
            'diffuse_to_total_irradiance_ratio': diffuse_to_total_irradiance_ratio,
            'Ei': grapevine_mtg.property('Ei'),
            'Eabs': grapevine_mtg.property('Eabs')}})

    path_preprocessed_inputs = path_project_dir / 'preprocessed_inputs'
    with open(path_preprocessed_inputs / 'static.json', mode='w') as f_prop:
        dump(static_data, f_prop)
    pass
    with open(path_preprocessed_inputs / 'dynamic.json', mode='w') as f_prop:
        dump(dynamic_data, f_prop)
    pass


path_project = Path("C:\GitModeles\GrapeInSilico\scenarios\hyshoot_vberry\sim_with_preprocessed_inputs.py").parent
path_preprocessed_data = path_project / 'preprocessed_inputs'
path_output = path_project / 'output' / 'time_series_with_preprocessed_data3.csv'

g, scene = build_mtg(path_file=path_project / 'grapevine_pot.csv', is_show_scene=False)
# preprocess_inputs(grapevine_mtg=g, path_project_dir=path_project, psi_soil=-0.5, gdd_since_budbreak=1000., scene=scene)

with open(path_preprocessed_data / 'static.json') as f:
        static_inputs = load(f)
with open(path_preprocessed_data / 'dynamic.json') as f:
        dynamic_inputs = load(f)

path_weather = r'C:\GitModeles\GrapeInSilico\scenarios\hyshoot_vberry\meteo.input'

summary_results = hs_wrapper.run(g=g, wd=path_project, scene=scene, gdd_since_budbreak=1000.,
                                     form_factors=static_inputs['form_factors'],
                                     leaf_nitrogen=static_inputs['Na'],
                                     leaf_ppfd=dynamic_inputs,
                                     path_weather=path_weather,
                                     grape_vid=9,
                                     path_output=path_project / 'output' / 'time_series_with_preprocessed_data3.csv')

summary_results.psi_grape

inputs = io.HydroShootInputs(
    path_project=path_project,
    user_params=None,
    scene=scene,
    write_result=True,
    path_output_file=path_output,
    path_weather=path_weather,
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

psi_grape_bar = summary_results.psi_grape * 10

DATA_input.insert(3, "PTLx", psi_grape_bar.values.tolist())



virtual_berry(DATA_input.reset_index())