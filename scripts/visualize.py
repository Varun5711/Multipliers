#!/usr/bin/env python3
"""
Visualization script for multiplier analysis results
Generates comparison graphs for Classical, Dadda, and Wallace multipliers
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set style for better-looking graphs
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#e74c3c', '#3498db', '#2ecc71']  # Red, Blue, Green

def load_results():
    """Load analysis results from JSON file"""
    with open('results/analysis_results.json', 'r') as f:
        return json.load(f)

def plot_area_comparison(data, ax):
    """Plot area comparison bar chart"""
    names = list(data.keys())
    cells = [data[name]['total_cells'] for name in names]
    area_ge = [data[name]['estimated_area_ge'] for name in names]

    x = np.arange(len(names))
    width = 0.35

    ax1 = ax
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width/2, cells, width, label='Total Cells', color=colors, alpha=0.8)
    bars2 = ax2.bar(x + width/2, area_ge, width, label='Area (GE)', color=colors, alpha=0.5, hatch='//')

    ax1.set_xlabel('Multiplier Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Total Cells', fontsize=11, fontweight='bold', color='navy')
    ax2.set_ylabel('Estimated Area (GE)', fontsize=11, fontweight='bold', color='darkgreen')
    ax1.set_title('Area Comparison: Cell Count vs Gate Equivalents', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    ax1.tick_params(axis='y', labelcolor='navy')
    ax2.tick_params(axis='y', labelcolor='darkgreen')
    ax1.grid(True, alpha=0.3)

    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars1, cells)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    for i, (bar, val) in enumerate(zip(bars2, area_ge)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

def plot_timing_comparison(data, ax):
    """Plot timing comparison"""
    names = list(data.keys())
    delays = [data[name]['critical_path_delay_ns'] for name in names]
    freqs = [data[name]['max_frequency_mhz'] for name in names]

    x = np.arange(len(names))
    width = 0.35

    ax1 = ax
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width/2, delays, width, label='Critical Path Delay (ns)',
                    color=colors, alpha=0.8)
    bars2 = ax2.bar(x + width/2, freqs, width, label='Max Frequency (MHz)',
                    color=colors, alpha=0.5, hatch='\\\\')

    ax1.set_xlabel('Multiplier Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Critical Path Delay (ns)', fontsize=11, fontweight='bold', color='darkred')
    ax2.set_ylabel('Max Frequency (MHz)', fontsize=11, fontweight='bold', color='darkblue')
    ax1.set_title('Timing Analysis: Delay vs Maximum Frequency', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    ax1.tick_params(axis='y', labelcolor='darkred')
    ax2.tick_params(axis='y', labelcolor='darkblue')
    ax1.grid(True, alpha=0.3)

    # Add value labels
    for bar, val in zip(bars1, delays):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    for bar, val in zip(bars2, freqs):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

def plot_power_comparison(data, ax):
    """Plot power consumption comparison"""
    names = list(data.keys())
    power = [data[name]['estimated_power_mw'] for name in names]
    energy = [p * 10 for p in power]  # Energy per operation in pJ

    x = np.arange(len(names))
    width = 0.35

    ax1 = ax
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width/2, power, width, label='Power (mW @ 100MHz)',
                    color=colors, alpha=0.8)
    bars2 = ax2.bar(x + width/2, energy, width, label='Energy/Op (pJ)',
                    color=colors, alpha=0.5, hatch='xx')

    ax1.set_xlabel('Multiplier Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Power Consumption (mW)', fontsize=11, fontweight='bold', color='darkviolet')
    ax2.set_ylabel('Energy per Operation (pJ)', fontsize=11, fontweight='bold', color='darkorange')
    ax1.set_title('Power Analysis: Power Consumption vs Energy per Operation',
                  fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    ax1.tick_params(axis='y', labelcolor='darkviolet')
    ax2.tick_params(axis='y', labelcolor='darkorange')
    ax1.grid(True, alpha=0.3)

    # Add value labels
    for bar, val in zip(bars1, power):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    for bar, val in zip(bars2, energy):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

def plot_gate_breakdown(data, ax):
    """Plot gate type breakdown as stacked bar chart"""
    names = list(data.keys())
    gate_types = ['and_gates', 'or_gates', 'xor_gates', 'nand_gates', 'xnor_gates']
    gate_labels = ['AND', 'OR', 'XOR', 'NAND', 'XNOR']
    gate_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#a29bfe']

    x = np.arange(len(names))
    width = 0.6

    # Prepare data for stacking
    gate_counts = []
    for gate in gate_types:
        gate_counts.append([data[name][gate] for name in names])

    # Create stacked bars
    bottom = np.zeros(len(names))
    bars = []
    for i, (counts, label, color) in enumerate(zip(gate_counts, gate_labels, gate_colors)):
        bar = ax.bar(x, counts, width, label=label, bottom=bottom, color=color, alpha=0.8)
        bars.append(bar)
        bottom += np.array(counts)

    ax.set_xlabel('Multiplier Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Gates', fontsize=11, fontweight='bold')
    ax.set_title('Gate Type Breakdown by Multiplier', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend(loc='upper right', ncol=2)
    ax.grid(True, alpha=0.3, axis='y')

    # Add total count on top
    for i, name in enumerate(names):
        total = data[name]['total_cells']
        ax.text(i, total, f'{total:,}', ha='center', va='bottom',
               fontsize=10, fontweight='bold')

def plot_normalized_comparison(data, ax):
    """Plot normalized comparison (spider/radar chart alternative as grouped bars)"""
    names = list(data.keys())

    # Normalize metrics (inverse for delay - lower is better)
    metrics = ['Area', 'Delay', 'Power', 'Cells']

    # Get values and normalize to percentage of best
    area_vals = [data[name]['estimated_area_ge'] for name in names]
    delay_vals = [data[name]['critical_path_delay_ns'] for name in names]
    power_vals = [data[name]['estimated_power_mw'] for name in names]
    cells_vals = [data[name]['total_cells'] for name in names]

    min_area = min(area_vals)
    min_delay = min(delay_vals)
    min_power = min(power_vals)
    min_cells = min(cells_vals)

    # Normalized (relative to best = 1.0)
    norm_data = {
        name: [
            data[name]['estimated_area_ge'] / min_area,
            data[name]['critical_path_delay_ns'] / min_delay,
            data[name]['estimated_power_mw'] / min_power,
            data[name]['total_cells'] / min_cells
        ]
        for name in names
    }

    x = np.arange(len(metrics))
    width = 0.25

    for i, name in enumerate(names):
        offset = (i - 1) * width
        bars = ax.bar(x + offset, norm_data[name], width, label=name,
                     color=colors[i], alpha=0.8)

        # Add value labels
        for bar, val in zip(bars, norm_data[name]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.2f}x', ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
    ax.set_ylabel('Relative to Best (1.0 = optimal)', fontsize=11, fontweight='bold')
    ax.set_title('Normalized Performance Comparison (Lower is Better)',
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Optimal')

def plot_efficiency_scatter(data, ax):
    """Plot efficiency: Area vs Delay scatter plot"""
    names = list(data.keys())
    areas = [data[name]['estimated_area_ge'] for name in names]
    delays = [data[name]['critical_path_delay_ns'] for name in names]
    powers = [data[name]['estimated_power_mw'] for name in names]

    # Normalize power for size
    max_power = max(powers)
    sizes = [1000 * (p / max_power) for p in powers]

    scatter = ax.scatter(areas, delays, s=sizes, c=colors, alpha=0.6, edgecolors='black', linewidth=2)

    # Add labels
    for i, name in enumerate(names):
        ax.annotate(name, (areas[i], delays[i]),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=colors[i], alpha=0.3),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1.5))

    ax.set_xlabel('Estimated Area (GE)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Critical Path Delay (ns)', fontsize=12, fontweight='bold')
    ax.set_title('Efficiency Map: Area vs Delay\n(Bubble size = Power consumption)',
                 fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Add "better" annotations
    ax.text(0.02, 0.98, 'FASTER', transform=ax.transAxes,
           fontsize=10, verticalalignment='top', color='green', fontweight='bold')
    ax.text(0.98, 0.02, 'LARGER', transform=ax.transAxes,
           fontsize=10, horizontalalignment='right', color='red', fontweight='bold')

def create_all_plots(data):
    """Create all visualization plots"""
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('Multiplier Design Comparison: Classical vs Dadda vs Wallace',
                 fontsize=16, fontweight='bold', y=0.995)

    # Create grid of subplots
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.35)

    ax1 = fig.add_subplot(gs[0, 0])
    plot_area_comparison(data, ax1)

    ax2 = fig.add_subplot(gs[0, 1])
    plot_timing_comparison(data, ax2)

    ax3 = fig.add_subplot(gs[1, 0])
    plot_power_comparison(data, ax3)

    ax4 = fig.add_subplot(gs[1, 1])
    plot_gate_breakdown(data, ax4)

    ax5 = fig.add_subplot(gs[2, 0])
    plot_normalized_comparison(data, ax5)

    ax6 = fig.add_subplot(gs[2, 1])
    plot_efficiency_scatter(data, ax6)

    plt.savefig('results/multiplier_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: results/multiplier_comparison.png")

    # Create individual plots for easier viewing
    create_individual_plots(data)

def create_individual_plots(data):
    """Create individual plots for each metric"""

    # 1. Area comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_area_comparison(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_area_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_area_comparison.png")
    plt.close()

    # 2. Timing comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_timing_comparison(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_timing_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_timing_comparison.png")
    plt.close()

    # 3. Power comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_power_comparison(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_power_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_power_comparison.png")
    plt.close()

    # 4. Gate breakdown
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_gate_breakdown(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_gate_breakdown.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_gate_breakdown.png")
    plt.close()

    # 5. Normalized comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_normalized_comparison(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_normalized_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_normalized_comparison.png")
    plt.close()

    # 6. Efficiency scatter
    fig, ax = plt.subplots(figsize=(10, 8))
    plot_efficiency_scatter(data, ax)
    plt.tight_layout()
    plt.savefig('results/graph_efficiency_map.png', dpi=300, bbox_inches='tight')
    print("Saved: results/graph_efficiency_map.png")
    plt.close()

def main():
    print("="*70)
    print("MULTIPLIER VISUALIZATION GENERATOR")
    print("="*70)

    # Load results
    print("\nLoading analysis results...")
    data = load_results()
    print(f"Loaded data for: {', '.join(data.keys())}")

    # Create plots
    print("\nGenerating visualizations...")
    create_all_plots(data)

    print("\n" + "="*70)
    print("VISUALIZATION COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    print("  - results/multiplier_comparison.png (combined view)")
    print("  - results/graph_area_comparison.png")
    print("  - results/graph_timing_comparison.png")
    print("  - results/graph_power_comparison.png")
    print("  - results/graph_gate_breakdown.png")
    print("  - results/graph_normalized_comparison.png")
    print("  - results/graph_efficiency_map.png")
    print("="*70)

if __name__ == '__main__':
    main()
