import warnings
from numpy import clip, minimum, isfinite, all


def _poisson_normalise_extreme_values(y):
    max_val = 25000.
    if y.values.max() > max_val:
        msg = "Output values of Poisson likelihood greater"
        msg += " than {} is set to {} before applying GLMM."
        msg = msg.format(max_val, max_val)
        warnings.warn(msg)
    y.values[:] = clip(y.values, 0., max_val)


def _binomial_normalise_extreme_values(y):
    max_val = 300
    v = y.values
    ratio = v[:, 0] / v[:, 1]
    v[:, 1] = minimum(v[:, 1], max_val)
    v[:, 0] = ratio * v[:, 1]
    v[:, 0] = v[:, 0].round()
    y.values[:] = v


def normalise_extreme_values(y, likelihood):
    if not all(isfinite(y)):
        msg = "There are non-finite values in the the provided phenotype."
        raise ValueError(msg)

    if likelihood == "poisson":
        _poisson_normalise_extreme_values(y)
    elif likelihood == "binomial":
        _binomial_normalise_extreme_values(y)

    return y


def assert_likelihood_name(likname):
    likname = likname.lower()
    valid_names = set(["normal", "bernoulli", "probit", "binomial", "poisson"])
    if likname not in valid_names:
        msg = f"Unrecognized likelihood name: {likname}.\n"
        msg += f"Valid names are: {valid_names}."
        raise ValueError(msg)