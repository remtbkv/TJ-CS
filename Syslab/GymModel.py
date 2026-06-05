import gym, time, os, warnings, importlib
from datetime import datetime
import ballbeam_gym
from PPO import PPO

warnings.simplefilter("ignore", UserWarning) # ignore precision loss Box float32

class GymModel:
    def __init__(self, env="BallBeam"):
        """
        env : BallBeam, CartPole
        """
        self.env_shortname = env
        change = {"BallBeam": [3, 3, "BallBeam-v0"], "CartPole": [2, 4, "CartPole-v1"]}
        self.action_dim, self.state_dim, self.env_name = change[env]

        self.has_continuous_action_space = False
        self.reward_scale = [1]*self.state_dim
        self.policy_dir = "trained/"+env+"/"
        self.rf_dir = "reward_functions/"
        self.kwargs = {}
        self.training_data = []
        self.stop_train_loop = False
        self.stop_test_loop = False
        self.stop_test_physical_loop = False
        self.is_training = False
        self.is_testing = False
        self.is_testing_physical = False
        self.use_new_rf = False
        self.use_init = False

        self.K_epochs = 80        # update policy for K epochs
        self.eps_clip = 0.2        # clip parameter for PPO
        self.gamma = 0.99              # discount factor
        self.lr_actor = 0.003        # learning rate for actor
        self.lr_critic = 0.01      # learning rate for critic
        self.action_std_TEST = 0.1
        self.max_ep_len_TEST = 10000
        self.action_std_TRAIN = 0.6
        self.max_ep_len_TRAIN = 10000
        self.action_std_decay_rate = 0.05
        self.min_action_std = 0.1
        self.action_std_decay_freq = int(2.5e5)
        self.max_epochs = 1000
        self.update_timestep = self.max_ep_len_TRAIN * 4
        self.max_training_timesteps = int(self.max_epochs*self.max_ep_len_TRAIN)
        self.print_freq = self.max_ep_len_TRAIN
        self.log_freq = self.max_ep_len_TRAIN * 2
        self.save_model_freq = int(1e5)
        self.char_width = 80
        self.block = '-'*self.char_width
        self.big_block = '='*self.char_width
        
    def set_args(self, args):
        """
        args:
            timestep: default 0.05 s
            max_timesteps: default 100
            beam_length: default 1.0 m
            ball_radius: default 0.05 m
            max_angle: default 0.2 rad
            max_ang_a: default 26.18 rad/s^2 (from 0.2 sec / 60 deg servo speed)
            init_velocity: default 0 m/s
            setpoint: fraction of beam length, default 0
            random_set: default True
            random_init_vel: default True
            
            reward_scale: default [1,1]
            
            Typically use:
                - setpoint
                - reward_scale: [0.6, 0.4] (pos, vel)
                - random_set: False
            - random_init_vel: False
        """
        for key in ["reward_scale", "use_new_rf", "char_width"]:
            if key in args:
                setattr(self, key, args[key])
                del args[key]
        self.block = '-'*self.char_width
        self.big_block = '='*self.char_width
        self.kwargs = args
        # TODO: if implementing continuous action space, add option here

    def get_training_data(self):
        return self.training_data

    def get_fn(self, train=True):
        # filename format: {env_name}_{reward_scale}_{version}_{epoch}_{reward}.pth
        #   - custom name doesn't have version number
        # returns start of filename (everything before _epoch_reward.pth); full filename; whether using existing file

        if train:
            create_new = len(input("Create new file (n) or load existing (enter)? "))
        reward_scale = ",".join(str(float(i)) for i in self.reward_scale)
        fn_inp = input("Enter filename (blank for default): ")
        fn = fn_inp if len(fn_inp) else "{}_{}".format(self.env_shortname, reward_scale)
        if train and create_new:
            if len(fn_inp): # check if custom filename already exists
                existing, files = False, []
                for i in os.listdir(self.policy_dir):
                    if i.startswith(fn):
                        existing = True
                        files.append((i, float(i.split("_")[-1][:-4])))
                if existing:
                    use_new = len(input("File already exists. Create new (n) or load existing (enter)? "))
                    if use_new:
                        return fn, fn+"_0_0.pth", False
                    files.sort(key=lambda x: x[1], reverse=True)
                    return fn, files[0][0], True
            else: # using default naming
                vers_inp = input("Enter number for version (blank for default): ")
                fn += "_{}".format(0 if not vers_inp else vers_inp)
            return fn, fn+"_0_0.pth", False # _epoch_reward.pth
        else: # load file
            existing, files = False, []
            for i in os.listdir(self.policy_dir):
                if i.startswith(fn):
                    existing = True
                    files.append((i, float(i.split("_")[-1][:-4])))
            if not existing:
                print("File does not exist!")
                return self.get_fn(train)
            files.sort(key=lambda x: x[1], reverse=True)
            return fn, files[0][0], True
    
    def stop_train(self):
        self.stop_train_loop = True

    def make_env(self):
        """
        Returns gym environment with specified parameters and reward function
        """
        env = gym.make(self.env_name, **self.kwargs)
        if not hasattr(env, "goal"):
            env.goal = 0
        env.reward_scale = self.reward_scale
        if self.use_new_rf:
            rf = importlib.import_module(f'{self.rf_dir[:-1]+"."+self.env_shortname}_rf').user_reward
            env.original_step = env.step
            def wrapped_step(action):
                state, _, done, *info = env.original_step(action)
                reward = rf(env)
                return state, reward, done, *info
            env.step = wrapped_step
        return env

    def train(self):
        self.is_training = True
        fn_start, filename, use_existing_ppo = self.get_fn()
        ppo_agent = PPO(self.state_dim, self.action_dim, self.lr_actor, self.lr_critic, self.gamma, self.K_epochs, self.eps_clip, self.has_continuous_action_space, self.action_std_TRAIN)
        if use_existing_ppo:
            ppo_agent.load(self.policy_dir+filename)
        print_running_reward = print_running_episodes = timestep = 0
        epoch = int(filename.split("_")[-2])
        avg_rewards = []
        env = self.make_env()
        
        print(self.big_block)
        print(f"{'Loaded weights from:':<30}{fn_start}")
        if not os.path.exists(self.policy_dir):
            os.makedirs(self.policy_dir)
        print(f"{'Saving weights file to:':<30}{fn_start}")
        print(f"{'Started training at (GMT):':<30}{(start_time := datetime.now().replace(microsecond=0))}")
        print(self.block)

        while timestep <= self.max_training_timesteps:
            state = env.reset()
            current_ep_reward = 0

            for states in range(1, self.max_ep_len_TRAIN+1):
                # select action with policy
                action = ppo_agent.select_action(state)
                state, reward, done, *_ = env.step(action)
                
                # saving reward and is_terminals
                ppo_agent.buffer.rewards.append(reward)
                ppo_agent.buffer.is_terminals.append(done)

                timestep += 1
                current_ep_reward += reward
                print_avg_reward = print_running_reward / print_running_episodes if print_running_episodes else 0

                # update PPO agent
                if timestep % self.update_timestep == 0:
                    if self.stop_train_loop:
                        break
                    ppo_agent.update()

                # decay action std of ouput action distribution
                if self.has_continuous_action_space and timestep % self.action_std_decay_freq == 0:
                    ppo_agent.decay_action_std(self.action_std_decay_rate, self.min_action_std)

                # save model weights
                if timestep % self.save_model_freq == 0:
                    print(self.block)
                    fn = self.policy_dir + fn_start + "_{}_{}.pth".format(epoch, round(print_avg_reward,3))
                    ppo_agent.save(fn)
                    print("Saved model at : " + fn)
                    print("Elapsed Time : ", datetime.now().replace(microsecond=0) - start_time)
                    print(self.block)

                # printing average reward till last episode
                if timestep % self.print_freq == 0:
                    avg_rewards.append(print_avg_reward)
                    self.training_data.append((epoch, print_running_reward / print_running_episodes))
                    print("Epoch : {}\t\tAverage Reward : {}".format(epoch, round(print_avg_reward, 2)))
                    print_running_reward, print_running_episodes = 0, 0
                    epoch += 1

                # stop if episode over
                if done:
                    break
            
            if self.stop_train_loop:
                print(f"{self.block}\nTraining stopped by user\n{self.block}")
                break
            print_running_reward += current_ep_reward
            print_running_episodes += 1

        env.close()
        self.training_data = []
        if not self.stop_train_loop:
            print(self.big_block, "\n")
        print("Started training at (GMT) : ", start_time)
        print("Finished training at (GMT) : ", end_time := datetime.now().replace(microsecond=0))
        print("Total training time  : ", end_time - start_time)
        print(self.big_block)
        self.is_training = False

    def stop_test(self):
        self.stop_test_loop = True

    def test(self, max_ep_len=1000, total_test_episodes=10):
        self.is_testing = True
        _, filename, use_existing_ppo = self.get_fn(train=False)
        ppo_agent = PPO(self.state_dim, self.action_dim, self.lr_actor, self.lr_critic, self.gamma, self.K_epochs, self.eps_clip, self.has_continuous_action_space, self.action_std_TEST)
        if use_existing_ppo:
            ppo_agent.load(self.policy_dir + filename)
        fd = input("Enter frame delay in seconds (enter for 0): ")
        frame_delay = float(fd) if fd else 0
        print(self.big_block)
        print(f"{'Loaded weights from:':<30}{filename}")
        print(self.block)
        test_running_reward =  0
        env = self.make_env()
        for ep in range(1, total_test_episodes+1):
            ep_reward = 0
            state = env.reset()
            for frameNum in range(1, max_ep_len+1):
                if self.stop_test_loop:
                    break
                if self.env_shortname == "BallBeam":
                    env.render(button_info=(ep, frameNum))
                else:
                    env.render()
                time.sleep(frame_delay)
                action = ppo_agent.select_action(state)
                state, reward, done, *_ = env.step(action)
                ep_reward += reward
                ppo_agent.buffer.clear()
                if done:
                    break
            print('Episode: {}\t\tAvg Reward: {}'.format(ep, round(avg_reward := ep_reward/frameNum, 3)))
            test_running_reward += avg_reward
            if self.stop_test_loop:
                print(f"{self.block}\nTesting stopped by user\n{self.block}")
                break
        env.close()
        if not self.stop_test_loop:
            print(self.big_block)
        print("Average test reward:", round(test_running_reward/ep, 2))
        print(self.big_block)
        self.is_testing = False

    def send_action(self, action):
        self.use_action = True
        self.send_action = action

    def get_state(self):
        """
        self.get_state : pos, vel, ang
        """
        self.use_state = False
        return self.get_state

    def reset_state(self):
        """
        Sets initial state parameters for BallBeam environment
        
        self.init_info : dict() { beam_length, ball_radius, setpoint }
        """
        self.use_init = False
        for param in ["beam_length", "ball_radius", "setpoint"]:
            setattr(self.kwargs, param, self.init_info[param])
        self.kwargs["random_set"] = False
        
    def set_state(self, env, state):
        """
        Overrides state for BallBeam object
        """
        env.x, env.v, env.theta = state

    def test_physical(self):
        """
        init_info : dict() { beam_length, ball_radius, setpoint }

        SETTER/GETTER:
            simulation:
                reset_state() : self.use_init
                send_action() : self.use_action
                get_state() : self.use_state
                stop the loop : stop_test_physical_loop
            other party:
                ?() : self.use_init
                ?() : self.use_action
                ?() : self.use_state
                ?() : stop_test_physical_loop

        BLOCKING FLOW:

        initialization: 
            simulation:
                if self.use_init, initialize (-> self.use_init = False)
            other party:
                if self.testing_done and not self.use_init, send initial state (-> self.use_init = True)
        testing:
            simulation:
                if self.use_state, use this (-> self.use_state = False) to send next action (-> self.use_action = True)
                else, wait for next state to be loaded
            other party:
                if self.use_action, use this (-> self.use_state = True) to send new state (self.use_action = False)
                else, wait for next action to be sent
        """
        self.is_testing_physical = True
        _, filename, use_existing_ppo = self.get_fn(train=False)
        ppo_agent = PPO(self.state_dim, self.action_dim, self.lr_actor, self.lr_critic, self.gamma, self.K_epochs, self.eps_clip, self.has_continuous_action_space, self.action_std_TEST)
        if use_existing_ppo:
            ppo_agent.load(self.policy_dir + filename)
        print(self.big_block)
        print(f"{'Loaded weights from:':<30}{filename}")
        print(self.block)
        
        while not self.stop_test_physical_loop:
            if self.use_init:
                self.reset_state()
                env = self.make_env()
                # one problem with starting ep_reward at 0 with a random state is that it could end up seeming low if the initial state is very bad and takes a little time to stabilize
                ep_reward, i, done = 0, 1, False
                env.reset()
                while not done:
                    if self.stop_test_physical_loop:
                        print(f"{self.block}\nTesting stopped by user\n{self.block}")
                        break
                    if self.use_state:
                        real_state = self.get_state()
                        action = ppo_agent.select_action(real_state)
                        self.send_action(action)
                        sim_state, reward, done, *_ = env.step(action)
                        # handle difference between sim/real state
                        env.set_state(real_state)
                        ep_reward += reward
                        ppo_agent.buffer.clear()
                        i += 1
                print(f'Avg Reward: {round(ep_reward/i, 3)}')
        self.is_testing_physical = False

    def stop_test_physical(self):
        self.stop_test_physical_loop = True

    def quit(self):
        os._exit(0)

    
if __name__ == "__main__":
    print("Ran the wrong file!")