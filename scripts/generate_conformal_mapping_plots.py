import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def plot_conformal_angle():
    """Plot diagram illustrating angle preservation in conformal mapping."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left plot: z-plane
    ax = axes[0]
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(r'$z$-plane', fontsize=14)

    # Center point z0
    ax.plot(1, 1, 'ko', markersize=8)

    # Two curves intersecting at z0
    # Curve 1: along real axis direction
    t1 = np.linspace(0, 1, 50)
    z1 = 1 + t1 * np.exp(1j * 0)  # along positive real direction
    ax.plot(z1.real, z1.imag, 'b-', linewidth=2, label=r'$C_1$')

    # Curve 2: at 45 degree angle
    z2 = 1 + t1 * np.exp(1j * np.pi/4)
    ax.plot(z2.real, z2.imag, 'r-', linewidth=2, label=r'$C_2$')

    # Angle arc
    arc = mpatches.Arc((1, 1), 0.4, 0.4, angle=0, theta1=0, theta2=45)
    ax.add_patch(arc)
    ax.text(1.25, 1.2, r'$\alpha$', fontsize=12)

    # Direction arrows
    ax.annotate('', xy=(1.6, 1.0), xytext=(1.1, 1.0),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(1.5, 1.4), xytext=(1.1, 1.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

    ax.text(1.05, 0.95, r'$z_0$', fontsize=12)
    ax.legend(loc='upper left')

    # Remove axis ticks but keep frame
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Right plot: w-plane
    ax = axes[1]
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(r'$w$-plane', fontsize=14)

    # Center point w0 = f(z0)
    ax.plot(1.5, 1, 'ko', markersize=8)

    # Mapped curves (angle preserved, rotated)
    t1 = np.linspace(0, 1, 50)
    w1 = 1.5 + t1 * np.exp(1j * np.pi/6)  # rotated to 30 degrees
    ax.plot(w1.real, w1.imag, 'b-', linewidth=2, label=r'$\Gamma_1$')

    w2 = 1.5 + t1 * np.exp(1j * np.pi/6 + np.pi/4)  # still 45 degree angle difference
    ax.plot(w2.real, w2.imag, 'r-', linewidth=2, label=r'$\Gamma_2$')

    # Angle arc
    arc = mpatches.Arc((1.5, 1), 0.4, 0.4, angle=0, theta1=30, theta2=75)
    ax.add_patch(arc)
    ax.text(1.75, 1.2, r'$\alpha$', fontsize=12)

    # Direction arrows
    ax.annotate('', xy=(1.9, 1.3), xytext=(1.6, 1.1),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(1.85, 1.6), xytext=(1.6, 1.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

    ax.text(1.55, 0.95, r'$w_0$', fontsize=12)
    ax.legend(loc='upper left')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Arrow between plots
    ax.annotate('', xy=(0.85, 1.5), xytext=(1.55, 1.5),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='->', lw=2))
    ax.text(1.2, 1.55, r'$w = f(z)$', fontsize=12, transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig('docs/note/复变函数/pictures/conformal_angle.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == '__main__':
    plot_conformal_angle()
