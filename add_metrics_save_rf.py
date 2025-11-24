import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/Random_Forest.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell = nb['cells'][12]
source = cell['source']

already_added = False
for line in source:
    if "rf_metrics.csv" in line:
        already_added = True
        break

if not already_added:
    new_code = [
        "\n",
        "# Save metrics to CSV\n",
        "output_dir = Path(\"../../reports/metrics\")\n",
        "output_dir.mkdir(parents=True, exist_ok=True)\n",
        "metrics_rf_df.to_csv(output_dir / \"rf_metrics.csv\", index=False)\n",
        "print(f\"Metrics saved to {output_dir / 'rf_metrics.csv'}\")\n"
    ]
    cell['source'].extend(new_code)
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Random_Forest.ipynb modified.")
else:
    print("Random_Forest.ipynb already has save code.")
