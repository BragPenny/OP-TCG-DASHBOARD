import json
import requests

# Master product list containing both Sealed and Singles datasets
FALLBACK_CATALOG = [
    {
        "id": "OP01-BOX",
        "name": "Romance Dawn Booster Box (OP-01)",
        "category": "sealed",
        "set": "OP-01",
        "globalUsd": 220.00,
        "stores": {"Solarpop": 3800, "LevelUp": 3950, "BigBang": 4100, "Mirage": 3900}
    },
    {
        "id": "OP02-BOX",
        "name": "Paramount War Booster Box (OP-02)",
        "category": "sealed",
        "set": "OP-02",
        "globalUsd": 145.00,
        "stores": {"Solarpop": 2800, "LevelUp": 3100, "BigBang": 3400, "Mirage": 3000}
    },
    {
        "id": "OP03-BOX",
        "name": "Pillars of Strength Booster Box (OP-03)",
        "category": "sealed",
        "set": "OP-03",
        "globalUsd": 125.00,
        "stores": {"Solarpop": 2400, "LevelUp": 2650, "BigBang": 2900}
    },
    {
        "id": "OP04-BOX",
        "name": "Kingdoms of Intrigue Booster Box (OP-04)",
        "category": "sealed",
        "set": "OP-04",
        "globalUsd": 115.00,
        "stores": {"Solarpop": 2200, "LevelUp": 2450, "BigBang": 2700}
    },
    {
        "id": "OP05-BOX",
        "name": "Awakening of the New Era Box (OP-05)",
        "category": "sealed",
        "set": "OP-05",
        "globalUsd": 195.00,
        "stores": {"Solarpop": 3800, "LevelUp": 4200, "BigBang": 4600}
    },
    {
        "id": "OP06-BOX",
        "name": "Wings of the Captain Booster Box (OP-06)",
        "category": "sealed",
        "set": "OP-06",
        "globalUsd": 140.00,
        "stores": {"Solarpop": 2600, "LevelUp": 2850, "BigBang": 3100}
    },
    {
        "id": "OP07-BOX",
        "name": "500 Years Into the Future Box (OP-07)",
        "category": "sealed",
        "set": "OP-07",
        "globalUsd": 130.00,
        "stores": {"Solarpop": 2500, "LevelUp": 2700, "BigBang": 2950}
    },
    {
        "id": "OP08-BOX",
        "name": "Two Legends Booster Box (OP-08)",
        "category": "sealed",
        "set": "OP-08",
        "globalUsd": 125.00,
        "stores": {"Solarpop": 2400, "LevelUp": 2600, "BigBang": 2800}
    },
    {
        "id": "EB01-BOX",
        "name": "Memorial Collection Extra Booster (EB-01)",
        "category": "sealed",
        "set": "EB-01",
        "globalUsd": 110.00,
        "stores": {"Solarpop": 2100, "LevelUp": 2250, "BigBang": 2400}
    },
    {
        "id": "PRB01-BOX",
        "name": "ONE PIECE CARD THE BEST (PRB-01)",
        "category": "sealed",
        "set": "PRB-01",
        "globalUsd": 180.00,
        "stores": {"Solarpop": 3400, "LevelUp": 3700, "BigBang": 3950}
    },
    {
        "id": "OP01-120",
        "name": "Shanks (Manga Alternate Art)",
        "category": "singles",
        "set": "OP-01",
        "globalUsd": 1100.00,
        "stores": {"LevelUp": 23500, "BigBang": 24000, "Mirage": 22500}
    },
    {
        "id": "OP02-121",
        "name": "Portgas.D.Ace (Manga Alternate Art)",
        "category": "singles",
        "set": "OP-02",
        "globalUsd": 850.00,
        "stores": {"LevelUp": 17500, "BigBang": 18200}
    },
    {
        "id": "OP03-122",
        "name": "Sabo (Manga Alternate Art)",
        "category": "singles",
        "set": "OP-03",
        "globalUsd": 600.00,
        "stores": {"LevelUp": 12500, "BigBang": 13000}
    },
    {
        "id": "OP04-083",
        "name": "Donquixote Doflamingo (SEC Alt)",
        "category": "singles",
        "set": "OP-04",
        "globalUsd": 75.00,
        "stores": {"LevelUp": 1550, "BigBang": 1700}
    },
    {
        "id": "OP05-119",
        "name": "Monkey.D.Luffy (Manga Alternate Art)",
        "category": "singles",
        "set": "OP-05",
        "globalUsd": 2400.00,
        "stores": {"LevelUp": 48000, "BigBang": 51000}
    }
]

def update_catalog():
    print("Updating catalog data...")
    # Write updated dataset directly to catalog.json
    with open("catalog.json", "w") as f:
        json.dump(FALLBACK_CATALOG, f, indent=2)
    print("catalog.json updated successfully.")

if __name__ == "__main__":
    update_catalog()
