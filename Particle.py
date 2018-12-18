import physical_constants
from ef.util.serializable_h5 import SerializableH5


class Particle(SerializableH5):
    def __init__(self, particle_id, charge, mass, position, momentum, momentum_is_half_time_step_shifted=False):
        self.particle_id = particle_id
        self.charge = charge
        self.mass = mass
        self.position = position
        self.momentum = momentum
        self.momentum_is_half_time_step_shifted = momentum_is_half_time_step_shifted

    def update_position(self, dt):
        pos_shift = self.momentum.times_scalar(dt / self.mass)
        self.position = self.position.add(pos_shift)

    def field_at_point(self, point):
        dist = point.sub(self.position)
        dist_len = dist.length()
        if dist_len == 0:
            return None
        dist_len_cube = dist_len ** 3
        return dist.times_scalar(self.charge / dist_len_cube)

    def boris_update_momentum(self, dt, total_el_field, total_mgn_field):
        q_quote = dt * self.charge / self.mass / 2.0
        half_el_force = total_el_field.times_scalar(q_quote)
        v_current = self.momentum.times_scalar(1.0 / self.mass)
        u = v_current.add(half_el_force)
        h = total_mgn_field.times_scalar(
            q_quote / physical_constants.speed_of_light)
        s = h.times_scalar(
            2.0 / (1.0 + h.dot_product(h)))
        tmp = u.add(u.cross_product(h))
        u_quote = u.add(tmp.cross_product(s))
        self.momentum = u_quote.add(half_el_force).times_scalar(self.mass)

    def boris_update_momentum_no_mgn(self, dt, total_el_field):
        dp = total_el_field.times_scalar(self.charge * dt)
        self.momentum = self.momentum.add(dp)
