"""
Generate synthetic species occurrence data across different water body types.

This script creates realistic ecological data for analyzing habitat preferences
of three aquatic species across three water body types.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_habitat_data(n_samples=500):
    """
    Generate synthetic observations of species occurrences in different water habitats.
    
    Parameters:
    -----------
    n_samples : int
        Number of total observations to generate
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with habitat characteristics and species presence
    """
    
    # Define water body types and their characteristics
    # Updated to user's water facets
    water_types = ['Clear spring fed pond', 'vegetated pond', 'Oxbow analog']
    species = ['RGS', 'RES', 'PH']
    
    data = []
    
    for water_type in water_types:
        # Generate n_samples/3 observations for each water body type
        n_habitat_samples = n_samples // 3
        
        # Generate environmental characteristics specific to each water type
        if water_type == 'Clear spring fed pond':
            # Clear spring-fed ponds: very low salinity, stable pH, cooler temperature
            salinity = np.random.normal(0.2, 0.1, n_habitat_samples)
            ph = np.random.normal(7.4, 0.3, n_habitat_samples)
            temperature = np.random.normal(12, 3, n_habitat_samples)
            dissolved_oxygen = np.random.normal(9.0, 1.0, n_habitat_samples)

        elif water_type == 'vegetated pond':
            # Vegetated ponds: low salinity, slightly higher temperature, variable DO
            salinity = np.random.normal(0.6, 0.4, n_habitat_samples)
            ph = np.random.normal(7.0, 0.5, n_habitat_samples)
            temperature = np.random.normal(16, 4, n_habitat_samples)
            dissolved_oxygen = np.random.normal(7.5, 1.5, n_habitat_samples)

        else:  # Oxbow analog
            # Oxbow analogs: low salinity, often warmer and more variable pH/DO
            salinity = np.random.normal(1.0, 0.6, n_habitat_samples)
            ph = np.random.normal(7.8, 0.6, n_habitat_samples)
            temperature = np.random.normal(17, 4, n_habitat_samples)
            dissolved_oxygen = np.random.normal(7.2, 1.3, n_habitat_samples)
        
        # Ensure values are within realistic ranges
        salinity = np.clip(salinity, 0, 40)
        ph = np.clip(ph, 6, 9)
        temperature = np.clip(temperature, 0, 35)
        dissolved_oxygen = np.clip(dissolved_oxygen, 2, 12)
        
        # Generate species occurrences based on habitat preference
        for i in range(n_habitat_samples):
            obs = {
                'observation_id': len(data) + 1,
                'water_body_type': water_type,
                'salinity_ppt': salinity[i],
                'pH': ph[i],
                'temperature_C': temperature[i],
                'dissolved_oxygen_mg_L': dissolved_oxygen[i]
            }
            
            # Define habitat preferences for each species (renamed to user codes)
            # RGS: analogous to Carp, prefers clear spring fed ponds
            rgs_prob = 0.85 if water_type == 'Clear spring fed pond' else (0.30 if water_type == 'Oxbow analog' else 0.05)
            obs['RGS_present'] = 1 if np.random.random() < rgs_prob else 0

            # RES: analogous to Tuna, but here uses preference for Oxbow analog
            res_prob = 0.90 if water_type == 'Oxbow analog' else (0.25 if water_type == 'vegetated pond' else 0.02)
            obs['RES_present'] = 1 if np.random.random() < res_prob else 0

            # PH: analogous to Mullet, adaptable and often found in vegetated ponds
            ph_prob = 0.85 if water_type == 'vegetated pond' else (0.50 if water_type == 'Oxbow analog' else 0.45)
            obs['PH_present'] = 1 if np.random.random() < ph_prob else 0
            
            data.append(obs)
    
    df = pd.DataFrame(data)
    return df


def save_data(df, output_path='data/species_habitat_data.csv'):
    """Save generated data to CSV file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(f"Dataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData summary:")
    print(df.describe())
    return df


if __name__ == "__main__":
    # Generate and save data
    df = generate_habitat_data(n_samples=500)
    save_data(df)
