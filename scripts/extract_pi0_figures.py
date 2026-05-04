"""Extract key figures from the π0 paper PDF."""
from pathlib import Path

import fitz

pdf_path = Path("/tmp/pi0.pdf")
out_dir = Path("/Users/semt0/blog/Semt0.github.io/docs/blog/pictures/pi0")
out_dir.mkdir(parents=True, exist_ok=True)

zoom = 6.0
mat = fitz.Matrix(zoom, zoom)

doc = fitz.open(pdf_path)

# Key figures to extract (0-based page index):
# Page 1: Fig 1 - Architecture overview (page 0)
# Page 2: Fig 2 - Laundry folding (page 1)
# Page 3: Fig 3 - Framework overview (page 2)
# Page 5: Fig 5 - Robot platforms (page 4)
# Page 5: Fig 6 - Out-of-box eval tasks (page 4) - actually page 6
# Page 7: Fig 7 - Out-of-box results chart (page 6)
# Page 8: Fig 8 - Language evaluation tasks (page 7)
# Page 9: Fig 9 - Language evaluation results (page 8)
# Page 10: Fig 10 - Fine-tuning tasks (page 9)
# Page 11: Fig 11 - Fine-tuning results (page 10)
# Page 12: Fig 12 - Complex multi-stage tasks (page 11)
# Page 13: Fig 13 - Post-training results (page 12)

pages_to_extract = {
    0: "fig1_architecture_overview",
    1: "fig2_laundry_folding",
    2: "fig3_framework_overview",
    4: "fig5_robot_platforms",
    6: "fig7_out_of_box_results",
    7: "fig8_language_eval_tasks",
    8: "fig9_language_eval_results",
    9: "fig10_finetuning_tasks",
    10: "fig11_finetuning_results",
    11: "fig12_complex_tasks",
    12: "fig13_post_training_results",
    14: "fig14_timestep_sampling",
}

for page_idx, name in pages_to_extract.items():
    if page_idx < len(doc):
        page = doc[page_idx]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = out_dir / f"{name}.png"
        pix.save(out_path)
        print(f"Extracted page {page_idx} -> {out_path}")
    else:
        print(f"Page {page_idx} out of range, skipping")

doc.close()
print("Done!")
