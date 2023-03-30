import matplotlib.pyplot as plt

A=2*2.5 # [cm*cm] to-be-etched copper surface
d=0.1   # [mm] copper layer thickness
P_HCl=33  # [%] HCl mass percentage
ro_HCl=1.15  # [g/cm^3] táblázatból
ro_H2O2=1  # [g/cm^3] táblázatból

P_H2O2=12 # [%] H2O2 mass percentage

print("Cu + 2 HCl + H2O2 = CuCl2 + 2 H2O")

ro_Cu=8.960  # [g/cm^3]

M_Cu=63.54  # [g/mol]
M_H=1  # [g/mol]
M_HCl=35.45  # [g/mol]
M_O=16  # [g/mol]

m_Cu=A*d/1000*ro_Cu
n_Cu=m_Cu/M_Cu  # [mol]
print(f"Amount of copper:    {m_Cu*1000:.3} mg   =   {n_Cu:.3} mol")

n_HCl=n_Cu*2
n_H2O2=n_Cu

m_HCl=n_HCl*(M_H+M_HCl)
V_HCl=m_HCl/ro_HCl
print(f"Amount of HCl:    {m_HCl*1000:.3} mg   =   {V_HCl:.3} ml")

m_H2O2=n_H2O2*(2*M_H+2*M_O)
V_H2O2=m_H2O2/ro_H2O2
print(f"Amount of H2O2:    {m_H2O2*1000:.3} mg   =   {V_H2O2:.3} ml")
