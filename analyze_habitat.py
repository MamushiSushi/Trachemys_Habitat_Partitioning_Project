"""
Analyze habitat preferences of aquatic species across water body types.

This module performs statistical analysis to determine if species show
significant preference for particular water body types.
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
from pathlib import Path


class HabitatPreferenceAnalysis:
    """Analyze species habitat preferences."""
    
    def __init__(self, data_path='data/species_habitat_data.csv'):
        """
        Initialize analysis with data.
        
        Parameters:
        -----------
        data_path : str
            Path to the species habitat CSV file
        """
        self.df = pd.read_csv(data_path)
        # Updated species codes
        self.species = ['RGS', 'RES', 'PH']
        self.results = {}
        
    def contingency_analysis(self):
        """
        Perform chi-square test for independence between species presence
        and water body type.
        """
        print("\n" + "="*70)
        print("CONTINGENCY TABLE ANALYSIS - Chi-Square Test")
        print("="*70)
        
        contingency_results = {}
        
        for species in self.species:
            # Create contingency table
            contingency = pd.crosstab(
                self.df['water_body_type'],
                self.df[f'{species}_present']
            )
            
            # Perform chi-square test
            chi2, p_value, dof, expected_freq = chi2_contingency(contingency)
            
            contingency_results[species] = {
                'contingency_table': contingency.to_dict(),
                'chi2_statistic': float(chi2),
                'p_value': float(p_value),
                'degrees_of_freedom': int(dof),
                'significant': bool(p_value < 0.05)
            }
            
            print(f"\n{species.upper()}")
            print("-" * 70)
            print(f"Contingency Table:")
            print(contingency)
            print(f"\nChi-square statistic: {chi2:.4f}")
            print(f"P-value: {p_value:.4e}")
            print(f"Result: {'SIGNIFICANT' if p_value < 0.05 else 'NOT SIGNIFICANT'} habitat preference")
        
        self.results['contingency_analysis'] = contingency_results
        return contingency_results
    
    def calculate_occurrence_rates(self):
        """
        Calculate species occurrence rates in each water body type.
        """
        print("\n" + "="*70)
        print("OCCURRENCE RATES BY HABITAT TYPE")
        print("="*70)
        
        occurrence_data = []
        
        for water_type in self.df['water_body_type'].unique():
            habitat_subset = self.df[self.df['water_body_type'] == water_type]
            n_observations = len(habitat_subset)
            
            print(f"\n{water_type.upper()} (n={n_observations})")
            print("-" * 70)
            
            for species in self.species:
                occurrences = habitat_subset[f'{species}_present'].sum()
                rate = (occurrences / n_observations) * 100
                
                occurrence_data.append({
                    'species': species,
                    'water_body_type': water_type,
                    'occurrences': int(occurrences),
                    'n_observations': n_observations,
                    'occurrence_rate': float(rate)
                })
                
                print(f"  {species}: {occurrences}/{n_observations} ({rate:.1f}%)")
        
        occurrence_df = pd.DataFrame(occurrence_data)
        self.results['occurrence_rates'] = occurrence_df.to_dict(orient='records')
        return occurrence_df
    
    def habitat_similarity(self):
        """
        Analyze environmental similarity between habitat types using
        multivariate measures.
        """
        print("\n" + "="*70)
        print("HABITAT ENVIRONMENTAL CHARACTERISTICS")
        print("="*70)
        
        env_features = ['salinity_ppt', 'pH', 'temperature_C', 'dissolved_oxygen_mg_L']
        
        habitat_stats = {}
        
        for water_type in self.df['water_body_type'].unique():
            habitat_subset = self.df[self.df['water_body_type'] == water_type][env_features]
            
            print(f"\n{water_type.upper()}")
            print("-" * 70)
            
            stats = {
                'salinity_mean': float(habitat_subset['salinity_ppt'].mean()),
                'salinity_std': float(habitat_subset['salinity_ppt'].std()),
                'pH_mean': float(habitat_subset['pH'].mean()),
                'pH_std': float(habitat_subset['pH'].std()),
                'temperature_mean': float(habitat_subset['temperature_C'].mean()),
                'temperature_std': float(habitat_subset['temperature_C'].std()),
                'dissolved_oxygen_mean': float(habitat_subset['dissolved_oxygen_mg_L'].mean()),
                'dissolved_oxygen_std': float(habitat_subset['dissolved_oxygen_mg_L'].std())
            }
            
            habitat_stats[water_type] = stats
            
            print(f"  Salinity: {stats['salinity_mean']:.2f} ± {stats['salinity_std']:.2f} ppt")
            print(f"  pH: {stats['pH_mean']:.2f} ± {stats['pH_std']:.2f}")
            print(f"  Temperature: {stats['temperature_mean']:.2f} ± {stats['temperature_std']:.2f} °C")
            print(f"  Dissolved Oxygen: {stats['dissolved_oxygen_mean']:.2f} ± {stats['dissolved_oxygen_std']:.2f} mg/L")
        
        self.results['habitat_characteristics'] = habitat_stats
        return habitat_stats
    
    def summarize_findings(self):
        """
        Generate summary interpretation of findings.
        """
        print("\n" + "="*70)
        print("SUMMARY OF HABITAT PREFERENCES")
        print("="*70)
        
        summary = {}
        
        for species in self.species:
            occurrence_rates = self.results['occurrence_rates']
            species_data = [r for r in occurrence_rates if r['species'] == species]
            
            # Find preferred habitat
            preferred = max(species_data, key=lambda x: x['occurrence_rate'])
            
            summary[species] = {
                'preferred_habitat': preferred['water_body_type'],
                'preference_rate': preferred['occurrence_rate']
            }
            
            print(f"\n{species.upper()}")
            print(f"  Preferred habitat: {preferred['water_body_type']}")
            print(f"  Occurrence rate in preferred habitat: {preferred['occurrence_rate']:.1f}%")
        
        self.results['summary'] = summary
        return summary
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline."""
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + "AQUATIC SPECIES HABITAT PREFERENCE ANALYSIS".center(68) + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        
        self.contingency_analysis()
        self.calculate_occurrence_rates()
        self.habitat_similarity()
        self.summarize_findings()
        
        return self.results
    
    def save_results(self, output_path='results/analysis_results.json'):
        """Save analysis results to JSON file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to {output_path}")


if __name__ == "__main__":
    # Run analysis
    analysis = HabitatPreferenceAnalysis()
    analysis.run_full_analysis()
    analysis.save_results()
