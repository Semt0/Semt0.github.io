import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc, FancyBboxPatch
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def plot_power_method_convergence():
    """Plot showing power method convergence principle"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot eigenvalues on complex plane
    lambda1 = 5.0  # dominant eigenvalue
    lambda2 = 2.0  # second eigenvalue
    lambda3 = 0.5  # third eigenvalue

    # Draw real axis
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.5, linewidth=1)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.5, linewidth=1)

    # Plot eigenvalues
    ax.plot(lambda1, 0, 'ro', markersize=15, label=r'$\lambda_1 = 5.0$ (dominant)')
    ax.plot(lambda2, 0, 'go', markersize=12, label=r'$\lambda_2 = 2.0$')
    ax.plot(lambda3, 0, 'bo', markersize=10, label=r'$\lambda_3 = 0.5$')

    # Add circles showing magnitudes
    circle1 = plt.Circle((0, 0), lambda1, fill=False, color='red', linestyle='--', alpha=0.5)
    circle2 = plt.Circle((0, 0), lambda2, fill=False, color='green', linestyle='--', alpha=0.5)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    # Add ratio annotation
    ax.annotate('', xy=(4.5, 1.5), xytext=(2.5, 1.5),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
    ax.text(3.5, 1.8, r'$\frac{\lambda_2}{\lambda_1} = 0.4$', fontsize=14, color='purple', ha='center')

    ax.annotate('', xy=(4.5, -1.5), xytext=(0.5, -1.5),
                arrowprops=dict(arrowstyle='<->', color='orange', lw=2))
    ax.text(2.5, -1.2, r'$\frac{\lambda_3}{\lambda_1} = 0.1$', fontsize=14, color='orange', ha='center')

    ax.set_xlim(-1, 7)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.set_xlabel('Real Axis', fontsize=12)
    ax.set_ylabel('Imaginary Axis', fontsize=12)
    ax.set_title('Power Method Convergence: Dominant Eigenvalue Principle', fontsize=14)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/power_method_convergence.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_power_method_iteration():
    """Plot showing power method iteration process"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Iteration process
    iterations = np.arange(0, 8)
    lambda_approx = [1.0, 3.0, 5.28571, 5.37838, 5.37187, 5.37232, 5.37232, 5.37229]
    true_value = 5.37228

    ax1.plot(iterations, lambda_approx, 'bo-', markersize=8, linewidth=2, label='Estimated $\\lambda_1$')
    ax1.axhline(y=true_value, color='r', linestyle='--', label='True value $\\approx 5.37228$')

    ax1.set_xlabel('Iteration k', fontsize=12)
    ax1.set_ylabel(r'$\lambda_1^{(k)}$', fontsize=12)
    ax1.set_title('Power Method: Convergence to Dominant Eigenvalue', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 6)

    # Right: Error convergence
    errors = np.abs(np.array(lambda_approx) - true_value)
    ax2.semilogy(iterations, errors, 'ro-', markersize=8, linewidth=2)
    ax2.set_xlabel('Iteration k', fontsize=12)
    ax2.set_ylabel('Error $|\\lambda_1^{(k)} - \\lambda_1|$', fontsize=12)
    ax2.set_title('Exponential Convergence (Semi-log Plot)', fontsize=13)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/power_method_iteration.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_jacobi_rotation():
    """Plot showing Jacobi rotation for 2x2 matrix"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Original matrix visualization
    theta = np.linspace(0, 2*np.pi, 100)
    # Ellipse representing A = [[4, 2], [2, 3]]
    A = np.array([[4, 2], [2, 3]])

    # Generate ellipse points
    points = np.array([np.cos(theta), np.sin(theta)])
    ellipse = A @ points

    ax1.plot(ellipse[0], ellipse[1], 'b-', linewidth=2, label=r'$x^T A x = 1$')
    ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

    # Eigenvector directions
    eigvals, eigvecs = np.linalg.eig(A)
    for i, (val, vec) in enumerate(zip(eigvals, eigvecs.T)):
        color = 'red' if i == 0 else 'green'
        ax1.arrow(0, 0, vec[0]*2, vec[1]*2, head_width=0.2, head_length=0.2,
                 fc=color, ec=color, linewidth=2, label=f'$v_{i+1}$')

    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')
    ax1.set_title('Symmetric Matrix: Ellipse and Eigenvectors', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

    # Right: Jacobi rotation
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(-5, 5)
    ax2.set_aspect('equal')

    # Draw rotated ellipse (diagonalized)
    D = np.diag(eigvals)
    ellipse_diag = D @ points

    ax2.plot(ellipse_diag[0], ellipse_diag[1], 'b-', linewidth=2, label=r'$x^T D x = 1$')
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

    # Coordinate axes are now aligned with eigenvectors
    ax2.arrow(0, 0, 2.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=2)
    ax2.arrow(0, 0, 0, 2, head_width=0.2, head_length=0.2, fc='green', ec='green', linewidth=2)
    ax2.text(2.7, 0.2, r'$\lambda_1$', fontsize=12, color='red')
    ax2.text(0.2, 2.2, r'$\lambda_2$', fontsize=12, color='green')

    ax2.set_title('After Jacobi Rotation: Diagonal Form', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/jacobi_rotation.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_shifted_power_method():
    """Plot showing origin shift acceleration"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Eigenvalues
    lambda1 = 6.1
    lambda2 = 4.2
    lambda3 = -0.7

    # Plot original eigenvalues
    x_offset = 0
    ax.plot(lambda1, 1, 'ro', markersize=15, label=r'$\lambda_1 = 6.1$')
    ax.plot(lambda2, 1, 'go', markersize=12, label=r'$\lambda_2 = 4.2$')
    ax.plot(lambda3, 1, 'bo', markersize=10, label=r'$\lambda_3 = -0.7$')

    # Shift
    shift = 1.9
    ax.plot(lambda1 - shift, 0, 'r^', markersize=12, label=r'$\lambda_1 - \lambda_0 = 4.2$')
    ax.plot(lambda2 - shift, 0, 'g^', markersize=10, label=r'$\lambda_2 - \lambda_0 = 2.3$')
    ax.plot(lambda3 - shift, 0, 'b^', markersize=8, label=r'$\lambda_3 - \lambda_0 = -2.6$')

    # Arrows showing shift
    for lam, color in [(lambda1, 'red'), (lambda2, 'green'), (lambda3, 'blue')]:
        ax.annotate('', xy=(lam - shift, 0.1), xytext=(lam, 0.9),
                   arrowprops=dict(arrowstyle='->', color=color, alpha=0.6, lw=1.5))

    # Show ratios
    orig_ratio = abs(lambda2 / lambda1)
    shifted_ratio = abs((lambda2 - shift) / (lambda1 - shift))

    ax.text(5, 1.5, f'Original ratio: $|\\lambda_2/\\lambda_1| = {orig_ratio:.3f}$',
            fontsize=11, color='purple', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.text(5, 1.2, f'After shift: $|\\lambda_2-\\lambda_0|/|\\lambda_1-\\lambda_0| = {shifted_ratio:.3f}$',
            fontsize=11, color='darkgreen', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    ax.set_xlim(-4, 8)
    ax.set_ylim(-0.5, 2)
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.3, label='Original')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3, label='Shifted')
    ax.axvline(x=shift, color='orange', linestyle=':', alpha=0.7, label=r'Shift $\lambda_0 = 1.9$')

    ax.set_xlabel('Real Axis', fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Shifted', 'Original'])
    ax.set_title('Origin Shift Acceleration Principle', fontsize=14)
    ax.legend(loc='upper left', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/shifted_power_method.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_deflation_method():
    """Plot showing deflation method concept"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot eigenvalue spectrum
    eigenvalues = [6.1, 4.2, 2.5, -0.7, -1.3]
    colors = ['red', 'green', 'blue', 'orange', 'purple']

    for i, (lam, color) in enumerate(zip(eigenvalues, colors)):
        ax.plot(lam, 1, 'o', markersize=15, color=color)
        ax.text(lam, 1.15, f'$\\lambda_{i+1}={lam}$', ha='center', fontsize=11)

    # Strike through first eigenvalue
    ax.plot([eigenvalues[0]-0.3, eigenvalues[0]+0.3], [1, 1], 'k-', linewidth=3)

    # Arrow indicating deflation
    ax.annotate('Deflation: Remove $\\lambda_1$ and its eigenvector',
               xy=(eigenvalues[0], 0.6), xytext=(3, 0.6),
               arrowprops=dict(arrowstyle='->', color='black', lw=2),
               fontsize=12, ha='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax.set_xlim(-2, 8)
    ax.set_ylim(0.3, 1.5)
    ax.set_xlabel('Eigenvalue magnitude', fontsize=12)
    ax.set_yticks([1])
    ax.set_yticklabels(['Spectrum'])
    ax.set_title('Deflation Method: Computing Subsequent Eigenvalues', fontsize=14)
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/deflation_method.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_inverse_power_method():
    """Plot showing inverse power method concept"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Original eigenvalues
    eigenvalues = [6.1, 4.2, 2.5, -0.7, -1.3]
    inverse_eigenvalues = [1/lam for lam in eigenvalues]

    # Plot original (top)
    for lam in eigenvalues:
        ax.plot(lam, 1, 'bo', markersize=10)
    ax.axhline(y=1, color='blue', alpha=0.3, label='Original: A')

    # Plot inverse (bottom) - note smallest becomes largest
    for lam in inverse_eigenvalues:
        ax.plot(lam, 0, 'ro', markersize=10)
    ax.axhline(y=0, color='red', alpha=0.3, label='Inverse: $A^{-1}$')

    # Highlight smallest eigenvalue becomes dominant
    ax.plot(eigenvalues[-1], 1, 'go', markersize=15, label=f'Smallest: $\\lambda_n={eigenvalues[-1]}$')
    ax.plot(inverse_eigenvalues[-1], 0, 'go', markersize=15, label=f'Becomes dominant: $1/\\lambda_n={inverse_eigenvalues[-1]:.2f}$')

    # Arrows
    ax.annotate('', xy=(inverse_eigenvalues[-1], -0.1), xytext=(eigenvalues[-1], 0.9),
               arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax.set_xlim(-2, 8)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel('Value', fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Inverse $A^{-1}$', 'Original $A$'])
    ax.set_title('Inverse Power Method: Finding Smallest Eigenvalue', fontsize=14)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig('docs/note/计算方法/pictures/inverse_power_method.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


if __name__ == '__main__':
    plot_power_method_convergence()
    print("Generated: power_method_convergence.png")

    plot_power_method_iteration()
    print("Generated: power_method_iteration.png")

    plot_jacobi_rotation()
    print("Generated: jacobi_rotation.png")

    plot_shifted_power_method()
    print("Generated: shifted_power_method.png")

    plot_deflation_method()
    print("Generated: deflation_method.png")

    plot_inverse_power_method()
    print("Generated: inverse_power_method.png")

    print("\nAll eigenvalue method plots generated successfully!")
