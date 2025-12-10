import moments
import numpy as np

def model_func(params, ns):
	t1, nu11 = params
	_Nanc_size = 1.0  # This value can be used in splits with fractions
	sts = moments.LinearSystem_1D.steady_state_1D(np.sum(ns))
	fs = moments.Spectrum(sts)
	nu1_func = lambda t: _Nanc_size + (nu11 - _Nanc_size) * (t / t1)
	fs.integrate(tf=t1, Npop=lambda t: [nu1_func(t)], dt_fac=0.01)
	return fs

data = moments.Spectrum.from_file('/home/enoskova/Workspace/GADMA_workshops/2025-12-Demographic_Inference_Worshop/tutorials/2_GADMA_tutorial/outputs/easySFS_output/dadi/NN-10.sfs')
ns = data.sample_sizes

p0 = [0.06878536933156319, 0.029006452134392128]
lower_bound = [1e-15, 0.01]
upper_bound = [5.0, 100.0]
model = model_func(p0, ns)
ll_model = moments.Inference.ll_multinom(model, data)
print('Model log likelihood (LL(model, data)): {0}'.format(ll_model))

theta = moments.Inference.optimal_sfs_scaling(model, data)
print('Optimal value of theta: {0}'.format(theta))

Nanc = 340629.0293180597
mu = 1.554e-08
L = 118000000
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
                             pop_labels=['NN'],
                             nref=340629,
                             gen_time=1.0,
                             gen_time_units='generations',
                             reverse_timeline=True)