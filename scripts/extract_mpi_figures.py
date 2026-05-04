"""Extract key slides from MPI lecture PDFs as note figures."""
from pathlib import Path

import fitz

repo_root = Path(__file__).resolve().parent.parent
out_dir = repo_root / "docs" / "note" / "并行程序设计" / "pictures"
out_dir.mkdir(parents=True, exist_ok=True)

zoom = 6.0
mat = fitz.Matrix(zoom, zoom)

# PDF 22: MPI点对点通讯 — key pages
pdf22 = Path.home() / "Downloads" / "22-MPI点对点通讯_20260427_49.pdf"
key_pages_22 = {
    # Cover / overview
    1: "p2p_cover",
    3: "p2p_parallel_models",
    5: "p2p_mpi_overview",
    7: "p2p_communicator",
    9: "p2p_first_mpi_program",
    11: "p2p_send_recv_basics",
    13: "p2p_send_recv_semantics",
    16: "p2p_communication_modes",
    19: "p2p_buffered_mode",
    22: "p2p_deadlock",
    25: "p2p_nonblocking_intro",
    28: "p2p_wait_test",
    32: "p2p_communication_patterns",
    37: "p2p_safety",
    42: "p2p_summary",
    47: "p2p_example_matrix_vector",
}

doc = fitz.open(pdf22)
for page_idx, name in key_pages_22.items():
    p = doc[page_idx - 1]  # 0-based
    pix = p.get_pixmap(matrix=mat, alpha=False)
    pix.save(out_dir / f"{name}.png")
    print(f"  Saved {name}.png (page {page_idx})")
doc.close()

# PDF 23: MPI集合通讯 — key pages
pdf23 = Path.home() / "Downloads" / "23-MPI集合通讯_20260427_44.pdf"
key_pages_23 = {
    1: "collective_cover",
    3: "collective_overview",
    5: "collective_barrier",
    8: "collective_bcast",
    12: "collective_scatter",
    15: "collective_gather",
    18: "collective_allgather",
    21: "collective_alltoall",
    24: "collective_reduce",
    28: "collective_allreduce",
    31: "collective_scan",
    34: "collective_comm_management",
    37: "collective_topology",
    40: "collective_io",
    43: "collective_summary",
}

doc = fitz.open(pdf23)
for page_idx, name in key_pages_23.items():
    p = doc[page_idx - 1]
    pix = p.get_pixmap(matrix=mat, alpha=False)
    pix.save(out_dir / f"{name}.png")
    print(f"  Saved {name}.png (page {page_idx})")
doc.close()

print("Done extracting MPI figures.")
