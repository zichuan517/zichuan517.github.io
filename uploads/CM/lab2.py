import numpy as np

def g(t, x):
    return t + np.sin(x*t*t)

def h(x, y):
    return np.exp(x + y)

def trapezoid(n):
    w = np.ones(n+1)
    w[0] = w[-1] = 0.5
    return w

def simpson_weights(n):
    if n < 2 or n % 2 == 1:
        raise ValueError('Simpson formula requires n to be even and >= 2.')

    w = np.ones(n+1)
    w[1:-1:2] = 4
    w[2:-2:2] = 2
    return w / 3

def integrate(f, weights, a = 0, b = 1):
    n = len(weights) - 1
    t = np.linspace(a, b, n + 1)
    h = (b - a) / n
    return h * np.dot(weights, f(t))

def integrate_2d(f, wx, wy, ax = 0, bx = 0, ay = 0, by = 0):
    nx, ny = len(wx) - 1, len(wy) - 1

    x = np.linspace(ax, bx, nx + 1)
    y = np.linspace(ay, by, ny + 1)

    hx = (bx - ax) / nx
    hy = (by - ay) / ny

    values = f(x[:, None], y[None, :])

    return hx * hy * (wx @ values @ wy)

def convergence_order(f, weight_fn, n):
    """Return NaN when the integral differences cannot resolve an order."""
    I1 = integrate(f, weight_fn(n))
    I2 = integrate(f, weight_fn(2 * n))
    I4 = integrate(f, weight_fn(4 * n))

    d1 = abs(I1 - I2)
    d2 = abs(I4 - I2)

    # Scale the round-off threshold with the integrals, including small ones.
    scale = max(abs(I1), abs(I2), abs(I4))
    roundoff = 16 * np.finfo(float).eps * scale
    if d1 <= roundoff or d2 <= roundoff:
        return np.nan

    return np.log2(d1 / d2)

def romberg(f, a = 0, b = 1, eps = 1e-12, max_iter = 20):
    R_prev = [(b - a) * (f(a) + f(b)) /  2]

    for k in range(1, max_iter + 1):
        n = 2**k
        h = (b - a) / n

        t = a + h * np.arange(1, n, 2)
        T = R_prev[0] / 2 + h * np.sum(f(t))

        R = [T]
        for j in range(1, k + 1):
            R.append(R[j-1] + (R[j-1] - R_prev[j-1]) / (4**j - 1))

        if abs(R[-1] - R_prev[-1]) < eps:
            return R[-1], n

        R_prev = R

    raise RuntimeError('Romberg integration failed to converge.')


def experiment(x, weight_fn, ns):
    f = lambda t: g(t, x)
    print(f"\nx = {x}, method = {weight_fn.__name__}")
    print(f"{'n':>10} {'I_n':>22} {'Order':>12}")

    for n in ns:
        I = integrate(f, weight_fn(n))
        p = convergence_order(f, weight_fn, n)
        print(f"{n:10d} {I:22.15f} {p:12.6f}")


def experiment_2d(ns):
    exact1 = (np.exp(3) - 1) * (np.e - 1)

    J, _ = romberg(lambda t: np.sin(10*t*t), eps = 1e-14)
    exact2 = 4 + np.cos(10) + 20 * J

    print(f"\nReference: I1 = {exact1:.15f}")
    print(f"Reference: I2 = {exact2:.15f}")
    print(f"{'n':>6} {'I1':>20} {'Error1':>14} "
          f"{'I2':>20} {'Error2':>14}")

    for n in ns:
        w = simpson_weights(n)
        I1 = integrate_2d(h, w, w, 0, 3, 0, 1)
        I2 = integrate_2d(g, w, w, 0, 1, 0, 10)

        print(f"{n:6d} {I1:20.12f} {abs(I1-exact1):14.6e} "
              f"{I2:20.12f} {abs(I2-exact2):14.6e}")




if __name__ == "__main__":
    # Problems 1-3: include coarse grids and the round-off dominated regime.
    ns = [2**k for k in range(1, 17)]
    print("Order = nan means the differences are too small to estimate the order reliably.")

    experiment(1, trapezoid, ns)
    experiment(1, simpson_weights, ns)

    # Problem 4: resolve the increasingly rapid oscillations in both methods.
    ns_oscillatory = [2**k for k in range(1, 19)]
    for x in [100, 1000, 10000]:
        experiment(x, trapezoid, ns_oscillatory)
        experiment(x, simpson_weights, ns_oscillatory)

    # Problem 5.
    for x in [1, 100]:
        f = lambda t: g(t, x)
        I, n = romberg(f, eps = 1e-12)
        print(f"x = {x}, I = {I:.15f}, n = {n}")

    # Problem 6: a separate range keeps the two-dimensional grids manageable.
    ns_2d = [2**k for k in range(2, 12)]
    experiment_2d(ns_2d)
