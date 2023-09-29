# crustcrawler
Prosjekt i TEK4030
Simulering av crustcrawler med PD-kontroller med 'gravity compensation'
Setup simulering: 
https://github.uio.no/INF3480/crustcrawler_simulation/wiki/Setup
## Testing 
For å kjøre selve crustcrawler-simuleringen (uten PD-kontrolleren):
```bash
roslaunch crustcrawler_gazebo controller.launch
```

Kjøre PD-kontrolleren (mens simuleringen kjører):
```bash
rosrun joint_space_controller pd_controller
```

Kjøre konfigureringen:
```bash
rosrun rqt_reconfigure rqt_reconfigure
```

Her kan man endre K_d, K_p og q_d

## Functionality
```bash
$ ~/workspace chmod a+x src/joint_space_controller/cfg/PdControl.cfg
```

```bash
$ ~/workspace catkin_make
```

```bash
source devel/setup.bash
```

```bash
$ ~/workspace roslaunch joint_space_controller pd_controller
```

Opens rtq_reconfiguration for dynamic reconfiguration of the K_p, K_d and q_d 

## Dependencies
Github repos containing the crustcrawler:
https://github.uio.no/INF3480/crustcrawler_simulation.git
https://github.uio.no/TEK4030/crustcrawler_lib