import pandas as pd
import numpy as np

# Define the range for Pi (initial pressure) and Vi (initial volume)
P_i_values = np.linspace(101300, 101300 * 4, 200)  # 200 values for Pi
V_i_values = np.linspace(100, 1000, 200)  # 200 values for Vi

# compression factor fo air
Z = 0.9

# Calculate Pf, Vf, ΔP, ΔV, and C
P_f_values = 2 * P_i_values  # Pf = 2Pi
V_f_values = V_i_values / 2  # Vf = Vi / 2
ΔP_values = P_f_values - P_i_values  # ΔP = Pf - Pi
ΔV_values = V_f_values - V_i_values  # ΔV = Vf - Vi
C_values = (ΔV_values / ΔP_values)  # C = (ΔV / ΔP)*1/Z
C_real = C_values*(1/Z)
# Create DataFrame
data = pd.DataFrame({
    'Pi (Pa)': P_i_values,
    'Pf (Pa)': P_f_values,
    'Vi (m³)': V_i_values,
    'Vf (m³)': V_f_values,
    'ΔP (Pa)': ΔP_values,
    'ΔV (m³)': ΔV_values,
    'C = ΔV / ΔP (m⁴·s²/kg)': C_values,
    'Cr = (ΔV / ΔP)*(1/Z) (m⁴·s²/kg)': C_real
})

# Save data to CSV if needed
data.to_csv("compression_data.csv", index=False)

# Display the first few rows for verification
print(data)
