Mode MD
ForceField Reaxff
XYZFile input.rd

TimeStep 2.0000
TotalStep 500000
ObserveStep 1
FileStep 1000
BondStep 1000

MPIGridX 4
MPIGridY 4
MPIGridZ 3

CUTOFF 15.0
MARGIN 1.0
InitTemp 2800.0
SeedTemp 0

#ReadVelocity  0
Thermo  NoseHoover
#Thermo Berendsen
AimTemp 2800.0
ThermoFreq  200

Baro NoseHoover
PressFlag 1  1  1
AimPress 1.0 1.0 1.0
BaroFreq 2000  2000  2000

SaveRestartStep 1000

GhostFactor 10.0
