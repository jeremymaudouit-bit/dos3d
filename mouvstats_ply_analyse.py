import argparse
from pathlib import Path
from datetime import datetime

import numpy as np
import open3d as o3d
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def analyse_ply(input_path: Path):
    pcd = o3d.io.read_point_cloud(str(input_path))
    pts = np.asarray(pcd.points)
    if pts.size == 0:
        raise ValueError("Le fichier PLY ne contient aucun point exploitable.")

    mins = pts.min(axis=0)
    maxs = pts.max(axis=0)
    dims = maxs - mins
    center = pts.mean(axis=0)

    return {
        "nb_points": int(len(pts)),
        "min_x": float(mins[0]),
        "min_y": float(mins[1]),
        "min_z": float(mins[2]),
        "max_x": float(maxs[0]),
        "max_y": float(maxs[1]),
        "max_z": float(maxs[2]),
        "dim_x": float(dims[0]),
        "dim_y": float(dims[1]),
        "dim_z": float(dims[2]),
        "center_x": float(center[0]),
        "center_y": float(center[1]),
        "center_z": float(center[2]),
    }


def make_pdf(stats, input_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = out_dir / f"rapport_mouvstats_ply_{stamp}.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    y = height - 2 * cm
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y, "MouvStats - Rapport PLY")

    y -= 1.2 * cm
    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, y, f"Fichier analysé : {input_path.name}")

    y -= 0.8 * cm
    c.drawString(2 * cm, y, f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y -= 1.2 * cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "Statistiques du nuage de points")

    y -= 0.8 * cm
    c.setFont("Helvetica", 11)
    lines = [
        f"Nombre de points : {stats['nb_points']}",
        f"Dimensions X/Y/Z : {stats['dim_x']:.3f} / {stats['dim_y']:.3f} / {stats['dim_z']:.3f}",
        f"Centre X/Y/Z : {stats['center_x']:.3f} / {stats['center_y']:.3f} / {stats['center_z']:.3f}",
        f"Min X/Y/Z : {stats['min_x']:.3f} / {stats['min_y']:.3f} / {stats['min_z']:.3f}",
        f"Max X/Y/Z : {stats['max_x']:.3f} / {stats['max_y']:.3f} / {stats['max_z']:.3f}",
    ]

    for line in lines:
        c.drawString(2 * cm, y, line)
        y -= 0.6 * cm

    y -= 0.8 * cm
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(2 * cm, y, "Version test : ce rapport vérifie le chargement PLY. L'analyse clinique complète sera intégrée ensuite.")

    c.save()
    return pdf_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Fichier .ply à analyser")
    parser.add_argument("--out", required=True, help="Dossier de sortie")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out)

    stats = analyse_ply(input_path)
    pdf_path = make_pdf(stats, input_path, out_dir)
    print(f"PDF généré : {pdf_path}")


if __name__ == "__main__":
    main()
