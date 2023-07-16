import os.path
import random
from tkinter import *
from agents import *
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Gui(VacuumEnvironment):
    """This is a two-dimensional GUI environment. Each location may be
    dirty, clean or can have a wall. The user can change these at each step.
    """
    xi, yi = (0, 0)
    xi2, yi2 = (0, 0)
    count = 0
    perceptible_distance = 1
    drt_count=0

    def __init__(self, root, width=7, height=7, elements=None):
        print("creating xv with width ={} and height={}".format( width, height))
        super().__init__(height,width)
        if elements is None:
            elements = ['D', 'W'] # D is Dirt and W is Wall
        self.root = root
        self.create_frames(height)
        self.create_buttons(width)
        self.create_walls()
        self.elements = elements
        self.agents = []


    def add_agent(self, agt, xyloc):
        """add an agent to the GUI"""
        self.add_thing(agt, xyloc)
        self.buttons[xyloc[0]][xyloc[1]].config(
            bg='green', text='A', state='disabled', disabledforeground='black')

    def add_agent2(self, agt, xyloc):
        """add an agent to the GUI"""
        #self.agents.append(agt)
        self.add_thing(agt, xyloc)
        self.buttons[xyloc[0]][xyloc[1]].config(
            bg='green', text='A', state='disabled', disabledforeground='black')

    def create_frames(self,h):
        """Adds frames to the GUI environment."""
        self.frames = []
        for _ in range(h):
            frame = Frame(self.root, bg='red')
            frame.pack(side='bottom')
            self.frames.append(frame)

    def create_buttons(self,w):
        """Adds buttons to the respective frames in the GUI."""
        self.buttons = []
        for frame in self.frames:
            button_row = []
            for _ in range(w):
                button = Button(frame, height=3, width=5, padx=2, pady=2)
                button.config(command=lambda btn=button: self.display_element(btn))
                button.pack(side='left')
                button_row.append(button)
            self.buttons.append(button_row)

    def create_walls(self):
        """Creates the outer boundary walls which do not move."""
        for row, button_row in enumerate(self.buttons):
            if row == 0 or row == len(self.buttons) - 1 or row==int((len(self.buttons)/2)):
                for button in button_row:
                    button.config(bg = 'red', text='W', state='disabled', disabledforeground='black')
            else:
                button_row[0].config(bg = 'red',text='W', state='disabled', disabledforeground='black')
                button_row[len(button_row) - 1].config(bg = 'red',text='W',
                                                       state='disabled', disabledforeground='black')

    def display_element(self, button):
        """Show the things on the GUI."""
        txt = button['text']
        if txt != 'A':
            if txt == 'W':
                button.config(bg='grey', text='D')
            elif txt == 'D':
                button.config(bg='white', text='')
            elif txt == '':
                button.config(bg = 'red', text='W')
        if txt != 'A2':
            if txt == 'W':
                button.config(bg='grey', text='D')
            elif txt == 'D':
                button.config(bg='white', text='')
            elif txt == '':
                button.config(bg = 'red', text='W')

    def read_env(self):
        """Reads the current state of the GUI environment."""

        for i, btn_row in enumerate(self.buttons):
            for j, btn in enumerate(btn_row):
                if (i != 0 and i != len(self.buttons) - 1) and (j != 0 and j != len(btn_row) - 1):
                    agt_loc = self.agents[0].location
                    agt_loc2=self.agents[1].location
                    if self.some_things_at((i, j)) and (i, j) not in (agt_loc,agt_loc2):
                        for thing in self.list_things_at((i, j)):
                            self.delete_thing(thing)
                    if btn['text'] == self.elements[0]:
                        self.add_thing(Dirt(), (i, j))
                        self.drt_count=self.drt_count+1
                    elif btn['text'] == self.elements[1]:
                        self.add_thing(Wall(), (i, j))
                    elif btn['text'] == 'A':
                        self.add_thing(Wall(), (i, j))


    def run2(self):
        print("The current dirt count is",self.drt_count)
        self.read_env()
        super().run(self.drt_count)



    def execute_action(self, agent, action):
        """Determines the action the agent performs."""

        xi, yi = (self.xi, self.yi)
        agt1=self.agents[0]
        agt2=self.agents[1]


        print('The agent1 is at location',agt1.location,'and action',action)
        print('The agent2 is at location', agt2.location,'and action',action)

        #print("agent at location (", xi2, yi2, ") and action ", action)
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list:
                dirt = dirt_list[0]
                agent.performance += 100
                self.delete_thing(dirt)
                self.buttons[xi][yi].config(text='', state='normal')
                xf, yf = agent.location
                self.buttons[xf][yf].config(
                text='A', state='disabled', disabledforeground='black')



        else:
            agent.bump = False
            if action == 'TurnRight':
                agent.direction += Direction.R
                agent.count = agent.count + 1
            elif action == 'DoubleRight':
                agent.direction += Direction.R
                agent.direction += Direction.R
                agent.count = agent.count + 1
            elif action == 'DoubleLeft':
                agent.direction += Direction.L
                agent.direction += Direction.L
                agent.count = agent.count + 1
            elif action == 'TurnLeft':
                agent.direction += Direction.L
                agent.count = agent.count+1
            elif action == 'Forward':
                oldlocation = agent.location
                xi, yi = oldlocation
                agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
                agent.count=0
                if not agent.bump:
                        self.buttons[xi][yi].config(bg='white', text='', state='normal') #creates a white spot at old location
                        xf, yf = agent.location
                        self.buttons[xf][yf].config(
                            bg = 'green', text='A', state='disabled', disabledforeground='black') # Loads up 'A' in the new location

            if action != 'NoOp':
                agent.performance -= 1
            performance_button.config(text=str(agt1.performance))
            performance_button2.config(text=str(agt2.performance))
            performance_button3.config(text=str(agt1.performance+agt2.performance))




    def update_env(self):
        """Updates the GUI environment according to the current state."""
        self.read_env()
        agt = self.agents[0]
        #agt2 = self.agents[1]
        previous_agent_location = agt.location
        #previous_agent_location2 = agt2.location
        self.xi, self.yi = previous_agent_location
        #self.xi2, self.yi2 = previous_agent_location2
        self.step()
        xf, yf = agt.location
        #xf2, yf2 = agt2.location


    def reset_env(self):
        """Resets the GUI environment to the initial state."""
        #self.read_env()
        for i, btn_row in enumerate(self.buttons):
            for j, btn in enumerate(btn_row):
                if (i != 0 and i != len(self.buttons) - 1) and (j != 0 and j != len(btn_row) - 1):
                    if self.some_things_at((i, j)):
                        for thing in self.list_things_at((i, j)):
                            self.delete_thing(thing)
                            btn.config(bg='white', text='', state='normal')
        self.create_walls()


        ag1= RuleBasedAgent(program=XYRuleBasedAgentProgram)
        ag2= RuleBasedAgent(program=XYRuleBasedAgentProgram)



        ag1.performance=0
        ag2.performance=0
        performance_button.config(text='Ag1_Performance')
        performance_button2.config(text='Ag1_Performance')
        performance_button3.config(text='Total_Performance')



        self.add_thing(ag1, loc1)
        self.buttons[loc1[0]][loc1[1]].config(
            bg='green', text='A', state='disabled', disabledforeground='black')
        self.add_thing(ag2, loc2)
        self.buttons[loc2[0]][loc2[1]].config(
            bg='green', text='A', state='disabled', disabledforeground='black')

#implement this. Rule is as follows: At each location, agent checks all the neighboring location: If a "Dirty"
# location found, agent goes to that location, otherwise follow similar rules as the XYReflexAgentProgram bellow.


def XYRuleBasedAgentProgram(percept):
    status, bump, location1,direction,count= percept

    if (count==1):
        print("bottom Forward executed")
        return 'Forward'

    agt_direction = direction


    current_location = location1
    neighbors = [(current_location[0] - 1, current_location[1]),  # up 0
                 (current_location[0] + 1, current_location[1]),  # down 1
                 (current_location[0], current_location[1] - 1),  # Left 2
                 (current_location[0], current_location[1] + 1)]  # Right 3

    if status == 'Dirty':
        return 'Suck'

    #AgentFacingLeft
    if agt_direction.direction == Direction.U: #Up is left facing direction
        if env.some_things_at(neighbors[0], Dirt):  # left (x,y-1)  ##executed if Dirt is placed below Agent
            return 'TurnLeft'
        if env.some_things_at(neighbors[1], Dirt):  ##executed if Dirt is placed above Agent
            return 'TurnRight'
        if env.some_things_at(neighbors[2], Dirt):  # up (x-1,y)  ## executed if Dirt is placed at left of Agent
            return 'Forward'
        if env.some_things_at(neighbors[3], Dirt):
            #count=count+1
            return 'DoubleRight'
        else:
            if status == 'Dirty':
                return 'Suck'

            if bump == 'Bump':
                value = random.choice((1, 2))
            else:
                value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

            if value == 1:
                return 'TurnRight'
            elif value == 2:
                return 'TurnLeft'
            else:
                return 'Forward'

    #AgentFacingUp
    if agt_direction.direction == Direction.R:  #Right is when agent facing upwards direction
        if env.some_things_at(neighbors[2], Dirt):
            return 'TurnLeft'
        if env.some_things_at(neighbors[3], Dirt):
            return 'TurnRight'
        if env.some_things_at(neighbors[0], Dirt):
            return 'DoubleLeft'
        if env.some_things_at(neighbors[1], Dirt):
            #count = count + 1
            return 'Forward'
        else:
            if status == 'Dirty':
                return 'Suck'

            if bump == 'Bump':
                value = random.choice((1, 2))
            else:
                value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

            if value == 1:
                return 'TurnRight'
            elif value == 2:
                return 'TurnLeft'
            else:
                return 'Forward'

 #AgentFacingRight
    if agt_direction.direction == Direction.D:  #Down is when agent is facing Right
        if env.some_things_at(neighbors[1], Dirt):  # left (x,y-1)  ##executed if Dirt is placed below Agent
            return 'TurnLeft'
        if env.some_things_at(neighbors[0], Dirt):  # left (x,y-1)  ##executed if Dirt is placed below Agent
            return 'TurnRight'
        if env.some_things_at(neighbors[3], Dirt):  # left (x,y-1)  ##executed if Dirt is placed below Agent
            return 'Forward'
        if env.some_things_at(neighbors[2], Dirt):  # left (x,y-1)  ##executed if Dirt is placed below Agent
            return 'DoubleLeft'
        else:
            if status == 'Dirty':
                return 'Suck'

            if bump == 'Bump':
                value = random.choice((1, 2))
            else:
                value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

            if value == 1:
                return 'TurnRight'
            elif value == 2:
                return 'TurnLeft'
            else:
                return 'Forward'

 #AgentFacingDown
    if agt_direction.direction == Direction.L: #Left is when agent is facing Down
        if env.some_things_at(neighbors[2], Dirt):
            return 'TurnRight'
        if env.some_things_at(neighbors[3], Dirt):
            return 'TurnLeft'
        if env.some_things_at(neighbors[0], Dirt):
            return 'Forward'
        if env.some_things_at(neighbors[1], Dirt):
            return 'DoubleRight'
        else:
            if status == 'Dirty':
                return 'Suck'

            if bump == 'Bump':
                value = random.choice((1, 2))
            else:
                value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

            if value == 1:
                return 'TurnRight'
            elif value == 2:
                return 'TurnLeft'
            else:
                return 'Forward'

#Implement this: This will be similar to the ReflectAgent bellow.
class RuleBasedAgent(Agent):

    def __init__(self, program=None):
        super().__init__(program)
        self.location = (3, 3)
        self.direction = Direction("up")
        self.count=0
        self.drt_count = 0

        #trycount

def XYReflexAgentProgram(percept):
    """The modified SimpleReflexAgentProgram for the GUI environment."""
    status, bump, location1, direction,count = percept
    if status == 'Dirty':
        return 'Suck'

    if bump == 'Bump':
        value = random.choice((1, 2))
    else:
        value = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward

    if value == 1:
        return 'TurnRight'
    elif value == 2:
        return 'TurnLeft'
    else:
        return 'Forward'


class XYReflexAgent(Agent):
    """The modified SimpleReflexAgent for the GUI environment."""

    def __init__(self, program=None):
        super().__init__(program)
        self.location = (4,2)
        self.direction = Direction("up")
        self.count=0
        self.drt_count = 0



# TODO: Check the coordinate system.
# TODO: Give manual choice for agent's location.
if __name__ == "__main__":
    win = Tk()
    win.title("Vacuum Robot Environment")
    win.geometry("500x600")
    win.resizable(True, True)
    frame = Frame(win, bg='black')

    global dirt_count

    wid = 7
    if sys.argv[1]:
        wid = int(sys.argv[1])

    hig = 7
    if sys.argv[2]:
        hig = int(sys.argv[2])


    global performance_button
    global performance_button2
    performance_button = Button(frame, text='Agt1_Performance', height=2,
                         width=10, padx=2, pady=2)
    performance_button.pack(side='left')

    performance_button2 = Button(frame, text='Agt2_Performance', height=2,
                         width=10, padx=2, pady=2)

    performance_button2.pack(side='left')

    performance_button3 = Button(frame, text='Total_Performance', height=2,
                         width=10, padx=2, pady=2)

    performance_button3.pack(side='left')

    reset_button = Button(frame, text='Reset', height=2,
                          width=6, padx=2, pady=2)
    reset_button.pack(side='left')
    next_button = Button(frame, text='Next', height=2,
                         width=6, padx=2, pady=2)
    next_button.pack(side='left')
    frame.pack(side='bottom')

    mode_button_text = StringVar(value="Switch to RuleBased")
    mode_button = Button(frame, textvariable=mode_button_text, height=2,
                         width=16, padx=2, pady=2)
    mode_button.pack(side='left')
    run_button = Button(frame, text='Run', height=2, width=5, padx=2, pady=2)
    run_button.pack(side='left')


    global loc1
    global loc2
    loc1=(random.randint(int(wid/2)+1, wid-2), random.randint(2,hig-2))
    loc2=(random.randint(2,int(wid/2)-1),random.randint(2,hig-2))

    env = Gui(win, hig, wid)
    agt = XYReflexAgent(program=XYReflexAgentProgram)
    agt2 = XYReflexAgent(program=XYReflexAgentProgram)
    env.add_agent(agt,(loc1[0],loc1[1]))
    env.add_agent2(agt2,(loc2[0],loc2[1]))


    def switch_mode():
        global agt
        global agt2# Access vacAgent as a global variable

        if isinstance(agt, XYReflexAgent) and isinstance(agt2,XYReflexAgent):
            agt = RuleBasedAgent(program=XYRuleBasedAgentProgram)
            print("Ag1 is rule based now")
            agt2= RuleBasedAgent(program=XYRuleBasedAgentProgram)
            print("Ag2 is rule based now")
            mode_button_text.set("Switch to Reflex-Based")
        else:
            agt = XYReflexAgent(program=XYReflexAgentProgram)
            print("Ag1 changed to reflex based now")
            agt2=XYReflexAgent(program=XYReflexAgentProgram)
            print("Ag2 changed to reflex based now")
            mode_button_text.set("Switch to RuleBased")

        env.reset_env()
    run_button.config(command=env.run2)
    mode_button.config(command=switch_mode)
    next_button.config(command=env.update_env)
    reset_button.config(command=env.reset_env)
    win.mainloop()
