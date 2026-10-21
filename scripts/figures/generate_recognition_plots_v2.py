"""
Generate additional detailed illustrations for Visual Recognition I notes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle, Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def plot_harris_math():
    """Harris detector mathematical derivation visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel 1: Structure Tensor and Eigenvalues
    ax = axes[0, 0]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')

    # Draw ellipse representing M matrix
    angles = np.linspace(0, 2*np.pi, 100)
    # Example: lambda1=1.5, lambda2=0.3 (edge)
    lambda1, lambda2 = 1.5, 0.3
    theta = np.pi/6

    x = np.sqrt(lambda1) * np.cos(angles)
    y = np.sqrt(lambda2) * np.sin(angles)

    # Rotate
    x_rot = x * np.cos(theta) - y * np.sin(theta)
    y_rot = x * np.sin(theta) + y * np.cos(theta)

    ax.plot(x_rot, y_rot, 'b-', linewidth=2, label='Edge (λ1 >> λ2)')

    # Corner case
    lambda1, lambda2 = 1.2, 1.0
    x = np.sqrt(lambda1) * np.cos(angles)
    y = np.sqrt(lambda2) * np.sin(angles)
    x_rot2 = x * np.cos(theta) - y * np.sin(theta)
    y_rot2 = x * np.sin(theta) + y * np.cos(theta)
    ax.plot(x_rot2 + 3, y_rot2, 'r-', linewidth=2, label='Corner (λ1 ≈ λ2)')

    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    ax.set_title('Structure Tensor Eigenvalue Interpretation\n(Ellipse: gradient distribution)', fontsize=10)
    ax.legend(fontsize=8)
    ax.axis('off')

    # Panel 2: Eigenvalue space classification
    ax = axes[0, 1]
    lambda1_range = np.linspace(0, 3, 100)
    lambda2_range = np.linspace(0, 3, 100)
    L1, L2 = np.meshgrid(lambda1_range, lambda2_range)

    # Harris response R = λ1*λ2 - k*(λ1+λ2)^2
    k = 0.04
    R = L1 * L2 - k * (L1 + L2)**2

    contour = ax.contour(L1, L2, R, levels=[-0.1, 0, 0.1], colors=['blue', 'black', 'red'])
    ax.clabel(contour, inline=True, fontsize=8)

    # Label regions
    ax.text(0.3, 0.3, 'Flat\n(λ1≈λ2≈0)', ha='center', fontsize=9, style='italic')
    ax.text(2.5, 0.3, 'Edge\n(λ1>>λ2)', ha='center', fontsize=9, style='italic', color='blue')
    ax.text(2.0, 2.0, 'Corner\n(λ1≈λ2>>0)', ha='center', fontsize=9, style='italic', color='red')

    ax.set_xlabel('λ1 (larger eigenvalue)', fontsize=9)
    ax.set_ylabel('λ2 (smaller eigenvalue)', fontsize=9)
    ax.set_title('Harris Response in Eigenvalue Space\n(R = λ1λ2 - k(λ1+λ2)²)', fontsize=10)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    # Panel 3: DoG pyramid
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Draw octave pyramid
    for i, (w, h, label) in enumerate([(8, 6, 'Octave 0\n(σ, 2σ, 4σ, ...)'),
                                        (6, 4.5, 'Octave 1\n(2σ, 4σ, 8σ, ...)'),
                                        (4.5, 3.4, 'Octave 2\n(4σ, 8σ, ...)')]):
        x = 5 - w/2
        y = 6 - i * 2
        rect = Rectangle((x, y), w, h, fill=False, edgecolor=f'C{i}', linewidth=2)
        ax.add_patch(rect)
        ax.text(5, y + h/2, label, ha='center', va='center', fontsize=9, color=f'C{i}')

        # Draw scales inside octave
        for j in range(3):
            small_rect = Rectangle((x + j*0.5, y + 0.2), 0.4, h - 0.4,
                                   facecolor=f'C{i}', alpha=0.3, edgecolor='none')
            ax.add_patch(small_rect)

    ax.set_title('Gaussian Pyramid Structure\n(Multiple Octaves and Scales)', fontsize=10)

    # Panel 4: DoG extrema detection
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Draw 3x3x3 cube representation
    cube_center = (5, 5)
    layers = ['Scale s-1', 'Scale s', 'Scale s+1']
    colors = ['lightblue', 'lightgreen', 'lightyellow']

    for i, (layer, color) in enumerate(zip(layers, colors)):
        y_offset = 6 - i * 1.5
        # Draw 3x3 grid
        for row in range(3):
            for col in range(3):
                rect = Rectangle((3 + col*1.2, y_offset - row*1.2), 1, 1,
                               facecolor=color, edgecolor='black', linewidth=1)
                ax.add_patch(rect)

                # Mark center in middle layer
                if i == 1 and row == 1 and col == 1:
                    circle = Circle((3.5 + col*1.2, y_offset + 0.5 - row*1.2), 0.3,
                                  facecolor='red', edgecolor='darkred')
                    ax.add_patch(circle)

        ax.text(7.5, y_offset - 0.5, layer, fontsize=8, va='center')

    ax.set_title('DoG Extrema Detection\n(3x3 spatial × 3 scale neighborhood)', fontsize=10)

    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/harris_sift_detailed.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: harris_sift_detailed.png")


def plot_vlad_fisher_math():
    """VLAD and Fisher Vector mathematical visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel 1: VLAD residual visualization
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Draw cluster centers
    centers = [(3, 7), (7, 7), (5, 3)]
    colors_centers = ['C0', 'C1', 'C2']

    for (cx, cy), color in zip(centers, colors_centers):
        circle = Circle((cx, cy), 0.2, facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(cx, cy-0.6, f'c_{list(colors_centers).index(color)+1}',
               ha='center', fontsize=9, weight='bold')

    # Draw features and residuals
    np.random.seed(42)
    for idx, ((cx, cy), color) in enumerate(zip(centers, colors_centers)):
        # Generate features around center
        for _ in range(5):
            fx = cx + np.random.randn() * 0.8
            fy = cy + np.random.randn() * 0.8

            # Draw feature point
            ax.plot(fx, fy, 'o', color=color, markersize=6, alpha=0.7)

            # Draw residual arrow
            dx = (fx - cx) * 2  # Scale for visibility
            dy = (fy - cy) * 2
            ax.annotate('', xy=(cx + dx, cy + dy), xytext=(cx, cy),
                       arrowprops=dict(arrowstyle='->', color=color, alpha=0.5, lw=1.5))

    ax.set_title('VLAD: Residual Aggregation\nv_k = Σ(x - c_k) for x in S_k', fontsize=10)
    ax.set_xlabel('Feature Dimension 1', fontsize=9)
    ax.set_ylabel('Feature Dimension 2', fontsize=9)

    # Panel 2: Fisher Vector gradients
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # GMM visualization
    x = np.linspace(0, 10, 100)
    y1 = 3 * np.exp(-(x-3)**2/2) + 2
    y2 = 2.5 * np.exp(-(x-7)**2/1.5) + 2

    ax.fill_between(x, 2, y1, alpha=0.3, color='C0', label='Gaussian 1')
    ax.fill_between(x, 2, y2, alpha=0.3, color='C1', label='Gaussian 2')

    # Draw data points
    np.random.seed(123)
    for _ in range(15):
        # Sample from mixture
        if np.random.rand() > 0.5:
            px = np.random.randn() * 0.7 + 3
        else:
            px = np.random.randn() * 0.6 + 7
        ax.plot(px, 2.3, 'ko', markersize=5)

    ax.set_ylim(0, 6)
    ax.set_title('Fisher Vector: GMM and Gradients\n∂log p(x|θ)/∂θ for each Gaussian',
                fontsize=10)
    ax.legend(loc='upper right', fontsize=8)

    # Panel 3: Aggregation comparison chart
    ax = axes[1, 0]

    methods = ['BoW\n(0-order)', 'VLAD\n(1-order)', 'Fisher\n(0+1+2-order)']
    info_content = [1, 2, 3]
    dimensions = [1000, 128*16, 257*16]  # Typical dimensions

    x_pos = np.arange(len(methods))
    bars = ax.bar(x_pos, info_content, color=['C0', 'C1', 'C2'], alpha=0.7, edgecolor='black')

    ax.set_ylabel('Information Order', fontsize=10)
    ax.set_title('Feature Aggregation: Information Content', fontsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(methods, fontsize=9)
    ax.set_ylim(0, 3.5)

    # Add dimension annotations
    for i, (bar, dim) in enumerate(zip(bars, dimensions)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
               f'{dim}D', ha='center', fontsize=8, style='italic')

    # Panel 4: Soft vs Hard assignment
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Hard assignment
    ax.text(2.5, 9, 'Hard Assignment', fontsize=10, weight='bold', ha='center')
    feature_pos = (2.5, 6)
    centers_hard = [(1, 4), (4, 4)]

    ax.plot(feature_pos[0], feature_pos[1], 'ko', markersize=10, label='Feature x')
    for i, (cx, cy) in enumerate(centers_hard):
        ax.plot(cx, cy, 's', color=f'C{i}', markersize=12, label=f'Center {i+1}')

    # Arrow to nearest
    ax.annotate('', xy=centers_hard[0], xytext=feature_pos,
               arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(2.5, 2.5, 'Assign to c1 only', fontsize=9, ha='center', color='red')

    # Soft assignment
    ax.text(7.5, 9, 'Soft Assignment', fontsize=10, weight='bold', ha='center')
    feature_pos2 = (7.5, 6)
    centers_soft = [(6, 4), (9, 4)]

    ax.plot(feature_pos2[0], feature_pos2[1], 'ko', markersize=10)
    for i, (cx, cy) in enumerate(centers_soft):
        ax.plot(cx, cy, 's', color=f'C{i}', markersize=12)

    # Weighted arrows
    ax.annotate('', xy=centers_soft[0], xytext=feature_pos2,
               arrowprops=dict(arrowstyle='->', color='C0', lw=1.5, alpha=0.7))
    ax.annotate('', xy=centers_soft[1], xytext=feature_pos2,
               arrowprops=dict(arrowstyle='->', color='C1', lw=1.5, alpha=0.7))
    ax.text(7.5, 2.5, 'Weight: γ1=0.6, γ2=0.4', fontsize=9, ha='center', color='blue')

    ax.set_title('Hard vs Soft Assignment\nQuantization Error Reduction',
                fontsize=10)

    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/aggregation_math.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: aggregation_math.png")


def plot_spm_pmk_theory():
    """SPM and PMK theoretical visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel 1: SPM weight computation
    ax = axes[0, 0]

    levels = [0, 1, 2]
    cells = [1, 4, 16]
    weights_uniform = [1, 1, 1]
    weights_inverse = [1/4, 1/2, 1]

    x = np.arange(len(levels))
    width = 0.35

    ax.bar(x - width/2, weights_uniform, width, label='Uniform w_l=1',
          color='C0', alpha=0.7, edgecolor='black')
    ax.bar(x + width/2, weights_inverse, width, label='Inverse w_l=1/2^(L-l)',
          color='C1', alpha=0.7, edgecolor='black')

    ax.set_xlabel('Pyramid Level l', fontsize=10)
    ax.set_ylabel('Weight', fontsize=10)
    ax.set_title('SPM: Level Weighting Strategies\n(Finer grids → higher weights)',
                fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Level {l}\n({c} cells)' for l, c in zip(levels, cells)])
    ax.legend(fontsize=9)

    # Panel 2: PMK matching levels
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Show matching at different levels
    for level, bin_size, y_pos in [(0, 10, 8), (1, 5, 4.5), (2, 2.5, 1)]:
        ax.text(0.5, y_pos + 1.5, f'Level {level}\n(bin size={bin_size})',
               fontsize=9, va='center', weight='bold')

        # Draw grid
        for i in range(int(10/bin_size)):
            for j in range(int(10/bin_size)):
                rect = Rectangle((2 + j*bin_size, y_pos - i*bin_size),
                               bin_size*0.9, bin_size*0.9,
                               fill=False, edgecolor='gray', linewidth=0.5)
                ax.add_patch(rect)

        # Draw matching pairs in one cell
        if level == 2:
            ax.plot(3.5, y_pos - 0.5, 'bo', markersize=6)
            ax.plot(3.7, y_pos - 0.3, 'ro', markersize=6)

    ax.set_title('PMK: Multi-Resolution Matching\n(Matches found at finest resolution)',
                fontsize=10)

    # Panel 3: Dimension comparison
    ax = axes[1, 0]

    K = 1000  # vocabulary size
    L_values = [0, 1, 2, 3]
    dims = [K * ((4**(L+1) - 1) / 3) for L in L_values]

    ax.plot(L_values, dims, 'o-', linewidth=2, markersize=8, color='C0')
    ax.fill_between(L_values, 0, dims, alpha=0.3, color='C0')

    for L, dim in zip(L_values, dims):
        ax.annotate(f'{int(dim):,}', xy=(L, dim), xytext=(L, dim+5000),
                   fontsize=9, ha='center')

    ax.set_xlabel('Number of Pyramid Levels (L)', fontsize=10)
    ax.set_ylabel('Feature Dimension', fontsize=10)
    ax.set_title('SPM Feature Dimension Growth\n(K=1000 visual words)',
                fontsize=10)
    ax.set_xticks(L_values)

    # Panel 4: BoW evolution timeline
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    methods_timeline = [
        ('2004', 'SIFT', 9),
        ('2006', 'SPM', 7.5),
        ('2008', 'Vocabulary Tree', 6),
        ('2010', 'VLAD', 4.5),
        ('2010', 'Fisher Vector', 3),
        ('2011', 'Sparse Coding', 1.5),
    ]

    for year, method, y in methods_timeline:
        ax.plot(2, y, 'o', color='C0', markersize=10)
        ax.text(2.5, y, year, fontsize=9, va='center', color='C0', weight='bold')
        ax.text(4, y, method, fontsize=10, va='center')

    ax.set_title('Evolution of Visual Recognition Methods\n(Bag-of-Words Era)',
                fontsize=10)

    # Draw timeline line
    ax.plot([2, 2], [1.5, 9], 'k-', linewidth=1, alpha=0.5)

    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/spm_pmk_theory.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: spm_pmk_theory.png")


if __name__ == '__main__':
    import os
    os.makedirs('docs/note/CVDL/pictures', exist_ok=True)

    print("Generating additional illustrations for Visual Recognition I...")
    plot_harris_math()
    plot_vlad_fisher_math()
    plot_spm_pmk_theory()
    print("\nAll additional illustrations generated successfully!")
