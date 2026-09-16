
import shutil
import os


def main(scenario):
    dest = os.path.join("scenarios", scenario)

    # Ensure destination directory exists
    os.makedirs(dest, exist_ok=True)

    files = [
        "cylindrical.pdf",
        "polar_lines.pdf",
        "polar.pdf",
        "sphereical.pdf",
        "str_grph_proj.pdf",
        "all.pdf",
        "stars_&_lines.pdf",
        "borders_&_stars.pdf",
        "borders.pdf",
        "stars.pdf",
        "polar_trying_best.pdf",
        "polar_trying_best.png"

    ]

    for f in files:
        target = os.path.join(dest, f)

        try:
            # If file exists at destination, remove it so move can overwrite
            if os.path.exists(target):
                os.remove(target)

            shutil.move(f, target)
            print(f"Moved {f} → {target}")

        except FileNotFoundError:
            print(f"Skipped (missing): {f}")