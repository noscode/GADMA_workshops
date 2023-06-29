import momi
import numpy as np

def model_func(params):
	 = params

	model = momi.DemographicModel(
		N_e=1,
		gen_time=1,
		muts_per_gen=1.554e-08
	)


	model.add_leaf(
		pop_name='NN',
		t=0,
		N=1287.827247677082,
		g=0,
	)

	model.set_params({
	})
	return model


# Momi does not supports downsizing of the SFS so in this code there is no downsizing.
data = momi.sfs_from_dadi('/home/enoskova/Workspace/GADMA_workshops/ConGen2023_tutorial_demographic_inference/outputs/easySFS_output/dadi/NN-10.sfs')
data = data.fold()
data = data.subset_populations(['NN'])

params = []
model = model_func(params)
model.set_data(data, length=2329306282)
ll_model = model.log_likelihood()
print(f'Value of log-likelihood: {ll_model}')
from matplotlib import pyplot as plt
momi.DemographyPlot(
	model,
	pop_x_positions=data.sampled_pops,
	figsize=(6,8),
	linthreshy=None,
	pulse_color_bounds=(0,.25)
)
plt.savefig('model_from_GADMA.png')
