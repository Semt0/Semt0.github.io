"""Generate key explanatory figures for Diffusion Policy paper reading notes."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

OUT = 'docs/blog/pictures/diffusion_policy'


def fig1_policy_representations():
    """Figure 1: Three types of policy representations - Explicit, Implicit, Diffusion."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # (a) Explicit Policy
    ax = axes[0]
    ax.set_title("(a) Explicit Policy", fontweight='bold', fontsize=13)
    ax.set_xlabel("Action a")
    ax.set_ylabel("p(a|o)")

    # Draw bimodal distribution
    x = np.linspace(-4, 4, 200)
    p1 = 0.5 * np.exp(-(x + 1.5)**2 / 0.3)
    p2 = 0.5 * np.exp(-(x - 1.5)**2 / 0.3)
    ax.plot(x, p1 + p2, 'b-', linewidth=2, label='True distribution')

    # GMM fit (biased to one mode)
    gmm_fit = 0.7 * np.exp(-(x + 0.3)**2 / 0.5) + 0.3 * np.exp(-(x + 1.5)**2 / 0.6)
    ax.plot(x, gmm_fit, 'r--', linewidth=1.5, label='GMM fit (mode bias)')

    # Discrete bins
    bins = np.linspace(-4, 4, 15)
    p_binned = p1 + p2
    bin_vals = np.array([np.mean(p_binned[(x >= bins[i]) & (x < bins[i+1])]) for i in range(len(bins)-1)])
    ax.bar((bins[:-1] + bins[1:]) / 2, bin_vals, width=0.5, alpha=0.3, color='gray', label='Discretized')

    ax.legend(fontsize=9)
    ax.text(0.5, -0.25, "GMM / Categorical / Discretized", transform=ax.transAxes,
            ha='center', fontsize=10, style='italic', color='gray')

    # (b) Implicit Policy (EBM)
    ax = axes[1]
    ax.set_title("(b) Implicit Policy (EBM)", fontweight='bold', fontsize=13)
    ax.set_xlabel("Action a")
    ax.set_ylabel("E(a, o)")

    x_e = np.linspace(-4, 4, 200)
    # Energy function with two minima
    energy = 0.3*(x_e + 1.5)**2 * (x_e - 1.5)**2 + 0.5*np.sin(3*x_e)
    ax.plot(x_e, energy, 'b-', linewidth=2, label='Energy $E_\\theta(a, o)$')
    ax.scatter([-1.5, 1.5], [0, 0.5], c='red', s=100, zorder=5, marker='v', label='Local minima')

    # Gradient arrows
    for x0 in [-2.5, 0, 2.5]:
        idx = np.argmin(np.abs(x_e - x0))
        grad = (energy[idx+1] - energy[idx-1]) / (x_e[1] - x_e[0])
        ax.arrow(x0, energy[idx], -0.15*grad, -0.15*grad, head_width=0.2, head_length=0.1, fc='green', ec='green', alpha=0.6)

    ax.legend(fontsize=9)
    ax.text(0.5, -0.25, "Learn energy, optimize at inference (InfoNCE)", transform=ax.transAxes,
            ha='center', fontsize=10, style='italic', color='gray')

    # (c) Diffusion Policy
    ax = axes[2]
    ax.set_title("(c) Diffusion Policy", fontweight='bold', fontsize=13)
    ax.set_xlabel("Action a")
    ax.set_ylabel("t")

    # Show denoising process
    t_steps = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
    colors = plt.cm.Blues(np.linspace(0.3, 1.0, len(t_steps)))

    x_range = np.linspace(-4, 4, 200)
    for i, (t, c) in enumerate(zip(t_steps, colors)):
        sigma = t
        # Mixture of two Gaussians with decreasing noise
        y = 0.5 * np.exp(-(x_range + 1.5)**2 / (2*sigma**2 + 0.2)) / np.sqrt(2*np.pi*(sigma**2+0.1))
        y += 0.5 * np.exp(-(x_range - 1.5)**2 / (2*sigma**2 + 0.2)) / np.sqrt(2*np.pi*(sigma**2+0.1))
        y = y / y.max() * (1 - t*0.5)
        ax.plot(x_range, y + t, color=c, linewidth=1.5, label=f'$k={int((1-t)*100)}$')

    ax.set_ylim(-0.5, 2.0)
    ax.legend(fontsize=8, ncol=3)
    ax.text(0.5, -0.25, "Learn score gradient, iteratively denoise from $\\mathcal{N}(0,I)$", transform=ax.transAxes,
            ha='center', fontsize=10, style='italic', color='gray')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig1_policy_representations.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def fig3_overview():
    """Figure 3: Diffusion Policy Method Overview."""
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))

    # (a) General formulation
    ax = axes[0]
    ax.set_title("(a) General Formulation", fontweight='bold', fontsize=13)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Observation box
    obs_box = mpatches.FancyBboxPatch((1, 5.5), 2, 3, boxstyle="round,pad=0.1",
                                        facecolor='#a8d8ea', edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(obs_box)
    ax.text(2, 7.7, "$\\mathbf{O}_t$\n($T_o$ steps)", ha='center', fontsize=10, fontweight='bold')

    # Arrow
    ax.annotate('', xy=(4.2, 7), xytext=(3.2, 7), arrowprops=dict(arrowstyle='->', lw=2, color='#2c3e50'))

    # Policy box
    policy_box = mpatches.FancyBboxPatch((4.3, 5.5), 2.4, 3, boxstyle="round,pad=0.1",
                                           facecolor='#f8b500', edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(policy_box)
    ax.text(5.5, 7.5, "Diffusion\nPolicy", ha='center', fontsize=11, fontweight='bold')
    ax.text(5.5, 6.3, "$\\epsilon_\\theta$", ha='center', fontsize=10)

    # Arrow out
    ax.annotate('', xy=(7.9, 7), xytext=(6.9, 7), arrowprops=dict(arrowstyle='->', lw=2, color='#2c3e50'))

    # Action box
    act_box = mpatches.FancyBboxPatch((8, 5.5), 2, 3, boxstyle="round,pad=0.1",
                                        facecolor='#a8e6cf', edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(act_box)
    ax.text(9, 7.7, "$\\mathbf{A}_t$\n($T_p$ steps)", ha='center', fontsize=10, fontweight='bold')
    ax.text(9, 6, "(exec $T_a$)", ha='center', fontsize=9, style='italic')

    # Denoising illustration at bottom
    ax.text(3, 3.5, "Noise $\\mathcal{N}(0,I)$", fontsize=9, ha='center', color='#e74c3c')
    ax.annotate('', xy=(4.5, 3.5), xytext=(3.5, 3.5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#e74c3c'))
    ax.text(5.5, 3.5, "$A_t^K \\to A_t^{K-1} \\to \\dots \\to A_t^0$", fontsize=9, ha='center', color='#2c3e50', fontweight='bold')
    ax.annotate('', xy=(7.5, 3.5), xytext=(6.7, 3.5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#27ae60'))
    ax.text(8.5, 3.5, "Action", fontsize=9, ha='center', color='#27ae60', fontweight='bold')

    ax.text(5.5, 2.2, "Closed-loop: re-plan every $T_a$ steps", ha='center', fontsize=9, style='italic', color='gray')

    # (b) CNN-based
    ax = axes[1]
    ax.set_title("(b) CNN-based Diffusion Policy", fontweight='bold', fontsize=13)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Input
    ax.text(5, 9.3, "$A_t^k$ (noisy action)", ha='center', fontsize=10, fontweight='bold', color='#e74c3c')

    # CNN blocks
    for i, y in enumerate([7.5, 5.5, 3.5]):
        cnn_box = mpatches.FancyBboxPatch((2, y-0.8), 6, 1.6, boxstyle="round,pad=0.1",
                                            facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.2)
        ax.add_patch(cnn_box)
        ax.text(5, y, f"1D Temporal Conv {i+1}", ha='center', fontsize=10, fontweight='bold')
        ax.text(5, y-0.4, f"+ FiLM($O_t$, k)", ha='center', fontsize=8, style='italic', color='gray')

    # Observation arrow
    obs_box2 = mpatches.FancyBboxPatch((0, 6.8), 1.2, 1.4, boxstyle="round,pad=0.05",
                                         facecolor='#a8d8ea', edgecolor='#2c3e50', linewidth=1)
    ax.add_patch(obs_box2)
    ax.text(0.6, 7.5, "$O_t$", ha='center', fontsize=10, fontweight='bold')
    ax.annotate('', xy=(1.8, 7.5), xytext=(1.3, 7.5), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2c3e50'))

    # FiLM connections
    for y in [7.5, 5.5, 3.5]:
        ax.plot([1.3, 2], [7.2, y], 'k--', linewidth=0.5, alpha=0.3)

    # Output
    ax.text(5, 1.5, "$\\epsilon_\\theta$ (predicted noise)", ha='center', fontsize=10, fontweight='bold', color='#2980b9')

    # (c) Transformer-based
    ax = axes[2]
    ax.set_title("(c) Transformer-based (Time-series Diffusion)", fontweight='bold', fontsize=13)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Input tokens
    for i in range(5):
        color = '#e74c3c' if i == 0 else '#f39c12'
        label = 'k' if i == 0 else f'a{i}'
        tok_box = mpatches.FancyBboxPatch((1 + i*1.6, 8.3), 1.3, 1.0, boxstyle="round,pad=0.05",
                                            facecolor=color, edgecolor='#2c3e50', linewidth=1, alpha=0.7)
        ax.add_patch(tok_box)
        ax.text(1.65 + i*1.6, 8.8, label, ha='center', fontsize=9, color='white', fontweight='bold')

    ax.text(4.5, 7.8, "Input Tokens", ha='center', fontsize=9, style='italic', color='gray')

    # Transformer block
    for y_offset in [0, 2.5]:
        tf_box = mpatches.FancyBboxPatch((1, 4.5 - y_offset), 7, 2, boxstyle="round,pad=0.1",
                                           facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.2)
        ax.add_patch(tf_box)
        ax.text(4.5, 6.2 - y_offset, "Transformer Decoder Block", ha='center', fontsize=10, fontweight='bold')
        ax.text(4.5, 5.5 - y_offset, "Self-Attn (causal) + Cross-Attn($O_t$) + FFN", ha='center', fontsize=8.5)
        ax.text(4.5, 4.9 - y_offset, "+ FiLM($k$)", ha='center', fontsize=8, style='italic', color='gray')

    # Observation cross-attention
    obs_box3 = mpatches.FancyBboxPatch((0.2, 5.0), 1.2, 0.8, boxstyle="round,pad=0.05",
                                         facecolor='#a8d8ea', edgecolor='#2c3e50', linewidth=1)
    ax.add_patch(obs_box3)
    ax.text(0.8, 5.4, "$O_t$", ha='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(0.8, 5.65), xytext=(0.8, 5.6), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2c3e50'))

    # Output
    for i in range(5):
        out_box = mpatches.FancyBboxPatch((1 + i*1.6, 1.5), 1.3, 0.8, boxstyle="round,pad=0.05",
                                            facecolor='#2980b9', edgecolor='#2c3e50', linewidth=1, alpha=0.7)
        ax.add_patch(out_box)
        ax.text(1.65 + i*1.6, 1.9, f'ϵ{i}', ha='center', fontsize=8, color='white', fontweight='bold')
    ax.text(4.5, 1, "Predicted Noise (gradient field)", ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig3_overview.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def fig4_multimodal():
    """Figure 4: Multimodal action distribution handling comparison."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Push-T layout
    for i, (ax, title) in enumerate(zip(axes.flat, ['Diffusion Policy', 'LSTM-GMM', 'IBC', 'BET'])):
        ax.set_title(title, fontweight='bold', fontsize=12)
        ax.set_xlim(-2, 12)
        ax.set_ylim(-2, 12)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        # Draw T-block at bottom
        t_block = mpatches.Rectangle((3.5, 0), 2, 4, linewidth=1.5, edgecolor='#2c3e50', facecolor='#bdc3c7')
        t_top = mpatches.Rectangle((3, 4), 3, 1, linewidth=1.5, edgecolor='#2c3e50', facecolor='#bdc3c7')
        ax.add_patch(t_block)
        ax.add_patch(t_top)
        ax.text(4.5, 3.5, 'T', fontsize=18, fontweight='bold', ha='center', color='#2c3e50')

        # Target
        target = mpatches.Circle((9, 10), 0.6, linewidth=2, edgecolor='#e74c3c', facecolor='none', linestyle='--')
        ax.add_patch(target)
        ax.text(9, 10.8, 'Target', ha='center', fontsize=9, color='#e74c3c')

        # End-effector start
        ax.plot(4.5, 1, 'bs', markersize=10, label='Start')

        if i == 0:  # Diffusion Policy - shows both modes clearly
            # Left path
            xs_l = np.array([4.5, 2, 1, 1.5, 3, 5, 7, 9])
            ys_l = np.array([1, 1.5, 3, 5, 7, 8.5, 9.5, 10])
            ax.plot(xs_l, ys_l, 'b-', linewidth=2, alpha=0.5, label='Mode 1 (left)')
            ax.scatter(xs_l, ys_l, c='blue', s=30, alpha=0.5)

            # Right path
            xs_r = np.array([4.5, 7, 8, 9, 9])
            ys_r = np.array([1, 1.5, 3, 6, 10])
            ax.plot(xs_r, ys_r, 'g-', linewidth=2, alpha=0.5, label='Mode 2 (right)')
            ax.scatter(xs_r, ys_r, c='green', s=30, alpha=0.5)
            ax.legend(fontsize=8, loc='upper left')
            ax.text(4.5, -1.5, "Commits to ONE mode per rollout", ha='center', fontsize=9, color='#27ae60', fontweight='bold')

        elif i == 1:  # LSTM-GMM - biased to one
            xs_l = np.array([4.5, 2, 1.5, 2, 3.5, 5, 7, 9])
            ys_l = np.array([1, 1.5, 3, 5, 7, 8.5, 9.5, 10])
            ax.plot(xs_l, ys_l, 'b-', linewidth=2.5, alpha=0.8)
            ax.scatter(xs_l, ys_l, c='blue', s=30)
            ax.text(4.5, -1.5, "Biased toward one mode", ha='center', fontsize=9, color='#e74c3c', fontweight='bold')

        elif i == 2:  # IBC - biased to one
            xs_r = np.array([4.5, 7, 8, 9, 9])
            ys_r = np.array([1, 1.5, 3, 6, 10])
            ax.plot(xs_r, ys_r, 'g-', linewidth=2.5, alpha=0.8)
            ax.scatter(xs_r, ys_r, c='green', s=30)
            ax.text(4.5, -1.5, "Biased toward one mode", ha='center', fontsize=9, color='#e74c3c', fontweight='bold')

        else:  # BET - mode switching
            xs = np.array([4.5, 2, 7, 1.5, 8, 3, 9])
            ys = np.array([1, 1.5, 1.5, 3, 3.5, 6, 10])
            ax.plot(xs, ys, 'r-', linewidth=2)
            ax.scatter(xs, ys, c='red', s=30)
            ax.text(4.5, -1.5, "Switches between modes (jittery)", ha='center', fontsize=9, color='#e74c3c', fontweight='bold')

    plt.suptitle("Multimodal Action Distribution: Push-T Task", fontweight='bold', fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig4_multimodal.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def fig5_position_vs_velocity():
    """Figure 5: Position vs Velocity Control synergy with Diffusion Policy."""
    fig, ax = plt.subplots(figsize=(10, 6))

    tasks = ['Lift', 'Can', 'Square', 'Transport', 'Tool Hang']
    x = np.arange(len(tasks))
    width = 0.2

    # Simulated data showing trend
    bc_rnn_vel = [85, 80, 55, 40, 25]
    bc_rnn_pos = [60, 45, 25, 15, 10]
    bet_vel = [90, 82, 58, 45, 30]
    bet_pos = [65, 48, 28, 18, 12]
    dp_vel = [92, 85, 62, 55, 40]
    dp_pos = [96, 95, 90, 85, 78]

    ax.bar(x - 1.5*width, bc_rnn_vel, width, color='#e74c3c', alpha=0.7, label='BC-RNN (Vel)')
    ax.bar(x - 0.5*width, bc_rnn_pos, width, color='#e74c3c', alpha=0.3, label='BC-RNN (Pos)')
    ax.bar(x + 0.5*width, bet_vel, width, color='#f39c12', alpha=0.7, label='BET (Vel)')
    ax.bar(x + 1.5*width, bet_pos, width, color='#f39c12', alpha=0.3, label='BET (Pos)')

    ax.set_xticks(x)
    ax.set_xticklabels(tasks, fontsize=12)
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_title('Velocity vs Position Control: BC-RNN & BET degrade, Diffusion Policy improves', fontweight='bold', fontsize=13)
    ax.legend(fontsize=9, ncol=2, loc='upper right')
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3)

    # Add arrow annotations for Diffusion Policy
    dp_data = [96, 95, 90, 85, 78]
    for i, (v, p) in enumerate(zip([92, 85, 62, 55, 40], dp_data)):
        if p > v:
            ax.annotate('', xy=(i + 2.5*width, p), xytext=(i + 2.5*width, v),
                       arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))

    # Legend for DP
    ax.bar(0, 0, 0, color='#27ae60', alpha=0.7, label='DP (Vel)')
    ax.bar(0, 0, 0, color='#27ae60', alpha=0.3, label='DP (Pos)')
    ax.legend(fontsize=9, ncol=2, loc='lower left')

    # DP data points
    for i, (vel, pos) in enumerate(zip([92, 85, 62, 55, 40], dp_data)):
        ax.plot(i - 0.25, vel, 'D', color='#27ae60', markersize=8, alpha=0.7)
        ax.plot(i + 0.25, pos, 'D', color='#27ae60', markersize=8, alpha=0.3)
        ax.text(i + 0.25, pos + 2, str(pos), ha='center', fontsize=8, fontweight='bold', color='#27ae60')

    ax.text(2, 105, 'DP leverages position control advantage', ha='center', fontsize=11, style='italic', color='#27ae60', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig5_position_vs_velocity.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def fig6_ablation():
    """Figure 6: Ablation study - action horizon and latency robustness."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: Action horizon trade-off
    ax1.set_title("Action Horizon $T_a$ Trade-off", fontweight='bold', fontsize=13)
    tasks_short = ['Lift', 'Can', 'Square']
    T_a_values = [1, 2, 4, 8, 16]

    # Simulated data
    perf = {
        'Lift': [72, 85, 96, 92, 60],
        'Can': [65, 80, 95, 88, 55],
        'Square': [55, 72, 90, 85, 48],
    }

    x = np.arange(len(T_a_values))
    width = 0.25
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    for i, (task, c) in enumerate(zip(tasks_short, colors)):
        ax1.bar(x + i*width, perf[task], width, color=c, alpha=0.7, label=task)

    ax1.set_xticks(x + width)
    ax1.set_xticklabels(T_a_values, fontsize=11)
    ax1.set_xlabel('Action Execution Horizon $T_a$', fontsize=12)
    ax1.set_ylabel('Success Rate (%)', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(0, 110)

    # Add annotation
    ax1.axvspan(-0.5, 2.5, alpha=0.05, color='green')
    ax1.text(1, 108, 'Optimal: $T_a$ = 2-4\n(consistency + responsiveness)',
             ha='center', fontsize=10, fontweight='bold', color='#27ae60')

    # Right: Latency robustness
    ax2.set_title("Latency Robustness (Position Control)", fontweight='bold', fontsize=13)
    latency_steps = [0, 1, 2, 3, 4, 5]

    dp_pos = [95, 94, 93, 91, 88, 82]
    dp_vel = [85, 78, 65, 48, 32, 18]
    bc_rnn_pos = [55, 48, 38, 28, 18, 10]

    ax2.plot(latency_steps, dp_pos, 'o-', color='#27ae60', linewidth=2.5, markersize=8, label='DP (Position)')
    ax2.plot(latency_steps, dp_vel, 's-', color='#e74c3c', linewidth=2.5, markersize=8, label='DP (Velocity)')
    ax2.plot(latency_steps, bc_rnn_pos, '^--', color='#7f8c8d', linewidth=2, markersize=7, label='BC-RNN (Position)')

    ax2.set_xlabel('Latency (steps from last obs to first action)', fontsize=12)
    ax2.set_ylabel('Success Rate (%)', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 110)

    ax2.text(2.5, 98, 'DP + Position control: graceful degradation', fontsize=10, fontweight='bold', color='#27ae60', ha='center')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig6_ablation.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def fig7_training_stability():
    """Figure 7: Training stability comparison - IBC vs Diffusion Policy."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: Training loss curves
    ax1.set_title("Training Loss Stability", fontweight='bold', fontsize=13)
    steps = np.arange(0, 2000, 5)

    # IBC - spiky
    np.random.seed(42)
    ibc_loss = 0.5 * np.exp(-steps/800) + 0.15 + 0.08 * np.sin(steps/30) * np.exp(-steps/1500)
    ibc_loss += np.random.randn(len(steps)) * 0.03
    # Add sudden spikes
    spike_locs = [300, 600, 850, 1200, 1600]
    for loc in spike_locs:
        idx = np.argmin(np.abs(steps - loc))
        ibc_loss[max(0, idx-1):min(len(steps), idx+3)] += np.random.uniform(0.1, 0.3)

    ax1.plot(steps, ibc_loss, 'r-', linewidth=1, alpha=0.7, label='IBC (InfoNCE)')

    # Diffusion Policy - smooth
    dp_loss = 0.6 * np.exp(-steps/500) + 0.05 + 0.02 * np.sin(steps/200)
    dp_loss += np.random.randn(len(steps)) * 0.005
    ax1.plot(steps, dp_loss, 'b-', linewidth=1.5, alpha=0.8, label='Diffusion Policy (MSE)')

    ax1.set_xlabel('Training Steps', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    ax1.text(1000, 0.45, 'Spikes → unstable training\n→ hard checkpoint selection',
             fontsize=10, color='#e74c3c', fontweight='bold')
    ax1.text(1000, 0.15, 'Smooth → stable training\n→ reliable checkpoint',
             fontsize=10, color='#2980b9', fontweight='bold')

    # Right: Evaluation stability
    ax2.set_title("Eval Success Rate across Checkpoints", fontweight='bold', fontsize=13)
    checkpoints = np.arange(1, 21)

    np.random.seed(123)
    ibc_eval = 55 + np.random.randn(20) * 18
    ibc_eval = np.clip(ibc_eval, 10, 90)
    dp_eval = 70 + np.cumsum(np.random.randn(20) * 1.5) + 15
    dp_eval = np.clip(dp_eval, 60, 95)

    ax2.plot(checkpoints, ibc_eval, 'ro-', linewidth=1.5, markersize=6, alpha=0.7, label='IBC')
    ax2.plot(checkpoints, dp_eval, 'bo-', linewidth=2, markersize=6, label='Diffusion Policy')
    ax2.axhline(y=np.mean(dp_eval), color='blue', linestyle='--', alpha=0.5, label=f'DP mean = {np.mean(dp_eval):.0f}%')
    ax2.axhline(y=np.mean(ibc_eval), color='red', linestyle='--', alpha=0.5, label=f'IBC mean = {np.mean(ibc_eval):.0f}%')

    ax2.set_xlabel('Checkpoint #', fontsize=12)
    ax2.set_ylabel('Success Rate (%)', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 110)

    ax2.text(10, 10, 'IBC oscillates wildly → need hardware eval for EVERY checkpoint\nDP stable → pick last checkpoint',
             ha='center', fontsize=10, color='#2c3e50', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig7_training_stability.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


if __name__ == '__main__':
    print("Generating Diffusion Policy figures...")
    fig1_policy_representations()
    print("  ✓ fig1_policy_representations.png")
    fig3_overview()
    print("  ✓ fig3_overview.png")
    fig4_multimodal()
    print("  ✓ fig4_multimodal.png")
    fig5_position_vs_velocity()
    print("  ✓ fig5_position_vs_velocity.png")
    fig6_ablation()
    print("  ✓ fig6_ablation.png")
    fig7_training_stability()
    print("  ✓ fig7_training_stability.png")
    print("Done!")
