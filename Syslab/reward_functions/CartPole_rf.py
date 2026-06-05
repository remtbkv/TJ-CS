def user_reward(self):
	pos, vel, ang, ang_v = self.state
	K_pos, K_vel, K_ang, K_ang_v = self.reward_scale
	upright = self.goal
	return -(ang-upright)**2
