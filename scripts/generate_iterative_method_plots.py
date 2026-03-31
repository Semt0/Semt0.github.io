#!/usr/bin/env python3
"""
Generate illustrations for iterative methods note.
Using English labels for better compatibility.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc, FancyBboxPatch, Circle, Ellipse
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def plot_iteration_process():
    """Plot 1: Iteration process flow diagram"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(5, 5.5, 'Iterative Method Flow', fontsize=16, ha='center', fontweight='bold')

    # Boxes
    boxes = [
        (2, 4, 'Initialize\n$x^{(0)}$', '#E3F2FD'),
        (5, 4, 'Compute Iteration\n$x^{(k+1)} = Mx^{(k)} + g$', '#E8F5E9'),
        (8, 4, 'Check Convergence\n$\\|x^{(k+1)} - x^{(k)}\\| < \\varepsilon?$', '#FFF3E0'),
        (8, 2, 'End Iteration\nOutput $x^*$', '#FFEBEE'),
    ]

    for x, y, text, color in boxes:
        rect = FancyBboxPatch((x-1, y-0.5), 2, 1, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=10)

    # Arrows
    arrows = [
        ((3, 4), (4, 4), 'k = 0'),
        ((6, 4), (7, 4), 'Compute'),
        ((8, 3.5), (8, 2.5), 'Yes'),
        ((7, 4), (5, 3), 'No\n(k -> k+1)'),
        ((5, 3), (5, 4), ''),
    ]

    for start, end, label in arrows:
        if start == (7, 4) and end == (5, 3):
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color='#666', lw=1.5,
                                      connectionstyle='arc3,rad=-0.3'))
            ax.text(6, 3.3, label, ha='center', fontsize=9, color='#666')
        elif start == (5, 3) and end == (5, 4):
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
        else:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color='#333', lw=2))
            if label:
                mid_x = (start[0] + end[0]) / 2
                mid_y = (start[1] + end[1]) / 2
                ax.text(mid_x, mid_y + 0.15, label, ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/iteration_flow.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: iteration_flow.png")

def plot_jacobi_vs_gauss_seidel():
    """Plot 2: Jacobi vs Gauss-Seidel comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    n = 5

    # Jacobi
    ax1.set_title('Jacobi Iteration', fontsize=14, fontweight='bold')
    ax1.set_xlim(-0.5, n-0.5)
    ax1.set_ylim(-0.5, 2.5)

    for i in range(n):
        circle_old = plt.Circle((i, 1.5), 0.3, color='#64B5F6', ec='#1976D2', linewidth=2)
        ax1.add_patch(circle_old)
        ax1.text(i, 1.5, f'$x_{i+1}^{{(k)}}$', ha='center', va='center', fontsize=10)

        circle_new = plt.Circle((i, 0.3), 0.3, color='#81C784', ec='#388E3C', linewidth=2)
        ax1.add_patch(circle_new)
        ax1.text(i, 0.3, f'$x_{i+1}^{{(k+1)}}$', ha='center', va='center', fontsize=10)

        ax1.annotate('', xy=(i, 0.7), xytext=(i, 1.1),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    ax1.text(2, 2.2, 'Update all components simultaneously\n(using all old values)', ha='center', fontsize=10)
    ax1.axis('off')

    # Gauss-Seidel
    ax2.set_title('Gauss-Seidel Iteration', fontsize=14, fontweight='bold')
    ax2.set_xlim(-0.5, n-0.5)
    ax2.set_ylim(-0.5, 3.5)

    for i in range(n):
        y_pos = 2.8 - i * 0.5

        if i == 0:
            for j in range(n):
                circle = plt.Circle((j, y_pos + 0.5), 0.2, color='#BBDEFB', ec='#1976D2', linewidth=1)
                ax2.add_patch(circle)
        else:
            for j in range(i):
                circle = plt.Circle((j, y_pos + 0.5), 0.2, color='#C8E6C9', ec='#388E3C', linewidth=1)
                ax2.add_patch(circle)
            for j in range(i, n):
                circle = plt.Circle((j, y_pos + 0.5), 0.2, color='#BBDEFB', ec='#1976D2', linewidth=1)
                ax2.add_patch(circle)

        circle_curr = plt.Circle((i, y_pos), 0.25, color='#81C784', ec='#388E3C', linewidth=2)
        ax2.add_patch(circle_curr)
        ax2.text(i, y_pos, f'$x_{i+1}^{{(k+1)}}$', ha='center', va='center', fontsize=9)

    ax2.text(2, 3.2, 'Sequential update, using latest values', ha='center', fontsize=10)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/jacobi_vs_gauss_seidel.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: jacobi_vs_gauss_seidel.png")

def plot_steepest_descent_path():
    """Plot 3: Steepest descent zigzag path"""
    fig, ax = plt.subplots(figsize=(9, 7))

    x = np.linspace(-2, 2, 100)
    y = np.linspace(-1, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X**2 + 10*Y**2)

    contours = ax.contour(X, Y, Z, levels=15, colors='#90A4AE', linewidths=0.8, alpha=0.7)
    ax.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')

    points_sd = [(1.5, 0.8)]
    x_curr, y_curr = 1.5, 0.8

    for _ in range(8):
        grad_x, grad_y = x_curr, 10*y_curr
        alpha = (grad_x**2 + grad_y**2) / (grad_x**2 + 10*grad_y**2)
        x_new = x_curr - alpha * grad_x
        y_new = y_curr - alpha * grad_y
        points_sd.append((x_new, y_new))
        x_curr, y_curr = x_new, y_new

    xs_sd, ys_sd = zip(*points_sd)
    ax.plot(xs_sd, ys_sd, 'o-', color='#E53935', linewidth=2, markersize=6,
            label='Steepest Descent', zorder=5)

    for i in range(len(points_sd)-1):
        mid_x = (points_sd[i][0] + points_sd[i+1][0]) / 2
        mid_y = (points_sd[i][1] + points_sd[i+1][1]) / 2
        dx = points_sd[i+1][0] - points_sd[i][0]
        dy = points_sd[i+1][1] - points_sd[i][1]
        ax.annotate('', xy=(mid_x + dx*0.1, mid_y + dy*0.1),
                   xytext=(mid_x - dx*0.1, mid_y - dy*0.1),
                   arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5))

    ax.plot(0, 0, '*', color='#FFD700', markersize=15, markeredgecolor='#FF8F00',
            markeredgewidth=2, label='Minimum', zorder=10)

    ax.set_xlabel('$x_1$', fontsize=12)
    ax.set_ylabel('$x_2$', fontsize=12)
    ax.set_title('Steepest Descent "Zigzag" Convergence Path', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/steepest_descent_zigzag.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: steepest_descent_zigzag.png")

def plot_cg_vs_sd():
    """Plot 4: Conjugate gradient vs Steepest descent"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    x = np.linspace(-2, 2, 100)
    y = np.linspace(-1, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X**2 + 10*Y**2)

    for ax, title, color, points_data in [
        (ax1, 'Steepest Descent (Many Iterations)', '#E53935', 'sd'),
        (ax2, 'Conjugate Gradient (2 Steps for 2D)', '#43A047', 'cg')
    ]:
        contours = ax.contour(X, Y, Z, levels=10, colors='#90A4AE', linewidths=0.8, alpha=0.7)

        if points_data == 'sd':
            points = [(1.5, 0.8)]
            x_curr, y_curr = 1.5, 0.8
            for _ in range(15):
                grad_x, grad_y = x_curr, 10*y_curr
                alpha = (grad_x**2 + grad_y**2) / (grad_x**2 + 10*grad_y**2)
                x_new = x_curr - alpha * grad_x
                y_new = y_curr - alpha * grad_y
                if abs(x_new - x_curr) < 0.001 and abs(y_new - y_curr) < 0.001:
                    break
                points.append((x_new, y_new))
                x_curr, y_curr = x_new, y_new
        else:
            points = [(1.5, 0.8), (0, 0)]

        xs, ys = zip(*points)
        ax.plot(xs, ys, 'o-', color=color, linewidth=2.5, markersize=7,
                label='Iteration Path', zorder=5)

        for i, (px, py) in enumerate(points):
            offset = 0.08 if py >= 0 else -0.15
            ax.text(px + 0.1, py + offset, f'{i}', fontsize=9,
                   bbox=dict(boxstyle='circle', facecolor='white', edgecolor=color, alpha=0.8))

        ax.plot(0, 0, '*', color='#FFD700', markersize=15, markeredgecolor='#FF8F00',
                markeredgewidth=2, label='Minimum', zorder=10)

        ax.set_xlabel('$x_1$', fontsize=12)
        ax.set_ylabel('$x_2$', fontsize=12)
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/cg_vs_sd_comparison.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: cg_vs_sd_comparison.png")

def plot_sor_omega_effect():
    """Plot 5: Effect of relaxation factor omega"""
    fig, ax = plt.subplots(figsize=(10, 6))

    iterations = np.arange(0, 50)

    omega_values = [0.5, 0.8, 1.0, 1.2, 1.5]
    colors = ['#E53935', '#FB8C00', '#43A047', '#1E88E5', '#8E24AA']
    labels = [r'$\\omega = 0.5$ (Under-relaxation)', r'$\\omega = 0.8$', 
              r'$\\omega = 1.0$ (Gauss-Seidel)', r'$\\omega = 1.2$ (Over-relaxation)', 
              r'$\\omega = 1.5$']

    for omega, color, label in zip(omega_values, colors, labels):
        if omega < 1:
            rate = 0.8 + 0.1 * (1 - omega)
        elif omega == 1:
            rate = 0.7
        elif omega < 1.5:
            rate = 0.7 - 0.3 * (omega - 1)
        else:
            rate = 0.95

        error = np.exp(-iterations * (1-rate)) + 1e-15
        if omega == 1.5:
            error = np.exp(iterations * 0.02) * 1e-3

        ax.semilogy(iterations, error, color=color, linewidth=2.5, label=label)

    ax.axhline(y=1e-10, color='#666', linestyle='--', linewidth=1, alpha=0.7, label='Convergence Threshold')
    ax.set_xlabel('Iteration Count', fontsize=12)
    ax.set_ylabel('Error (log scale)', fontsize=12)
    ax.set_title('Effect of Relaxation Factor ω on Convergence', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(0, 50)
    ax.set_ylim(1e-12, 1)

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/sor_omega_effect.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: sor_omega_effect.png")

def plot_a_conjugate_directions():
    """Plot 6: A-conjugate directions visualization"""
    fig, ax = plt.subplots(figsize=(9, 7))

    theta = np.linspace(0, 2*np.pi, 100)
    a, b = 2, 1
    x_ellipse = a * np.cos(theta)
    y_ellipse = b * np.sin(theta)

    ax.fill(x_ellipse, y_ellipse, alpha=0.15, color='#64B5F6', label='Contour Interior')
    ax.plot(x_ellipse, y_ellipse, color='#1976D2', linewidth=2, label='Contour Line')

    d1_start = (-1.5, -0.75)
    d1_end = (1.5, 0.75)
    ax.annotate('', xy=d1_end, xytext=d1_start,
               arrowprops=dict(arrowstyle='->', color='#E53935', lw=3))
    ax.text(1.7, 0.9, r'$d^{(0)}$', fontsize=14, color='#E53935', fontweight='bold')

    d2_start = (-1, 0.5)
    d2_end = (1, -0.5)
    ax.annotate('', xy=d2_end, xytext=d2_start,
               arrowprops=dict(arrowstyle='->', color='#43A047', lw=3))
    ax.text(1.2, -0.7, r'$d^{(1)}$', fontsize=14, color='#43A047', fontweight='bold')

    ax.plot(0, 0, '*', color='#FFD700', markersize=18, markeredgecolor='#FF8F00',
            markeredgewidth=2, label='Center (Solution)', zorder=10)

    ax.text(0, -1.8, r'A-conjugate: $\\langle d^{(0)}, Ad^{(1)} \\rangle = 0$',
           ha='center', fontsize=13, style='italic',
           bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FBC02D', alpha=0.9))

    ax.set_xlabel('$x_1$', fontsize=12)
    ax.set_ylabel('$x_2$', fontsize=12)
    ax.set_title('Geometric Meaning of A-Conjugate Directions', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.5, 2.5)

    plt.tight_layout()
    plt.savefig('/Users/semt0/blog/Semt0.github.io/docs/note/计算方法/pictures/a_conjugate_directions.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated: a_conjugate_directions.png")

if __name__ == '__main__':
    print("Generating illustrations for iterative methods...")
    plot_iteration_process()
    plot_jacobi_vs_gauss_seidel()
    plot_steepest_descent_path()
    plot_cg_vs_sd()
    plot_sor_omega_effect()
    plot_a_conjugate_directions()
    print("\nAll illustrations generated successfully!")
