"""
Generate visualizations for habitat preference analysis results.

Creates publication-quality figures showing species distributions
across water body types and environmental characteristics.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10


class HabitatVisualization:
    """Create visualizations for habitat preference analysis."""
    
    def __init__(self, data_path='data/species_habitat_data.csv'):
        """Initialize with data."""
        self.df = pd.read_csv(data_path)
        # Updated species codes
        self.species = ['RGS', 'RES', 'PH']
        self.water_types = self.df['water_body_type'].unique()
        self.output_dir = Path('plots')
        self.output_dir.mkdir(exist_ok=True)
    
    def plot_occurrence_by_habitat(self):
        """Create bar plot of species occurrence rates by habitat type."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate occurrence rates
        occurrence_data = []
        for water_type in self.water_types:
            habitat_subset = self.df[self.df['water_body_type'] == water_type]
            for species in self.species:
                rate = (habitat_subset[f'{species}_present'].sum() / len(habitat_subset)) * 100
                occurrence_data.append({
                    'Water Body Type': water_type,
                    'Species': species,
                    'Occurrence Rate (%)': rate
                })
        
        occurrence_df = pd.DataFrame(occurrence_data)
        
        # Create grouped bar plot
        x = np.arange(len(self.water_types))
        width = 0.25
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        
        for i, species in enumerate(self.species):
            species_data = occurrence_df[occurrence_df['Species'] == species]
            rates = [species_data[species_data['Water Body Type'] == wt]['Occurrence Rate (%)'].values[0] 
                     for wt in self.water_types]
            ax.bar(x + i*width, rates, width, label=species, color=colors[i], alpha=0.8)
        
        ax.set_xlabel('Water Body Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Occurrence Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Species Occurrence Rates Across Water Body Types', fontsize=14, fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels(self.water_types)
        ax.legend(title='Species', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, 100])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'occurrence_by_habitat.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: occurrence_by_habitat.png")
        plt.close()
    
    def plot_heatmap(self):
        """Create heatmap of species presence across habitats."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create pivot table
        heatmap_data = []
        for water_type in self.water_types:
            habitat_subset = self.df[self.df['water_body_type'] == water_type]
            row = []
            for species in self.species:
                rate = (habitat_subset[f'{species}_present'].sum() / len(habitat_subset)) * 100
                row.append(rate)
            heatmap_data.append(row)
        
        heatmap_array = np.array(heatmap_data)
        
        # Create heatmap
        sns.heatmap(heatmap_array, annot=True, fmt='.1f', cmap='YlOrRd', 
                    xticklabels=self.species, yticklabels=self.water_types,
                    cbar_kws={'label': 'Occurrence Rate (%)'}, ax=ax,
                    vmin=0, vmax=100)
        
        ax.set_title('Habitat Preference Heatmap\n(% Species Occurrence by Water Body Type)', 
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Species', fontsize=12, fontweight='bold')
        ax.set_ylabel('Water Body Type', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'habitat_preference_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: habitat_preference_heatmap.png")
        plt.close()
    
    def plot_environmental_conditions(self):
        """Plot environmental characteristics of each habitat type."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        env_features = {
            'salinity_ppt': ('Salinity (ppt)', 0),
            'pH': ('pH', 1),
            'temperature_C': ('Temperature (°C)', 2),
            'dissolved_oxygen_mg_L': ('Dissolved Oxygen (mg/L)', 3)
        }
        
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        
        for feature, (label, idx) in env_features.items():
            ax = axes[idx]
            
            # Create box plot
            data_by_type = [self.df[self.df['water_body_type'] == wt][feature].values 
                           for wt in self.water_types]
            
            bp = ax.boxplot(data_by_type, labels=self.water_types, patch_artist=True)
            
            # Customize colors
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel(label, fontsize=11, fontweight='bold')
            ax.set_xlabel('Water Body Type', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
        
        fig.suptitle('Environmental Characteristics by Water Body Type', 
                    fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'environmental_conditions.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: environmental_conditions.png")
        plt.close()
    
    def plot_species_distribution(self):
        """Create multi-panel plot showing each species distribution."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Map new water facet names to colors
        colors = {'Clear spring fed pond': '#2E86AB', 'vegetated pond': '#A23B72', 'Oxbow analog': '#F18F01'}
        
        for idx, species in enumerate(self.species):
            ax = axes[idx]
            
            # Count occurrences
            species_present = self.df[self.df[f'{species}_present'] == 1]
            habitat_counts = species_present['water_body_type'].value_counts()
            
            # Create bar plot
            habitats = self.water_types
            counts = [habitat_counts.get(h, 0) for h in habitats]
            bar_colors = [colors[h] for h in habitats]
            
            bars = ax.bar(habitats, counts, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # Add count labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontweight='bold')
            
            ax.set_ylabel('Number of Observations', fontsize=11, fontweight='bold')
            ax.set_xlabel('Water Body Type', fontsize=11, fontweight='bold')
            ax.set_title(f'{species}', fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.suptitle('Species Distribution Across Habitats', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'species_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: species_distribution.png")
        plt.close()
    
    def plot_co_occurrence(self):
        """Plot species co-occurrence patterns by habitat."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for idx, water_type in enumerate(self.water_types):
            ax = axes[idx]
            habitat_subset = self.df[self.df['water_body_type'] == water_type]
            
            # Create co-occurrence matrix
            co_occur = np.zeros((3, 3))
            for i, sp1 in enumerate(self.species):
                for j, sp2 in enumerate(self.species):
                    if i == j:
                        co_occur[i, j] = habitat_subset[f'{sp1}_present'].sum()
                    else:
                        co_occur[i, j] = ((habitat_subset[f'{sp1}_present'] == 1) & 
                                        (habitat_subset[f'{sp2}_present'] == 1)).sum()
            
            # Plot heatmap
            sns.heatmap(co_occur, annot=True, fmt='.0f', cmap='Blues', ax=ax,
                       xticklabels=self.species, yticklabels=self.species,
                       cbar_kws={'label': 'Count'})
            
            ax.set_title(f'{water_type}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Species', fontsize=11, fontweight='bold')
            if idx == 0:
                ax.set_ylabel('Species', fontsize=11, fontweight='bold')
        
        fig.suptitle('Species Co-occurrence by Habitat Type', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'species_cooccurrence.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: species_cooccurrence.png")
        plt.close()
    
    def generate_all_plots(self):
        """Generate all visualizations."""
        print("\n" + "="*70)
        print("GENERATING VISUALIZATIONS")
        print("="*70 + "\n")
        
        self.plot_occurrence_by_habitat()
        self.plot_heatmap()
        self.plot_environmental_conditions()
        self.plot_species_distribution()
        self.plot_co_occurrence()
        
        print(f"\n✓ All plots saved to: {self.output_dir}")


if __name__ == "__main__":
    viz = HabitatVisualization()
    viz.generate_all_plots()
