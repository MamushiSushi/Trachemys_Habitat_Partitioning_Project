"""
Main execution script for the habitat preference analysis pipeline.

Runs the complete workflow:
1. Generate synthetic species-habitat data
2. Perform statistical analysis
3. Create visualizations
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from generate_data import generate_habitat_data, save_data
from analyze_habitat import HabitatPreferenceAnalysis
from visualize_results import HabitatVisualization


def main():
    """Execute complete analysis pipeline."""
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "AQUATIC SPECIES HABITAT PREFERENCE ANALYSIS PIPELINE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")
    
    # Step 1: Generate Data
    print("[1/3] GENERATING SYNTHETIC DATA...")
    print("-" * 70)
    df = generate_habitat_data(n_samples=500)
    save_data(df, 'data/species_habitat_data.csv')
    print("✓ Data generation complete\n")
    
    # Step 2: Run Analysis
    print("[2/3] PERFORMING STATISTICAL ANALYSIS...")
    print("-" * 70)
    analysis = HabitatPreferenceAnalysis('data/species_habitat_data.csv')
    analysis.run_full_analysis()
    analysis.save_results('results/analysis_results.json')
    print("✓ Analysis complete\n")
    
    # Step 3: Generate Visualizations
    print("[3/3] GENERATING VISUALIZATIONS...")
    print("-" * 70)
    viz = HabitatVisualization('data/species_habitat_data.csv')
    viz.generate_all_plots()
    print("✓ Visualization complete\n")
    
    # Summary
    print("█"*70)
    print("█" + " "*68 + "█")
    print("█" + "PIPELINE EXECUTION COMPLETE!".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    print("\nOutputs generated:")
    print("  ✓ data/species_habitat_data.csv (500 observations)")
    print("  ✓ results/analysis_results.json (statistical results)")
    print("  ✓ plots/ (5 publication-quality figures)")
    print("\nReady for presentation! 🎉\n")


if __name__ == "__main__":
    main()
