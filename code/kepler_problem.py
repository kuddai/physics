GlowScript 2.1 VPython
# Using a graph-plotting module

EPS = 0.001
energy = -0.25
scene.height = 20  
scene.background = vector(0.95, 0.95, 0.95)

class EventBus:
  def __init__(self):
      self.events = dict(color=5)
  def on(self, event_name, handler):
    events = self.events
    if not events[event_name]:
      events[event_name] = []
    events[event_name].append(handler)
  
  def get_trigger(self, event_name):
    events = self.events
    def on_call(value):
      if not events[event_name]:
        events[event_name] = []
      for handler in events[event_name]:
        handler(value)
    return on_call
    
eventBus = EventBus()
eventBus.on('slider_changed', on_slider_changed)

def on_slider_changed(slider_data):
  global energy
  value = float(slider_data.value)
  energy = value
  trigger = eventBus.get_trigger('energy_changed')
  trigger(energy)

def calc_effective_potential(r):
  # normalised so
  # alpha = 1, M**2/m = 1
  r = float(r)
  return -1/r + 1/(2 * r**2)
  
def calc_conic_section_dist(phi, e):
  r = 1/(1.0 + e * cos(phi))
  if r < 0:
    raise ArithmeticError('negative')
  return r
  
def calc_eccentricity(energy):
  return (1 + 2*energy)**0.5

def potential_plot():
  xmin, xmax =  0.0, 3.0
  ymin, ymax = -1.0, 1.0
  potential_plot = gdisplay( xtitle='r', 
                             ytitle='Potential', 
                             width=400, 
                             height=300,
                             xmin=xmin,
                             xmax=xmax,
                             ymin=ymin,
                             ymax=ymax)
  effective_potential_plot = gcurve(color=color.cyan,
                                    label='U_eff')
  middle_line = gcurve(color=color.black, 
                       data=[[0, 0], [xmax, 0]])
  energy_plot = gcurve(color=color.orange, 
                       data=[[0, energy], [xmax, energy]],
                       label='energy')

  def draw_effective_potential():
    num_ticks = 100.0
    step = (xmax - xmin) / num_ticks
    for r in arange(xmin, xmax, step):
      effective_potential_plot.plot( pos=(r, calc_effective_potential(r)) )

  def draw_energy(energy):
    energy_plot.data = [[0, energy], [xmax, energy]]
  
  eventBus.on('energy_changed', draw_energy)
  draw_effective_potential()
  # here border cases from analysis of effective_potential
  slider( min=-0.5 + EPS, # to avoid sqrt(negative number)
          max=0.5, 
          value=energy, 
          length=400, 
          bind=eventBus.get_trigger('slider_changed'))

def trajectory_plot():
  # simulation meta variables
  FPS = 40.0
  out_point = (5000, 5000)
  d_t = 1/FPS
  phi_speed = pi * 0.5
  d_phi = phi_speed * d_t
  steps = int(2 * pi / d_phi)
  trajectory = [out_point]
  
  xmin, xmax = -5.0, 5.0
  ymin, ymax = -5.0, 5.0  
  
  potential_plot = gdisplay(width=400, 
                            height=400,
                            xmin=xmin,
                            xmax=xmax,
                            ymin=ymin,
                            ymax=ymax)  
                            
  particle = gdots(color=color.red, size=10)
  trajectory_plot = gdots(color=color.red, size=1)
  
  #print(dir(redraw_trajectory))
  def calc_trajectory(energy):
    data = []
    e = calc_eccentricity(energy)
    for i in range(steps + 1):
      phi = 2.0*pi*i/steps
      r = 2 #calc_conic_section_dist(phi, e)
      x = r*cos(phi)
      y = r*sin(phi)      
      data.append((x, y))
    return data
    
  def on_energy_changed(energy):
    global trajectory
    trajectory = calc_trajectory(energy)
    trajectory_plot.data = trajectory[::4]
    
  #eventBus.on('energy_changed', on_energy_changed)    
  #on_energy_changed(energy)
  
  # initial values
  curr_step = 0
  particle.data = [out_point]
  
  def run():
    global curr_step
    # loop it. See:
    # http://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Bounce-Callbacks-VPython/edit
    rate(int(FPS), run)
    # e = calc_eccentricity(energy)
    
    curr_step = (curr_step + 1) % len(trajectory)
    curr_point = trajectory[curr_step]
    particle.data = [curr_point]    
    
  run()

trajectory_plot()
potential_plot()

