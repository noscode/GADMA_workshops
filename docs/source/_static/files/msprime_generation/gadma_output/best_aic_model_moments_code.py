import moments
import numpy as np

def model_func(params, ns):
	 = params
	_Nanc_size = 1.0  # This value can be used in splits with fractions
	sts = moments.LinearSystem_1D.steady_state_1D(np.sum(ns))
	fs = moments.Spectrum(sts)
	return fs

data = moments.Spectrum.from_file('/Users/noskovae/Workspace/GADMA_workshops/docs/source/2024_18_11/files/msprime_generation/example_input.sfs')
ns = data.sample_sizes

p0 = []
lower_bound = []
upper_bound = []
model = model_func(p0, ns)
ll_model = moments.Inference.ll_multinom(model, data)
print('Model log likelihood (LL(model, data)): {0}'.format(ll_model))

theta = moments.Inference.optimal_sfs_scaling(model, data)
print('Optimal value of theta: {0}'.format(theta))

Nanc = 10096.9696969697
mu = 1.25e-08
L = 2000000
theta0 = 4 * mu * L
Nanc = int(theta / theta0)
print('Size of ancestral population: {0}'.format(Nanc))


plot_ns = [4 for _ in ns]  # small sizes for fast drawing
gen_mod = moments.ModelPlot.generate_model(model_func,
                                           p0, plot_ns)
moments.ModelPlot.plot_model(gen_mod,
                             save_file='model_from_GADMA.png',
                             fig_title='Demographic model from GADMA',
                             draw_scale=True,
                             pop_labels=['Pop1'],
                             nref=10096,
                             gen_time=1.0,
                             gen_time_units='generations',
                             reverse_timeline=True)