import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/XGBOOST.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# We know it's cell 8 from previous inspection
cell = nb['cells'][8]
source = cell['source']

# Check if we already added the save code
already_added = False
for line in source:
    if "xgboost_metrics.csv" in line:
        already_added = True
        break

if not already_added:
    new_code = [
        "\n",
        "# Save metrics to CSV\n",
        "output_dir = Path(\"../../reports/metrics\")\n",
        "output_dir.mkdir(parents=True, exist_ok=True)\n",
        "res_df.to_csv(output_dir / \"xgboost_metrics.csv\", index=False)\n",
        "print(f\"Metrics saved to {output_dir / 'xgboost_metrics.csv'}\")\n"
    ]
    cell['source'].extend(new_code)
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("XGBOOST.ipynb modified.")
else:
    print("XGBOOST.ipynb already has save code.")
