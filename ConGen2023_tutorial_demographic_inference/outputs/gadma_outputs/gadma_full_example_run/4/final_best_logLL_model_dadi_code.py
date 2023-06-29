import dadi
import numpy as np

def model_func(params, ns, pts):
	t1, nu11, t2, nu21 = params
	_Nanc_size = 1.0  # This value can be used in splits with fractions
	xx = dadi.Numerics.default_grid(pts)
	phi = dadi.PhiManip.phi_1D(xx)
	phi = dadi.Integration.one_pop(phi, xx, T=t1, nu=nu11)
	nu1_func = lambda t: nu11 + (nu21 - nu11) * (t / t2)
	phi = dadi.Integration.one_pop(phi, xx, T=t2, nu=nu1_func)
	sfs = dadi.Spectrum.from_phi(phi, ns, [xx]*len(ns))
	return sfs

data = dadi.Spectrum.from_file('/home/enoskova/Workspace/GADMA_workshops/ConGen2023_tutorial_demographic_inference/outputs/easySFS_output/dadi/NN-10.sfs')
pts = [10, 20, 30]
ns = data.sample_sizes

p0 = [1.1068231416018231e-08, 0.04719738349112105, 0.0019630495513878253, 0.00031554429085266114]
lower_bound = [1e-15, 1e-05, 1e-15, 1e-05]
upper_bound = [5.0, 100.0, 5.0, 100.0]
func_ex = dadi.Numerics.make_extrap_log_func(model_func)
model = func_ex(p0, ns, pts)
ll_model = dadi.Inference.ll_multinom(model, data)
print('Model log likelihood (LL(model, data)): {0}'.format(ll_model))

theta = dadi.Inference.optimal_sfs_scaling(model, data)
print('Optimal value of theta: {0}'.format(theta))

Nanc = 1739.448901127648
mu = 1.554e-08
L = 2329306282
theta0 = 4 * mu * L
Nanc = int(theta / theta0)
print('Size of ancestral population: {0}'.format(Nanc))
