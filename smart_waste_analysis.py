import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)

# Ruta completa al archivo
file_path = Path(r"C:\Users\jg436\Downloads\Data_waste_cleaned.xlsx")
df = pd.read_excel(file_path)

#Auditoría de la estructura de los datos 
print(df.head())
print(df.shape)   
print(df.columns)
print(df.info())

#Feature engineering 

#Días de inventario 
Inventory_days = df["InventoryDays"] = df["StockQty"] / df["DailySaleAvg"]
print(f"Días de inventario")
print(Inventory_days)

#Oportunidad de transferencia 
Transfer_opportunity = df["TransferOpportunity"] = (df["StockQty"] > df["AvgDailySaleInNearbyStores"])
print(f"Oportunidades de transferencia a otras tiendas")
print(Transfer_opportunity)

#Riesgo de desperdicio
Waste_risk = df["WasteRisk"] = df["InventoryDays"] > df["DaysUntilExpiry"]
print(f"Riesgo de desperdicio")
print(Waste_risk)

#KPIS 

#Tasa de deterioro 
Waste_risk_rate = df["WasteRisk"].mean()
print(f"Tasa de desperdicio en promedio")
print(Waste_risk_rate)

#Tasa de producto caducado
Spoiled_rate = df.groupby("StoreID") ["IsSpoiled"].mean()
print(f"Tasa de producto caducado")
print(Spoiled_rate)

#Días promedio de inventario 
Avg_inventory_days = df["InventoryDays"] = df["StockQty"] / df["DailySaleAvg"]
print(f"Días promedio de inventario")
print(Avg_inventory_days)

#Días promedio de expiración 
Avg_days_to_expiry = df["AvgDaysToExpiry"] = df["DaysUntilExpiry"].mean()
print(f"Días promedio de expiración")
print(Avg_days_to_expiry)

#Oportunidad de transferencia 
Transfer_opportunity = df["TransferOpportunity"] = (df["WasteRisk"] > 0.5) & (df["AvgDailySaleInNearbyStores"] > df["DailySaleAvg"])
print(f"Oportunidad de transferencia")
print(Transfer_opportunity)

#Emparejamiento de la demanda cercana 
Demand_nearby_match = df["DemandNearbtMatch"] = df["AvgDailySaleInNearbyStores"] >= df["DailySaleAvg"]
print(f"Demanda por aproximación cercana")
print(Demand_nearby_match)

#Velocidad de rotación aproximada 
Inventory_turnover_Proxy = df["InventoryTurnOverProxy"] = df["DailySaleAvg"] / df["StockQty"]
print(f"Velocidad de la rotación de inventario")
print(Inventory_turnover_Proxy)

#Exploración de hallazgos 

#Hallazgo 1

Results_by_category = df.groupby("Category")[["WasteRisk", "InventoryDays", "InventoryTurnOverProxy"]].mean()
print(f"Agrupaciones de valores promedio por categoria de producto")
print(Results_by_category)

# Hallazgo 2 

#Covertir a dataframe SpoilageRate
df["SpoilageRate"] = df["IsSpoiled"]

Results_by_store = df.groupby("StoreID")[["TransferOpportunity", "SpoilageRate"]].mean()
print(f"Agrupaciones de valores promedio por tienda")
print(Results_by_store)

#Hallazgo 3 
Results_by_product = df.groupby("ItemName")[["WasteRisk", "InventoryDays"]].agg(["mean","max","min"])
print(f"Agrupaciones promedio, máximo y mínimo de los productos por riesgo de desperdicio y días de inventario")
print(Results_by_product)

#Productos con alto riesgo de caducar y con movimiento bajo en inventarios 

critical_products = df[(df["WasteRisk"] > 0.5) & (df["InventoryTurnOverProxy"] < 0.2)]
print(f"Productos con riesgo de caducar y tener bajo movimiento")
print(critical_products)

#Transferencias sugeridas 
Transfer_candidates = df[df["TransferOpportunity"] == True]
print(f"Candidatos a transferir")
print(Transfer_candidates)

#Resumen por categoria 

category_summary = df.groupby("Category").agg(
    InventoryDays_mean=("InventoryDays", "mean"),
    WasteRisk_mean=("WasteRisk", "mean"), 
    InventoryTurnover_mean=("InventoryTurnOverProxy", "mean"),
    DaysUntilExpiry_mean=("DaysUntilExpiry", "mean")
).reset_index()

print("Resumen por categoría:")
print(category_summary)

#Resumen por producto 
product_summary = df.groupby("ItemName").agg(
    InventoryDays_mean=("InventoryDays", "mean"),
    InventoryDays_max=("InventoryDays", "max"),
    WasteRisk_mean=("WasteRisk", "mean"), 
    InventoryTurnover_mean=("InventoryTurnOverProxy", "mean"),
    DaysUntilExpiry_mean=("DaysUntilExpiry", "mean")
).reset_index()

print("Resumen por producto:")
print(product_summary)

#Resumen por tienda 
store_summary = df.groupby("StoreLocation").agg(
    InventoryDays_mean=("InventoryDays", "mean"),
    WasteRisk_mean=("WasteRisk", "mean"), 
    InventoryTurnover_mean=("InventoryTurnOverProxy", "mean")
).reset_index()

print("Resumen por tienda:")
print(store_summary)

#Visualizaciones 

import matplotlib.pyplot as plt 


#Top tiendas por inventario 

store_summary = df.groupby("StoreLocation").agg(
    AvgInventoryDays=("InventoryDays", "mean")
).sort_values("AvgInventoryDays", ascending=False)

store_summary.plot(kind="bar", figsize=(10,6))
plt.title("Average inventory days by store")
plt.ylabel("Days")
plt.show()


#KPI Brecha de la demanda 
Demand_gap = df["DemandGapScore"] = (df["AvgDailySaleInNearbyStores"] - df["DailySaleAvg"])
print(f"Brecha de la demanda")
print(Demand_gap)

#KPI Prioridad de la transferencia 
Transfer_priority = df["TransferPriorityScore"] = (df["DemandGapScore"] / (df["DistanceToNearestStore"] + 1)) * df["WasteRisk"]
print(f"Prioridad de trnsferencia acorde riesgo de desperdicio")
print(Transfer_priority)

#KPI Unidades rescatables 

Rescue_units = df["RescuableUnits"] = (
    df["StockQty"] - df["DailySaleAvg"]
).clip(lower=0)
print(f"Unidades rescatables")
print(Rescue_units)

#KPI Desperdicio salvable 
Waste_saved = df["WasteSavedProxy"] = (
    df["RescuableUnits"] * df["WasteRisk"]
)
print("Desperdicio que es salvable")
print(Waste_saved)

#KPI de oportunidades salvables 
Top_opportunities = top_savings = df.sort_values(
    "WasteSavedProxy",
    ascending=False
)[[
    "ItemName",
    "StoreLocation",
    "RescuableUnits",
    "WasteRisk",
    "TransferPriorityScore",
    "WasteSavedProxy"
]].head(15)

print(f"Ranking de oportunidades salvables")
print(Top_opportunities)

#KPI Ahorros totales 
total_savings = df["WasteSavedProxy"].sum()
print(f"Ahorros totales")
print(total_savings)

#Lógica de decisión de negocio 
def recommend_action(row):
    if row["TransferPriorityScore"] > 2:
        return "Transfer"
    elif row["WasteRisk"] > 0.9 and row["DaysUntilExpiry"] <= 1:
        return "Discount"
    elif row["IsSpoiled"]:
        return "Donate"
    else:
        return "Monitor"
        
df["RecommendedAction"] = df.apply(recommend_action, axis=1)

action_summary = df["RecommendedAction"].value_counts()

print("Resumen de acciones recomendadas:")
print(action_summary)



#Top de productos accionables 
top_actions = df[[
    "ItemName",
    "StoreLocation",
    "WasteRisk",
    "InventoryDays",
    "TransferPriorityScore",
    "RecommendedAction"
]].sort_values(
    "TransferPriorityScore",
    ascending=False
).head(20)

print(top_actions)

#What if analysis 
# Copia del DataFrame original
simulation_df = df.copy()

# Selección de los 20 productos con mayor prioridad de transferencia
top_idx = simulation_df[
    simulation_df["RecommendedAction"] == "Transfer"
].nlargest(20, "TransferPriorityScore").index

# Simulación: transferir la mitad del stock de esos productos
simulation_df.loc[top_idx, "StockQty"] = simulation_df.loc[top_idx, "StockQty"] * 0.5

# Recalcular días de inventario después de la transferencia
simulation_df["InventoryDays"] = (
    simulation_df["StockQty"] / simulation_df["DailySaleAvg"]
)

# Riesgo de desperdicio después de la transferencia
simulation_df["PostTransferWasteRisk"] = (
    simulation_df["InventoryDays"] > simulation_df["DaysUntilExpiry"]
)

# Riesgo promedio antes y después
before_risk = df["WasteRisk"].mean()
after_risk = simulation_df["PostTransferWasteRisk"].mean()

# Reducción del riesgo
risk_reduction = before_risk - after_risk

print("Riesgo antes:", before_risk)
print("Riesgo después:", after_risk)
print("Reducción de riesgo:", risk_reduction)

# Número de productos en riesgo antes y después
before_savings = df["WasteRisk"].sum()
after_savings = simulation_df["PostTransferWasteRisk"].sum()
saved_products = before_savings - after_savings

print("Productos en riesgo antes:", before_savings)
print("Productos en riesgo después:", after_savings)
print("Productos salvados por la transferencia:", saved_products)


