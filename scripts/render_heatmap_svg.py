import json
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def load_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "contributions.json"
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_svg(data):
    cells = data["cells"]
    summary = data["summary"]

    x0 = 30
    y0 = 20
    cell = 12
    gap = 2

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="860" height="220" viewBox="0 0 860 220" role="img" aria-label="Ram Dhote GitHub contribution graph">',
        '<defs>',
        '  <style>',
        '    .cell { rx: 3; ry: 3; }',
        '    .label { font: 12px "Segoe UI", sans-serif; fill: #c9d1d9; }',
        '    .small { font: 11px "Segoe UI", sans-serif; fill: #8b949e; }',
        '    .stat { font: 600 12px "Segoe UI", sans-serif; fill: #c9d1d9; }',
        '  </style>',
        '</defs>',
        '  <rect width="100%" height="100%" fill="#0d1117"/>',
        '  <text x="30" y="24" class="label">ramdhote05</text>',
        '  <text x="30" y="48" class="small">Contribution activity</text>',
    ]

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, month in enumerate(months):
        x = x0 + i * 56
        svg.append(f'  <text x="{x}" y="76" class="small">{month}</text>')

    cell_index = 0
    for row in range(7):
        for col in range(53):
            if cell_index >= len(cells):
                break
            item = cells[cell_index]
            level = int(item.get("level", "0"))
            color = PALETTE[level]
            x = x0 + col * (cell + gap)
            y = y0 + row * (cell + gap) + 50
            svg.append(f'  <rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color}" />')
            cell_index += 1

    legend_y = 180
    svg.append(f'  <text x="30" y="{legend_y}" class="small">Less</text>')
    for i, c in enumerate(PALETTE):
        x = 75 + i * 16
        svg.append(f'  <rect x="{x}" y="{legend_y - 10}" width="12" height="12" rx="2" fill="{c}" />')
    svg.append(f'  <text x="{75 + len(PALETTE) * 16 + 10}" y="{legend_y}" class="small">More</text>')

    total_contrib = summary.get("total", 0)
    svg.append(f'  <text x="30" y="206" class="stat">{total_contrib:,} contributions in the last year</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def main():
    data = load_data()
    svg = build_svg(data)
    out_path = Path(__file__).resolve().parents[1] / "contrib-heatmap.svg"
    out_path.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
