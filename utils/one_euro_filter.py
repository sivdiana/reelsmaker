import math

class OneEuroFilter:
    """
    One Euro Filter — фильтр для сглаживания с адаптивной частотой среза.
    Используется для плавного отслеживания координат.

    См. https://cristal.univ-lille.fr/~casiez/1euro/
    """

    def __init__(self, freq, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.freq = freq
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = 0
        self.t_prev = None

    def alpha(self, cutoff):
        te = 1.0 / self.freq
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def filter(self, x, t):
        if self.x_prev is None:
            self.x_prev = x
            self.t_prev = t
            return x

        dt = t - self.t_prev
        if dt <= 0:
            return x

        dx = (x - self.x_prev) * self.freq
        alpha_d = self.alpha(self.d_cutoff)
        dx_hat = alpha_d * dx + (1 - alpha_d) * self.dx_prev

        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        alpha = self.alpha(cutoff)
        x_hat = alpha * x + (1 - alpha) * self.x_prev

        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat
