import momi
import numpy as np

def model_func(params):
	nu11, t1 = params

	model = momi.DemographicModel(
		N_e=1,
		gen_time=1,
		muts_per_gen=1.554e-08
	)

	model.add_time_param('t1', lower=2e-13, upper=10000000.0)
	model.add_size_param('nu11', lower=0.01, upper=100000000.0)

	model.add_leaf(
		pop_name='NN',
		t=0,
		N='nu11',
		g=lambda params: np.log(params.nu11 / params._Nanc_size) / params.t1,
	)
	model.set_size(
		pop_name='NN',
		t='t1',
		N=1774.511566131405,
		g=0,
	)

	model.set_params({
		'nu11': nu11,
		't1': t1,
	})
	return model


# Momi does not supports downsizing of the SFS so in this code there is no downsizing.
data = momi.sfs_from_dadi('/home/enoskova/Workspace/GADMA_workshop/outputs/easySFS_output/dadi/NN-10.sfs')
data = data.fold()
data = data.subset_populations(['NN'])

params = [43.99781470420896, 574.7900078945115]
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
