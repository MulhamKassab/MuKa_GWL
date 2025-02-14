import math


def calculate_hs(h1, h2, h_v):
    """
    Calculate h_s, h_{s,1}, and h_{s,2} based on the given formulas.
    """

    # h_s: Average thickness plus interlayer thickness
    hs = 0.5 * (h1 + h2) + h_v

    # h_{s,1}: Harmonic mean of the glass layer thicknesses
    hs_1 = (hs * h1) / (h1 + h2)

    # h_{s,2}: Combined effective thickness considering h_s
    hs_2 = (hs * h2) / (h1 + h2)

    return hs_1, hs, hs_2


def calculate_gamma(E, G, h_v, h_s, I_s, a):
    """
    Calculate the shear transfer coefficient (Γ).
    """
    fraction = (E * I_s * h_v) / (G * h_s ** 2 * a ** 2)

    # Calculating Gamma (Γ)
    gamma = 1 / (1 + 9.6 * fraction)
    return gamma


def calculate_effective_thickness(h1, h2, I_s, gamma):
    """
    Calculate the effective thickness for deflection (h_ef,w).
    """
    h_ef_w = (h1 ** 3 + h2 ** 3 + 12 * I_s * gamma)**(1/3)
    return h_ef_w


def calculate_deflection(q, a, k, E_glass, h_ef_w):
    """
    Calculate the deflection (δ) of the laminated glass.
    """
    delta = (4 * q * a ** 3) / (E_glass * h_ef_w ** 3)
    return delta


def laminated_glass_deflection(q, a, h1, h2, h_v, G_interlayer, E_glass, k):
    """
    Full process for calculating deflection with a non-equivalent interlayer.
    """
    # Step 1: Calculate h_s, h_{s,1}, and h_{s,2}
    hs_1, hs, hs_2 = calculate_hs(h1, h2, h_v)

    # Step 2: Calculate I_s
    I_s = h1 * hs_2 ** 2 + h2 * hs_1 ** 2  # Using h_{s,1} for I_s

    # Step 3: Calculate Γ
    gamma = calculate_gamma(E_glass, G_interlayer, h_v, hs, I_s, a)

    # Step 4: Calculate h_ef,w
    h_ef_w = calculate_effective_thickness(h1, h2, I_s, gamma)

    # Step 5: Calculate deflection
    delta = calculate_deflection(q, a, k, E_glass, h_ef_w)

    return {
        "hs_1": hs_1,
        "hs": hs,
        "hs_2": hs_2,
        "gamma": gamma,
        "h_ef_w": h_ef_w,
        "deflection": delta
    }


# Example Input
G_interlayer = 0.72  # Shear modulus of interlayer (MPa)
E_glass = 71700  # Young's modulus of glass (MPa)

h1 = 9.02 # Thickness of the first glass layer (mm)
h2 = 9.02  # Thickness of the second glass layer (mm)
h_v = 1.52 # Thickness of the interlayer (mm)

q = 0.75  # Uniform load (kPa)
a = 1000  # Shorter side of the laminated plate (mm)
k = 0.013  # Boundary condition factor for 4-sided support (example value)

# Perform Calculation
results = laminated_glass_deflection(q, a, h1, h2, h_v, G_interlayer, E_glass, k)

# Output Results
print(f"h_s,1: {results['hs_1']:.4f} mm")
print(f"h_s: {results['hs']:.4f} mm")
print(f"h_s,2: {results['hs_2']:.4f} mm")
print(f"Γ (Gamma): {results['gamma']:.4f}")
print(f"Effective Thickness (h_ef,w): {results['h_ef_w']:.4f} mm")
print(f"Deflection (δ): {results['deflection']:.4f} mm")
