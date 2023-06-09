import moments
import numpy as np

def model_func(params, ns):
	t1, nu11, t2, nu21 = params
	_Nanc_size = 1.0  # This value can be used in splits with fractions
	sts = moments.LinearSystem_1D.steady_state_1D(np.sum(ns))
	fs = moments.Spectrum(sts)
	nu1_func = lambda t: _Nanc_size + (nu11 - _Nanc_size) * (t / t1)
	fs.integrate(tf=t1, Npop=lambda t: [nu1_func(t)], dt_fac=0.01)
	fs.integrate(tf=t2, Npop=[nu21], dt_fac=0.01)
	return fs

data = moments.Spectrum.from_file('/home/jupyter-user_workshop/GADMA_workshops/SMSC_workshop/outputs/easySFS_output/dadi/NN-10.sfs')
ns = data.sample_sizes

p0 = [1.8239527996618337, 7.757108406614604, 0.0050532762571613805, 0.013512780816844424]
lower_bound = [1e-15, 0.0001, 1e-15, 0.0001]
upper_bound = [5.0, 100.0, 5.0, 100.0]
model = model_func(p0, ns)
ll_model = moments.Inference.ll_multinom(model, data)
print('Model log likelihood (LL(model, data)): {0}'.format(ll_model))

theta = moments.Inference.optimal_sfs_scaling(model, data)
print('Optimal value of theta: {0}'.format(theta))

Nanc = 974.2001139134609
mu = 1.554e-08
L = 2329306282
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
                             nref=974,
                             gen_time=7.0,
                             gen_time_units='years',
                             reverse_timeline=True)