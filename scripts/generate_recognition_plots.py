"""
Generate illustrations for Visual Recognition I notes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def plot_bow_pipeline():
    """Visual Bag-of-Words pipeline diagram."""
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(7, 5.5, 'Visual Bag-of-Words Pipeline', fontsize=16, weight='bold', ha='center')

    # Step boxes
    steps = [
        (1, 2.5, 'Interest\nPoint\nDetection', '#E3F2FD'),
        (4, 2.5, 'Local\nFeature\nExtraction', '#E8F5E9'),
        (7, 2.5, 'Feature\nQuantization', '#FFF3E0'),
        (10, 2.5, 'Histogram\nAggregation', '#FCE4EC'),
        (12.5, 2.5, 'Image\nRepresentation', '#F3E5F5'),
    ]

    for x, y, text, color in steps:
        box = FancyBboxPatch((x-0.8, y-0.8), 1.6, 1.6,
                            boxstyle="round,pad=0.05,rounding_size=0.1",
                            facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', weight='bold')

    # Arrows
    for i in range(4):
        x_start = 1.8 + i * 3
        x_end = 3.2 + i * 3 if i < 3 else 11.7
        arrow = FancyArrowPatch((x_start, 2.5), (x_end, 2.5),
                               arrowstyle='->', mutation_scale=20, linewidth=2, color='#555')
        ax.add_patch(arrow)

    # Examples below each step
    examples = [
        (1, 1.2, 'Harris / DoG', '#E3F2FD'),
        (4, 1.2, 'SIFT 128-d', '#E8F5E9'),
        (7, 1.2, 'K-means\nClustering', '#FFF3E0'),
        (10, 1.2, 'BoW\nHistogram', '#FCE4EC'),
        (12.5, 1.2, 'K-dim\nVector', '#F3E5F5'),
    ]

    for x, y, text, color in examples:
        ax.text(x, y, text, fontsize=8, ha='center', va='center',
               style='italic', color='#666',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.5, edgecolor='none'))

    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/bow_pipeline.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: bow_pipeline.png")


def plot_harris_detector():
    """Harris corner detector illustration."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Flat region
    ax = axes[0]
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.ones_like(X) * 128  # Flat image
    ax.imshow(Z, cmap='gray', vmin=0, vmax=255)
    ax.set_title('Flat Region\n(No Change)', fontsize=11, weight='bold')
    ax.axis('off')

    # Edge region
    ax = axes[1]
    Z = np.zeros((100, 100))
    Z[:, :50] = 200
    Z[:, 50:] = 50
    ax.imshow(Z, cmap='gray', vmin=0, vmax=255)
    ax.set_title('Edge\n(Change in one direction)', fontsize=11, weight='bold')
    ax.axis('off')
    # Draw window
    rect = Rectangle((35, 35), 30, 30, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

    # Corner region
    ax = axes[2]
    Z = np.zeros((100, 100))
    Z[:50, :50] = 200
    Z[50:, :50] = 50
    Z[:50, 50:] = 50
    Z[50:, 50:] = 200
    ax.imshow(Z, cmap='gray', vmin=0, vmax=255)
    ax.set_title('Corner\n(Change in all directions)', fontsize=11, weight='bold')
    ax.axis('off')
    # Draw window
    rect = Rectangle((35, 35), 30, 30, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

    fig.suptitle('Harris Corner Detection: Window Shift Analysis', fontsize=13, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/harris_detector.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: harris_detector.png")


def plot_sift_descriptor():
    """SIFT descriptor construction."""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'SIFT Descriptor Construction', fontsize=14, weight='bold', ha='center')

    # Main grid (16x16)
    grid_size = 6
    cell_size = grid_size / 4
    start_x, start_y = 2, 2.5

    # Draw 4x4 sub-regions
    colors = plt.cm.Blues(np.linspace(0.3, 0.8, 16))
    for i in range(4):
        for j in range(4):
            idx = i * 4 + j
            rect = Rectangle((start_x + j*cell_size, start_y + (3-i)*cell_size),
                            cell_size, cell_size,
                            facecolor=colors[idx], edgecolor='black', linewidth=1)
            ax.add_patch(rect)

    # Label
    ax.text(5, start_y - 0.5, '16×16 neighborhood', fontsize=10, ha='center')
    ax.text(5, start_y - 0.9, '→ 4×4 sub-regions', fontsize=9, ha='center', style='italic')

    # Gradient arrows in one cell
    cell_x = start_x + 0.5 * cell_size
    cell_y = start_y + 0.5 * cell_size
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        dx = 0.15 * np.cos(np.radians(angle))
        dy = 0.15 * np.sin(np.radians(angle))
        ax.annotate('', xy=(cell_x + dx, cell_y + dy), xytext=(cell_x, cell_y),
                   arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    ax.text(cell_x, cell_y - 0.5, '8 orientations', fontsize=8, ha='center', color='red')

    # Output vector
    ax.text(8.5, 6, 'Output:', fontsize=11, weight='bold')
    ax.text(8.5, 5.5, '4 × 4 × 8 = 128-d', fontsize=10, ha='center',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    # Scale invariance note
    ax.text(5, 1, 'Scale Invariant: detected at multiple scales via DoG', fontsize=9, ha='center',
           style='italic', color='#666')

    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/sift_descriptor.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: sift_descriptor.png")


def plot_spm_structure():
    """Spatial Pyramid Matching structure."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    levels = [(1, 'Level 0\n1×1'), (2, 'Level 1\n2×2'), (4, 'Level 2\n4×4')]

    for ax, (n, title) in zip(axes, levels):
        # Draw grid
        for i in range(n):
            for j in range(n):
                color = plt.cm.Set3((i * n + j) % 12)
                rect = Rectangle((j/n, i/n), 1/n, 1/n,
                                facecolor=color, edgecolor='black', linewidth=1.5)
                ax.add_patch(rect)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=11, weight='bold')

    fig.suptitle('Spatial Pyramid Matching: Multi-Resolution Grids', fontsize=13, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/spm_structure.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: spm_structure.png")


def plot_pmk_illustration():
    """Pyramid Match Kernel illustration."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    np.random.seed(42)
    # Two point sets
    X = np.random.rand(15, 2) * 0.8 + 0.1
    Y = X + np.random.randn(15, 2) * 0.05  # Slightly perturbed

    levels = [(1, 'Level 0\n(bin size: 1)'),
              (2, 'Level 1\n(bin size: 0.5)'),
              (4, 'Level 2\n(bin size: 0.25)')]

    for ax, (n, title) in zip(axes, levels):
        bin_size = 1.0 / n

        # Draw grid
        for i in range(n):
            for j in range(n):
                rect = Rectangle((j*bin_size, i*bin_size), bin_size, bin_size,
                                fill=False, edgecolor='gray', linewidth=0.8)
                ax.add_patch(rect)

        # Plot points
        ax.scatter(X[:, 0], X[:, 1], c='blue', s=50, marker='o', label='Set X', alpha=0.7, edgecolors='black')
        ax.scatter(Y[:, 0], Y[:, 1], c='red', s=50, marker='s', label='Set Y', alpha=0.7, edgecolors='black')

        # Count matches in each bin
        matches = 0
        for i in range(n):
            for j in range(n):
                x_min, x_max = j*bin_size, (j+1)*bin_size
                y_min, y_max = i*bin_size, (i+1)*bin_size

                count_x = np.sum((X[:, 0] >= x_min) & (X[:, 0] < x_max) &
                                (X[:, 1] >= y_min) & (X[:, 1] < y_max))
                count_y = np.sum((Y[:, 0] >= x_min) & (Y[:, 0] < x_max) &
                                (Y[:, 1] >= y_min) & (Y[:, 1] < y_max))
                matches += min(count_x, count_y)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f'{title}\nMatches: {matches}', fontsize=10, weight='bold')
        ax.legend(loc='upper right', fontsize=7)

    fig.suptitle('Pyramid Match Kernel: Multi-Scale Histogram Matching', fontsize=13, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/pmk_illustration.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: pmk_illustration.png")


def plot_vlad_fisher_comparison():
    """Compare BoW, VLAD, and Fisher Vector aggregation."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # BoW
    ax = axes[0]
    k = 5
    counts = [3, 1, 4, 2, 5]
    colors_bow = plt.cm.Set2(np.linspace(0, 1, k))
    bars = ax.bar(range(k), counts, color=colors_bow, edgecolor='black')
    ax.set_title('BoW: Counting\n(0-order)', fontsize=11, weight='bold')
    ax.set_ylabel('Count', fontsize=10)
    ax.set_xlabel('Visual Word', fontsize=10)
    ax.set_xticks(range(k))
    ax.set_xticklabels([f'w{i}' for i in range(1, k+1)])

    # VLAD
    ax = axes[1]
    residuals = np.random.randn(k, 2) * 0.3
    centers = np.array([[0.2, 0.8], [0.5, 0.5], [0.8, 0.2], [0.3, 0.3], [0.7, 0.7]])

    for i, (c, r) in enumerate(zip(centers, residuals)):
        circle = Circle(c, 0.05, color=colors_bow[i], alpha=0.5)
        ax.add_patch(circle)
        ax.annotate('', xy=(c[0] + r[0], c[1] + r[1]), xytext=c,
                   arrowprops=dict(arrowstyle='->', color=colors_bow[i], lw=2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title('VLAD: Residual Aggregation\n(1-order)', fontsize=11, weight='bold')
    ax.axis('off')

    # Fisher Vector
    axes[2].axis('off')
    text = """
    Fisher Vector:

    • 0-order: weights (π)
    • 1-order: mean gradients
    • 2-order: variance grads

    Captures full GMM
    statistics
    """
    axes[2].text(0.5, 0.5, text, fontsize=10, ha='center', va='center',
                family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    axes[2].set_title('Fisher Vector\n(0+1+2-order)', fontsize=11, weight='bold')

    fig.suptitle('Feature Aggregation Methods Comparison', fontsize=13, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('docs/note/CVDL/pictures/aggregation_comparison.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: aggregation_comparison.png")


if __name__ == '__main__':
    import os
    os.makedirs('docs/note/CVDL/pictures', exist_ok=True)

    print("Generating illustrations for Visual Recognition I...")
    plot_bow_pipeline()
    plot_harris_detector()
    plot_sift_descriptor()
    plot_spm_structure()
    plot_pmk_illustration()
    plot_vlad_fisher_comparison()
    print("\nAll illustrations generated successfully!")
