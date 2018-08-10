import numpy as np
import sys
from CoolProp.CoolProp import PropsSI
from math import exp
from scipy.optimize import minimize

# damn those pesky global constants
gravity = 9.81
rho_hdpe = 0.955

# convergence tolerance
tol = 0.001


class SWHE():

    def __init__(self, d_i, d_o, d_coil, dx, dy, pipe_material, fluid, concentration=0.0, foul_in=False,
                 foul_out=False):

        self.d_i = d_i
        self.d_o = d_o
        self.d_coil = d_coil
        self.dx = dx
        self.dy = dy
        self.pipe_material = pipe_material
        self.fluid = fluid
        self.concentration = concentration / 100.0
        self.foul_in = foul_in
        self.foul_out = foul_out
        self.out_dict = {}

    def surf_water_props(self, temp):
        d = {'Dens': PropsSI('D', 'T', temp + 273.15, 'P', 101325, 'Water'),
             'Cond': PropsSI('L', 'T', temp + 273.15, 'P', 101325, 'Water'),
             'Visc': PropsSI('VISCOSITY', 'T', temp + 273.15, 'P', 101325, 'Water'),
             'SpHt': PropsSI('C', 'T', temp + 273.15, 'P', 101325, 'Water'),
             'Beta': PropsSI('ISOBARIC_EXPANSION_COEFFICIENT', 'T', temp + 273.15, 'P', 101325, 'Water')}

        d['KVisc'] = d['Visc'] / d['Dens']
        d['Diff'] = d['Cond'] / (d['Dens'] * d['SpHt'])

        return d

    def circ_fluid_props(self, temp):
        if self.fluid == 'Water':
            fluid = 'Water'
        elif self.fluid == 'PG':
            fluid = 'INCOMP::%s[%0.3f]' % ('MPG', self.concentration)
        else:
            sys.exit(1)

        d = {'Dens': PropsSI('D', 'T', temp + 273.15, 'P', 101325, fluid),
             'Cond': PropsSI('L', 'T', temp + 273.15, 'P', 101325, fluid),
             'Visc': PropsSI('VISCOSITY', 'T', temp + 273.15, 'P', 101325, fluid),
             'SpHt': PropsSI('C', 'T', temp + 273.15, 'P', 101325, fluid),
             'Pr': PropsSI('PRANDTL', 'T', temp + 273.15, 'P', 101325, fluid)}

        d['KVisc'] = d['Visc'] / d['Dens']

        return d

    def calc_hx(self, t_i, t_sw, v_dot, l):

        # store data for reporting
        self.out_dict = {
            'Temp, inlet': t_i,
            'Temp, surf water': t_sw,
            'Vol Flow Rate': v_dot,
            'Length': l}

        # initialize temperatures
        t_o = np.mean([t_i, t_sw])
        t_mft = np.mean([t_i, t_sw])
        t_so = np.mean([t_i, t_sw])
        t_si = np.mean([t_i, t_sw])
        t_o_old = 0

        # initialize geometries
        area_cr = np.pi * self.d_i ** 2 / 4.0
        area_so = np.pi * self.d_i * l
        area_si = np.pi * self.d_o * l

        self.out_dict['Area, Cross'] = area_cr
        self.out_dict['Area, Surf, in'] = area_si
        self.out_dict['Area, Surf, out'] = area_so

        # other initializations
        q_coil = 1000

        # set coefficients for convection correlation
        if t_i > t_sw:
            a = 5.0
            b = 0.0317
            c = 0.333
            d = 0.344
            e = 0.301
        else:
            a = 5.75
            b = 0.00971
            c = 0.333
            d = 0.929
            e = 0.0

        while abs(t_o - t_o_old) > tol:

            t_o_old = t_o

            # circulation fluid props
            f_props = self.circ_fluid_props(t_mft)
            rho_f = f_props['Dens']
            k_f = f_props['Cond']
            nu_f = f_props['KVisc']
            cp_f = f_props['SpHt']
            pr_f = f_props['Pr']

            self.out_dict['Fluid Props'] = f_props

            # surface water props
            w_props = self.surf_water_props(np.mean([t_so, t_sw]))
            k_w = w_props['Cond']
            nu_w = w_props['KVisc']
            beta_w = w_props['Beta']
            alpha_w = w_props['Diff']

            self.out_dict['Water Props'] = w_props

            # internal fouling
            if self.foul_in:
                r_foul_i = 0.000175 / area_si
            else:
                r_foul_i = 0

            self.out_dict['Resist, int foul'] = r_foul_i

            # external fouling
            if self.foul_out:
                r_foul_o = 0.00053 / area_so
            else:
                r_foul_o = 0

            self.out_dict['Resist, ext foul'] = r_foul_o

            # pipe resistance
            t_pipe = np.mean([t_si, t_so])
            self.out_dict['Temp, Pipe'] = t_pipe

            if self.pipe_material == 'STD':
                k_pipe = 0.17 + 5 * (rho_hdpe - 0.9) - 0.001 * t_pipe
            elif self.pipe_material == 'TE':
                k_pipe = 0.7
            elif self.pipe_material == 'Cu':
                k_pipe = 400
            elif self.pipe_material == 'PEX':
                k_pipe = 0.4125

            self.out_dict['Pipe Cond'] = k_pipe

            r_pipe = np.log(self.d_o / self.d_i) / (2 * np.pi * k_pipe * l)

            self.out_dict['Resist, pipe'] = r_pipe

            # outside resistance
            q_flux = q_coil / area_so
            self.out_dict['Q, flux'] = q_flux

            ra_d_mod = gravity * abs(beta_w * q_flux) * self.d_o ** 4 / (k_w * nu_w * alpha_w)
            self.out_dict['Rayleigh'] = ra_d_mod

            nusselt_o = a + b * ra_d_mod ** c * (self.dy / self.d_o) ** d * (self.dx / self.d_o) ** e
            self.out_dict['Nusselt, out'] = nusselt_o

            h_o = nusselt_o * k_w / self.d_o
            self.out_dict['Conv Coeff, out'] = h_o

            r_o = 1 / (h_o * area_so)
            self.out_dict['Resist, out'] = r_o

            # inside resistance
            vel = v_dot / area_cr
            self.out_dict['Fluid Vel'] = vel

            re = vel * self.d_i / nu_f
            self.out_dict['Reynolds'] = re

            nusselt_i = 0.023 * re ** 0.85 * pr_f ** 0.4 * (self.d_i / self.d_coil) ** 0.1
            self.out_dict['Nusselt, in'] = nusselt_i

            h_i = nusselt_i * k_f / self.d_i
            self.out_dict['Conv Coeff, in'] = h_i

            r_i = 1 / (h_i * area_si)
            self.out_dict['Resist, in'] = r_i

            # total thermal resistance
            r_tot = r_i + r_o + r_pipe + r_foul_i + r_foul_o
            self.out_dict['Resist, tot'] = r_tot

            # overall heat transfer coefficient
            ua = 1 / r_tot
            self.out_dict['UA'] = ua

            # effectivness-NTU method
            m_dot = v_dot * rho_f
            self.out_dict['Mass flow rate'] = m_dot

            ntu = ua / (m_dot * cp_f)
            self.out_dict['NTU'] = ntu

            eff = 1 - exp(-ntu)
            self.out_dict['Effectiveness'] = eff

            q_max = m_dot * cp_f * (t_i - t_sw)
            self.out_dict['Q, max'] = q_max

            q_coil = eff * q_max
            self.out_dict['Q, coil'] = q_coil

            # calculate temperatures
            t_mft = t_sw + m_dot * cp_f * t_i * (1 - exp(-ntu)) / ua + m_dot * cp_f * t_sw * (-1 + exp(-ntu)) / ua
            self.out_dict['Temp, mft'] = t_mft

            t_si = t_mft - q_coil * (r_i + r_foul_i)
            self.out_dict['Temp, surf, in'] = t_si

            t_so = t_si - q_coil * (r_pipe + r_foul_o)
            self.out_dict['Temp, surf, out'] = t_so

            t_o = t_i - q_coil / (m_dot * cp_f)
            self.out_dict['Temp, exit'] = t_o

            t_appr = t_o - t_sw
            self.out_dict['Temp, appr'] = t_appr

        return self.out_dict

    def find_t_in(self, t_i, t_sw, v_dot, l, t_appr_req):
        return abs(t_appr_req - self.calc_hx(t_i=t_i[0], t_sw=t_sw, v_dot=v_dot, l=l)['Temp, appr'])

    def find_l(self, l, t_i, t_sw, v_dot, q_req):
        return abs(q_req - self.calc_hx(l=l[0], t_i=t_i, t_sw=t_sw, v_dot=v_dot)['Q, coil'])

    def size_hx(self, t_sw, v_dot, q_req, t_appr_req):

        q_coil = 0
        t_appr = 0

        while abs(q_coil - q_req) > tol and abs(t_appr - t_appr_req) > tol:
            # set inlet temp to hit approach temperature
            minimize(self.find_t_in, x0=np.array([30]), args=(t_sw, v_dot, 15, 5))
            # set length to hit load


if __name__ == '__main__':
    H = SWHE(d_i=0.025273,
             d_o=0.028575,
             d_coil=1.8288,
             dx=0.066675,
             dy=0.066675,
             pipe_material='STD',
             fluid='PG',
             concentration=12.5,
             foul_in=False,
             foul_out=False)

    print(H.calc_hx(31.08119, 23.8888889, 0.0001893, 127.30385)['Temp, appr'])
    minimize(H.find_t_in, x0=np.array([30]), args=(20, 0.0001893, 15, 5))
    print(H.out_dict['Temp, inlet'])
    minimize(H.find_l, x0=np.array([40]), args=(30, 20, 0.001893, 3500))
    print(H.out_dict['Length'])
