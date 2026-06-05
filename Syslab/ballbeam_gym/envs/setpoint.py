import numpy as np
from math import exp
from gym.spaces import Box
from ballbeam_gym.envs.base import BallBeamBaseEnv

class BallBeamEnv(BallBeamBaseEnv):
    """
    Parameters
    ----------
    time_step : time of one simulation step, float (s)
    max_timesteps : maximum length of an episode, int
    beam_length : length of beam, float (cm)
    ball_radius : radius of ball (cm)
    unit_conversion : convert radius of ball from cm to m (0.01 cm/m)
    max_angle : max of abs(angle), float (rad) 
    max_angle_change : max change in angle per timestep, float
    init_velocity : initial velocity of ball, float (m/s)
    setpoint : fraction of beam at which to balance ball, float, range: -0.5, 0.5
    reward_scale : list of weights for position and velocity rewards, length: 2
    random_set : random setpoint, boolean
    action_mode : action space, str ['continuous', 'discrete']
    """

    def __init__(self, timestep=0.05, max_timesteps=100, unit_conversion=0.01, beam_length=50, ball_radius=2, max_angle=0.2, max_angle_change=0.01, init_velocity=0, setpoint=0, random_set=True, random_init_vel=True, sleep=1, action_mode='discrete'):
        kwargs = {'timestep': timestep,
                  'max_timesteps': max_timesteps,
                  'beam_length': beam_length,
                  'ball_radius': ball_radius,
                  'unit_conversion': unit_conversion,
                  'max_angle': max_angle,
                  'max_angle_change': max_angle_change,
                  'init_velocity': init_velocity,
                  'setpoint': setpoint,
                  'random_set': random_set,
                  'random_init_vel': random_init_vel,
                  'sleep': sleep,
                  'action_mode': action_mode,
                  }
        super().__init__(**kwargs)
        self.observation_space = Box(low=-self.max_state, high=self.max_state)

    def reward(self):
        K_pos, K_vel, _ = self.reward_scale
        x, v, _ = self.state
        max_x, max_v, _ = self.max_state
        
        # arbitrary domain for exponential function: D = [0, domain_scale]; increase it for higher penalty to larger distances from setpoint
        # horizontal shift and domain scale for reasonable bounds of e^-x on [0, x_scale]

        reward, x_shift, x_scale = 0, 3, 1

        r = (x - self.goal)**2/max_x**2
        normal_exp = exp(-(r*x_scale - x_shift))/exp(x_shift) 
        reward += (K_pos*(1 - r*normal_exp))

        v = v**2/max_v**2
        reward += (K_vel*(1 - v*normal_exp))

        reward /= sum(self.reward_scale)
        return reward
        
    def step(self, action):
        """
        Update environment for one action

        Parameters
        ----------
        action [continuous] : set angle, float (rad)
        action [discrete] : decrease/keep/increase angle, int [0, 1, 2]

        Returns state, reward value, termination state, False?, info
         * False is necessary to match with Gymnasium convention but really serves no purpose
        """
        super().step()
        self.bb.update(self._action_conversion(action))
        state = np.array([self.bb.x, self.bb.v, self.bb.theta])
        reward = self.reward()
        return state, reward, self.done, False, {}
        
    def reset(self):
        """ 
        Reset environment

        Returns
        -------
        observation : simulation state, np.ndarray (state variables)
        """
        
        return super().reset()

