import streamlit as st
import os
import json
from datetime import datetime

# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory"], key="sidebar_nav")

# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INVENTORY_FILE = "inventory.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"

# --- Recipe Database ---
recipes = {
    "Creme Brulee": {
        "ingredients": {
            "milk": 20300,
            "cream": 6828,
            "sugar": 4400,
            "guar": 72,
            "dry milk": 2800,
            "yolks": 2400,
            "caramel sauce": 3200
        },
        "instructions": [
            "1) Weigh and mix all base ingredients except caramel sauce.",
            "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
            "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
            "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
            "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
        ],
        "subrecipes": {
            "caramel sauce": {
                "ingredients": {
                    "sugar": 3200,
                    "water": 500,
                    "honey": 50
                },
                "instructions": [
                    "1) Combine sugar, water, and honey.",
                    "2) Cook on medium-high heat until sugar dissolves.",
                    "3) Raise heat and cook until mixture reaches 220°F."
                ]
            }
        }
    },
    "Crumble": {
        "ingredients": {
            "flour": 223,
            "sugar": 388,
            "cinnamon": 8,
            "butter": 272
        },
        "instructions": [
            "1) Melt the butter.",
            "2) Briefly mix ingredients on the mixer, and remove them before they form a homogeneous mix.",
            "3) Bake for 15 minutes at 350°F."
        ],
        "subrecipes": {}
    },
    "Cookie Dough": {
        "ingredients": {
            "butter": 396,
            "sugar": 344,
            "brown sugar": 386,
            "pasteurized egg whites": 92,
            "pasteurized egg yolks": 90,
            "vanilla extract": 16,
            "flour": 646,
            "salt": 6
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Dulce de Leche": {
        "ingredients": {
            "milk": 24775,
            "cream": 7500,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 500,
            "dulce de leche heladero": 90
        },
        "instructions": []
    },
    "Fresh Mint": {
        "ingredients": {
            "milk": 31140,
            "cream": 6500,
            "sugar": 8500,
            "guar": 110,
            "dry milk": 3000,
            "yolks": 750,
            "mint": 1250,
            "blanched mint": 500
        },
        "instructions": [
            "Day 1: Prepare Mint-Infused Milk",
            "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
            "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
            "Day 2: Prepare Blanched Mint Purée",
            "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
            "4) Bring 2 gallons of fresh water to a boil.",
            "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
            "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
            "7) Drain the mint and blend until very fine and smooth.",
            "Final Steps:",
            "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
            "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
        ],
        "subrecipes": {}
    },
    "Graham Cracker Crust": {
        "ingredients": {
            "graham cracker crumble": 338,
            "butter": 310,
            "sugar": 352
        },
        "instructions": [
            "1) Process graham crackers on the Robocoupe.",
            "2) Mix ingredients on the mixer.",
            "3) Press ingredients down on a flat pan.",
            "4) Bake for 15 minutes at 325°F."
        ],
        "subrecipes": {}
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F.",
            "4) Add the baking soda and stir.",
            "5) Pour the rising honeycomb on previously greased trays and let cool."
        ],
        "subrecipes": {}
    },
    "Lemon Bar": {
        "ingredients": {
            "crust": 566,
            "filling": 1362
        },
        "instructions": [
            "1) Bake the crust at 350°F for 15 minutes.",
            "2) Pour filling onto baked crust and bake at 350°F for 20 minutes."
        ],
        "subrecipes": {
            "crust": {
                "ingredients": {
                    "butter": 225,
                    "flour": 240,
                    "sugar": 100,
                    "salt": 1
                },
                "instructions": [
                    "1) Process all crust ingredients in a food processor until smooth.",
                    "2) Press into a greased pan and bake for 15 minutes at 350°F."
                ]
            },
            "filling": {
                "ingredients": {
                    "eggs (each)": 12,
                    "lemon juice": 360,
                    "sugar": 900,
                    "flour": 90
                },
                "instructions": [
                    "1) Beat all filling ingredients in a bowl until fully dissolved.",
                    "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
                ]
            }
        }
    },
    "Lemon Sorbet": {
        "ingredients": {
            "water": 5442,
            "lemon": 3500,
            "pectin": 87,
            "guar gum": 12,
            "sugar": 2625
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Peach Preserves": {
        "ingredients": {
            "peaches": 1350,
            "sugar": 1250,
            "lemon": 82
        },
        "instructions": [
            "1) Combine cored peaches and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Pear Sorbet": {
        "ingredients": {
            "water": 5500,
            "pectin": 100,
            "sugar": 3500,
            "pear": 10600,
            "lemon": 300
        },
        "instructions": [
            "1) Quarter the pears and remove their seeds.",
            "2) Fill a pot with the quartered pears and weigh.",
            "3) Add water to completely cover the pears.",
            "4) Weigh the water + pears in the pot.",
            "5) Cook until pears are soft and translucent.",
            "6) Re-weigh cooked pear+water mix.",
            "7) Add enough water to make up the difference between step 4 and 6.",
            "8) Process all the ingredients in a blender until smooth."
        ],
        "subrecipes": {}
    },
    "Pistachio": {
        "ingredients": {
            "milk": 32640,
            "cream": 750,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2750,
            "yolks": 1000,
            "pistachio paste": 4500
        },
        "instructions": [
            "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
            "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
        ],
        "subrecipes": {
            "pistachio paste": {
                "ingredients": {
                    "roasted pistachios": 2967,
                    "pistachio oil": 1532
                },
                "instructions": [
                    "1) Roast the pistachios if raw.",
                    "2) Blend pistachios with pistachio oil until smooth and creamy."
                ]
            }
        }
    },
    "Strawberry Preserves": {
        "ingredients": {
            "strawberries": 1250,
            "sugar": 1150,
            "pectin": 11,
            "lemon": 89
        },
        "instructions": [
            "1) Combine strawberries and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Toffee": {
        "ingredients": {
            "butter": 863,
            "sugar": 779,
            "honey": 17,
            "salt": 4
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F."
        ],
        "subrecipes": {}
    },
    "vanilla": {
        "ingredients": {
            "milk": 28510,
            "cream": 10000,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2500,
            "yolks": 500,
            "vanilla extract": 100,
            "vanilla seeds": 90
        },
        "instructions": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
        ]
    }
}
# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Ingredient Inventory Section ---
def ingredient_inventory_section():
    st.subheader("📦 Ingredient Inventory Control")

    bulk_units = {
        "milk": "gallons",
        "cream": "half gallons",
        "sugar": "50 lb bags",
        "dry milk": "50 lb bags",
        "flour": "50 lb bags",
        "brown sugar": "50 lb bags",
        "butter": "cases"
    }

    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())
    all_ingredients = sorted(set(all_ingredients))

    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect("Select ingredients to exclude", all_ingredients, default=excluded_ingredients, key="exclude_list")
    if st.button("Save Exclusion List", key="save_exclude_btn"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    ingredient_inventory = {}
    min_thresholds = {}

    st.markdown("#### Enter Inventory and Minimum Thresholds")
    for ing in all_ingredients:
        if ing in exclude_list:
            continue
        unit = bulk_units.get(ing, "grams")
        col1, col2 = st.columns(2)
        with col1:
            qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
        with col2:
            threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
        ingredient_inventory[ing] = {"amount": qty, "unit": unit}
        min_thresholds[ing] = threshold

    if st.button("Save Ingredient Inventory", key="save_inventory_btn"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: f"{v['amount']} {v['unit']}" for k, v in data.items() if k not in exclude_list}
        st.dataframe(filtered_data, use_container_width=True)

    if os.path.exists(THRESHOLD_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)
        with open(THRESHOLD_FILE) as f:
            thresholds = json.load(f)
        needs_order = {
            ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
            for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
        }
        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order)
        else:
            st.success("✅ All ingredients above minimum thresholds.")

# --- Batching System Section ---
def batching_system_section():
    st.subheader("⚙️ Manual Batching System")
    recipe_name = st.selectbox("Select Recipe", list(recipes.keys()), key="batch_recipe_select")
    recipe = recipes[recipe_name]

    st.markdown("### Scale by Target Weight")
    target_weight = st.number_input("Target total weight (grams)", min_value=100.0, step=100.0, key="batch_target_weight")
    if target_weight:
        scaled_recipe, factor = scale_recipe_to_target_weight(recipe, target_weight)
        st.markdown(f"#### Scaled Ingredients ({round(factor * 100)}%)")
        for ing, amt in scaled_recipe["ingredients"].items():
            st.write(f"- {amt} grams {ing}")

    st.markdown("### Step-by-Step Mode")
    if "step_i" not in st.session_state:
        st.session_state.step_i = 0

    if st.button("Start Over", key="reset_step_btn"):
        st.session_state.step_i = 0

    steps = list(scaled_recipe["ingredients"].items())
    if st.session_state.step_i < len(steps):
        ing, amt = steps[st.session_state.step_i]
        st.markdown(f"**Weigh:** {amt} grams of {ing}")
        if st.button("Next Ingredient", key=f"next_{st.session_state.step_i}"):
            st.session_state.step_i += 1
    else:
        st.success("🎉 All ingredients completed!")

# # --- Flavor Inventory Placeholder ---
# def flavor_inventory_section():
#     st.subheader("📋 Flavor Inventory Section")
#     st.info("This section is not yet implemented.")

def flavor_inventory_section():
    st.subheader("📋 Flavor Inventory Section")
    st.write("Placeholder content.")


# --- Routing ---
if page == "Ingredient Inventory":
    ingredient_inventory_section()
elif page == "Batching System":
    batching_system_section()
elif page == "Flavor Inventory":
    flavor_inventory_section()

# # --- Utility Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Ingredient Inventory Section ---
# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())
#     all_ingredients = sorted(set(all_ingredients))  # de-duplicate and sort

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", all_ingredients, default=excluded_ingredients, key="exclude_list")
#     if st.button("Save Exclusion List", key="save_exclude_btn"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in all_ingredients:
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory", key="save_inventory_btn"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         filtered_data = {k: f"{v['amount']} {v['unit']}" for k, v in data.items() if k not in exclude_list}
#         st.dataframe(filtered_data, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#         if needs_order:
#             st.error("⚠️ Order Needed:")
#             st.dataframe(needs_order)
#         else:
#             st.success("✅ All ingredients above minimum thresholds.")

# # --- Routing Logic ---
# if page == "Ingredient Inventory":
#     ingredient_inventory_section()

# elif page == "Flavor Inventory":
#     st.subheader("📋 Flavor Inventory Section")
#     st.info("This section is not yet implemented.")

# elif page == "Batching System":
#     st.subheader("⚙️ Batching System Section")
#     st.info("This section is not yet implemented.")
# # --- Utility Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Ingredient Inventory Section ---
# def ingredient_inventory_section():
#     st.subheader("\U0001F4E6 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients, key="exclude_list")
#     if st.button("Save Exclusion List", key="save_exclusion"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in sorted(all_ingredients):
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory", key="save_inventory"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         filtered_data = {k: f"{v['amount']} {v['unit']}" for k, v in data.items() if k not in exclude_list}
#         st.dataframe(filtered_data, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#         if needs_order:
#             st.error("\u26A0\uFE0F Order Needed:")
#             st.dataframe(needs_order)
#         else:
#             st.success("\u2705 All ingredients above minimum thresholds.")

# # --- Page Router ---
# if page == "Ingredient Inventory":
#     ingredient_inventory_section()

# # --- Utility Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Recipe Adjuster Section ---
# # ... (no changes here for brevity) ...

# # --- Ingredient Inventory Section ---
# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
#     if st.button("Save Exclusion List"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in sorted(all_ingredients):
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
#         st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#         if needs_order:
#             st.error("⚠️ Order Needed:")
#             st.dataframe(needs_order)
#         else:
#             st.success("✅ All ingredients above minimum thresholds.")

# # --- Utility Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Recipe Adjuster Section ---
# def recipe_adjuster_section():
#     st.title("Ice Cream Recipe Adjuster")
#     selected = st.selectbox("Choose a recipe", list(recipes.keys()))
#     recipe = recipes[selected]

#     st.subheader("Choose how you want to scale the recipe:")
#     scale_mode = st.selectbox("Scaling method", ["Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans", "Available ingredient amounts"])

#     target_weight = None
#     scaled_recipe = None

#     if scale_mode == "Total weight (grams)":
#         w = st.text_input("Enter target total weight (g)", "")
#         if w.strip():
#             try:
#                 target_weight = float(w)
#             except ValueError:
#                 st.error("Enter a valid number for total weight")

#     elif scale_mode == "1.5 gallon tubs":
#         tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#         target_weight = tubs * 4275

#     elif scale_mode == "5 liter pans":
#         pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#         target_weight = pans * 3750

#     elif scale_mode == "Mix of tubs and pans":
#         tubs = st.number_input("Tubs", min_value=0, step=1)
#         pans = st.number_input("Pans", min_value=0, step=1)
#         target_weight = tubs * 4275 + pans * 3750

#     if target_weight:
#         scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)

#     if scale_mode == "Available ingredient amounts":
#         st.subheader("Enter available ingredient amounts (g):")
#         available_inputs = {}
#         for ing in recipe["ingredients"]:
#             val = st.text_input(f"{ing}", "")
#             if val.strip():
#                 try:
#                     available_inputs[ing] = float(val)
#                 except ValueError:
#                     st.error(f"Invalid input for {ing}")

#         if st.button("Adjust Recipe Based on Ingredients"):
#             adjusted, limit_scale = adjust_recipe_with_constraints(recipe, available_inputs)
#             st.session_state.adjusted_recipe = adjusted
#             st.session_state.adjusted_total = round(sum(adjusted.values()))
#             st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
#             st.subheader("Final Adjusted Recipe:")
#             for ing, amt in adjusted.items():
#                 st.write(f"{ing}: {amt} g")

#     if scaled_recipe:
#         st.markdown("---")
#         st.success(f"Scaled recipe to {round(target_weight)} g")
#         st.subheader("Scaled Ingredients")
#         for ing, amt in scaled_recipe["ingredients"].items():
#             st.write(f"• {ing}: {amt} g")

#         if scaled_recipe.get("instructions"):
#             st.subheader("Instructions")
#             for step in scaled_recipe["instructions"]:
#                 st.markdown(f"- {step}")

#         st.markdown("---")
#         st.subheader("🧪 Step-by-Step Weighing")
#         if "step_index" not in st.session_state:
#             st.session_state.step_index = 0

#         if st.button("Start Step-by-Step Mode"):
#             st.session_state.step_index = 0

#         all_ingredients = list(scaled_recipe["ingredients"].items())
#         step = st.session_state.step_index
#         if step < len(all_ingredients):
#             label, amount = all_ingredients[step]
#             st.markdown(f"### {label}: {round(amount)} grams")
#             if st.button("Next"):
#                 st.session_state.step_index += 1
#         else:
#             st.success("✅ All ingredients completed!")
#             if st.button("Restart"):
#                 st.session_state.step_index = 0

# # --- Inventory Functions ---
# def load_inventory_data():
#     if os.path.exists(LINEUP_FILE):
#         with open(LINEUP_FILE) as f:
#             lineup = json.load(f)
#     else:
#         lineup = []

#     if os.path.exists(INVENTORY_FILE):
#         with open(INVENTORY_FILE) as f:
#             inventory = json.load(f)
#     else:
#         inventory = {}

#     return lineup, inventory

# def save_inventory_data(lineup, inventory):
#     with open(LINEUP_FILE, "w") as f:
#         json.dump(lineup, f)
#     with open(INVENTORY_FILE, "w") as f:
#         json.dump(inventory, f)

# # --- Flavor Inventory Section ---
# def flavor_inventory_section():
#     st.subheader("🍦 Flavor & Topping Inventory Control")
#     lineup, inventory = load_inventory_data()

#     st.markdown("#### 1. Set Weekly Flavor Lineup")
#     lineup_input = st.text_area("Flavors (comma-separated)", value=", ".join(lineup), key="lineup_input")
#     if st.button("Update Lineup"):
#         lineup = [flavor.strip() for flavor in lineup_input.split(",") if flavor.strip()]
#         inventory = {flavor: data for flavor, data in inventory.items() if flavor in lineup}
#         save_inventory_data(lineup, inventory)
#         st.success("Lineup updated and inventory cleaned.")

#     st.markdown("#### 2. Update Inventory")
#     if not lineup:
#         st.warning("Please set the weekly lineup first.")
#         return

#     flavor = st.selectbox("Select a flavor to update", lineup, key="flavor_select")
#     quarts = st.number_input("Enter quarts available", min_value=0, step=1, key="quarts_input")

#     if st.button("Submit Inventory"):
#         inventory[flavor] = {
#             "quarts": quarts,
#             "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
#         }
#         save_inventory_data(lineup, inventory)
#         st.success(f"Inventory updated for {flavor}")

#     st.markdown("#### 3. Current Inventory")
#     if inventory:
#         sorted_inventory = sorted(inventory.items(), key=lambda x: x[1]['quarts'], reverse=True)
#         table = {
#             "Flavor": [k for k, _ in sorted_inventory],
#             "Quarts": [v["quarts"] for _, v in sorted_inventory],
#             "Last Updated": [v["last_updated"] for _, v in sorted_inventory],
#         }
#         st.dataframe(table)
#     else:
#         st.info("No inventory records yet.")

# # --- Ingredient Inventory Section ---
# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases",
#         "dulce de leche heladero": "cans",
#         "lemon": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in sorted(all_ingredients):
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in data.items()}, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#        import streamlit as st
import os
import json
from datetime import datetime

# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory"])

# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INVENTORY_FILE = "inventory.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"

# --- Recipe Database ---
recipes = {
    "Creme Brulee": {
        "ingredients": {
            "milk": 20300,
            "cream": 6828,
            "sugar": 4400,
            "guar": 72,
            "dry milk": 2800,
            "yolks": 2400,
            "caramel sauce": 3200
        },
        "instructions": [
            "1) Weigh and mix all base ingredients except caramel sauce.",
            "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
            "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
            "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
            "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
        ],
        "subrecipes": {
            "caramel sauce": {
                "ingredients": {
                    "sugar": 3200,
                    "water": 500,
                    "honey": 50
                },
                "instructions": [
                    "1) Combine sugar, water, and honey.",
                    "2) Cook on medium-high heat until sugar dissolves.",
                    "3) Raise heat and cook until mixture reaches 220°F."
                ]
            }
        }
    },
    "Crumble": {
        "ingredients": {
            "flour": 223,
            "sugar": 388,
            "cinnamon": 8,
            "butter": 272
        },
        "instructions": [
            "1) Melt the butter.",
            "2) Briefly mix ingredients on the mixer, and remove them before they form a homogeneous mix.",
            "3) Bake for 15 minutes at 350°F."
        ],
        "subrecipes": {}
    },
    "Cookie Dough": {
        "ingredients": {
            "butter": 396,
            "sugar": 344,
            "brown sugar": 386,
            "pasteurized egg whites": 92,
            "pasteurized egg yolks": 90,
            "vanilla extract": 16,
            "flour": 646,
            "salt": 6
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Dulce de Leche": {
        "ingredients": {
            "milk": 24775,
            "cream": 7500,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 500,
            "dulce de leche heladero": 90
        },
        "instructions": []
    },
    "Fresh Mint": {
        "ingredients": {
            "milk": 31140,
            "cream": 6500,
            "sugar": 8500,
            "guar": 110,
            "dry milk": 3000,
            "yolks": 750,
            "mint": 1250,
            "blanched mint": 500
        },
        "instructions": [
            "Day 1: Prepare Mint-Infused Milk",
            "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
            "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
            "Day 2: Prepare Blanched Mint Purée",
            "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
            "4) Bring 2 gallons of fresh water to a boil.",
            "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
            "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
            "7) Drain the mint and blend until very fine and smooth.",
            "Final Steps:",
            "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
            "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
        ],
        "subrecipes": {}
    },
    "Graham Cracker Crust": {
        "ingredients": {
            "graham cracker crumble": 338,
            "butter": 310,
            "sugar": 352
        },
        "instructions": [
            "1) Process graham crackers on the Robocoupe.",
            "2) Mix ingredients on the mixer.",
            "3) Press ingredients down on a flat pan.",
            "4) Bake for 15 minutes at 325°F."
        ],
        "subrecipes": {}
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F.",
            "4) Add the baking soda and stir.",
            "5) Pour the rising honeycomb on previously greased trays and let cool."
        ],
        "subrecipes": {}
    },
    "Lemon Bar": {
        "ingredients": {
            "crust": 566,
            "filling": 1362
        },
        "instructions": [
            "1) Bake the crust at 350°F for 15 minutes.",
            "2) Pour filling onto baked crust and bake at 350°F for 20 minutes."
        ],
        "subrecipes": {
            "crust": {
                "ingredients": {
                    "butter": 225,
                    "flour": 240,
                    "sugar": 100,
                    "salt": 1
                },
                "instructions": [
                    "1) Process all crust ingredients in a food processor until smooth.",
                    "2) Press into a greased pan and bake for 15 minutes at 350°F."
                ]
            },
            "filling": {
                "ingredients": {
                    "eggs (each)": 12,
                    "lemon juice": 360,
                    "sugar": 900,
                    "flour": 90
                },
                "instructions": [
                    "1) Beat all filling ingredients in a bowl until fully dissolved.",
                    "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
                ]
            }
        }
    },
    "Lemon Sorbet": {
        "ingredients": {
            "water": 5442,
            "lemon": 3500,
            "pectin": 87,
            "guar gum": 12,
            "sugar": 2625
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Peach Preserves": {
        "ingredients": {
            "peaches": 1350,
            "sugar": 1250,
            "lemon": 82
        },
        "instructions": [
            "1) Combine cored peaches and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Pear Sorbet": {
        "ingredients": {
            "water": 5500,
            "pectin": 100,
            "sugar": 3500,
            "pear": 10600,
            "lemon": 300
        },
        "instructions": [
            "1) Quarter the pears and remove their seeds.",
            "2) Fill a pot with the quartered pears and weigh.",
            "3) Add water to completely cover the pears.",
            "4) Weigh the water + pears in the pot.",
            "5) Cook until pears are soft and translucent.",
            "6) Re-weigh cooked pear+water mix.",
            "7) Add enough water to make up the difference between step 4 and 6.",
            "8) Process all the ingredients in a blender until smooth."
        ],
        "subrecipes": {}
    },
    "Pistachio": {
        "ingredients": {
            "milk": 32640,
            "cream": 750,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2750,
            "yolks": 1000,
            "pistachio paste": 4500
        },
        "instructions": [
            "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
            "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
        ],
        "subrecipes": {
            "pistachio paste": {
                "ingredients": {
                    "roasted pistachios": 2967,
                    "pistachio oil": 1532
                },
                "instructions": [
                    "1) Roast the pistachios if raw.",
                    "2) Blend pistachios with pistachio oil until smooth and creamy."
                ]
            }
        }
    },
    "Strawberry Preserves": {
        "ingredients": {
            "strawberries": 1250,
            "sugar": 1150,
            "pectin": 11,
            "lemon": 89
        },
        "instructions": [
            "1) Combine strawberries and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Toffee": {
        "ingredients": {
            "butter": 863,
            "sugar": 779,
            "honey": 17,
            "salt": 4
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F."
        ],
        "subrecipes": {}
    },
    "vanilla": {
        "ingredients": {
            "milk": 28510,
            "cream": 10000,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2500,
            "yolks": 500,
            "vanilla extract": 100,
            "vanilla seeds": 90
        },
        "instructions": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
        ]
    }
}

# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Recipe Adjuster Section ---
# ... (no changes here for brevity) ...

# --- Ingredient Inventory Section ---
def ingredient_inventory_section():
    st.subheader("📦 Ingredient Inventory Control")

    bulk_units = {
        "milk": "gallons",
        "cream": "half gallons",
        "sugar": "50 lb bags",
        "dry milk": "50 lb bags",
        "flour": "50 lb bags",
        "brown sugar": "50 lb bags",
        "butter": "cases"
    }

    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())

    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
    if st.button("Save Exclusion List"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    ingredient_inventory = {}
    min_thresholds = {}

    st.markdown("#### Enter Inventory and Minimum Thresholds")
    for ing in sorted(all_ingredients):
        if ing in exclude_list:
            continue
        unit = bulk_units.get(ing, "grams")
        col1, col2 = st.columns(2)
        with col1:
            qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
        with col2:
            threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
        ingredient_inventory[ing] = {"amount": qty, "unit": unit}
        min_thresholds[ing] = threshold

    if st.button("Save Ingredient Inventory"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
        st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

    if os.path.exists(THRESHOLD_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)
        with open(THRESHOLD_FILE) as f:
            thresholds = json.load(f)
        needs_order = {
            ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
            for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
        }
        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order)
        else:
            st.success("✅ All ingredients above minimum thresholds.")
import streamlit as st
import os
import json
from datetime import datetime

# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory"])

# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INVENTORY_FILE = "inventory.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"

# --- Recipe Database ---
recipes = {
    "Creme Brulee": {
        "ingredients": {
            "milk": 20300,
            "cream": 6828,
            "sugar": 4400,
            "guar": 72,
            "dry milk": 2800,
            "yolks": 2400,
            "caramel sauce": 3200
        },
        "instructions": [
            "1) Weigh and mix all base ingredients except caramel sauce.",
            "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
            "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
            "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
            "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
        ],
        "subrecipes": {
            "caramel sauce": {
                "ingredients": {
                    "sugar": 3200,
                    "water": 500,
                    "honey": 50
                },
                "instructions": [
                    "1) Combine sugar, water, and honey.",
                    "2) Cook on medium-high heat until sugar dissolves.",
                    "3) Raise heat and cook until mixture reaches 220°F."
                ]
            }
        }
    },
    "Crumble": {
        "ingredients": {
            "flour": 223,
            "sugar": 388,
            "cinnamon": 8,
            "butter": 272
        },
        "instructions": [
            "1) Melt the butter.",
            "2) Briefly mix ingredients on the mixer, and remove them before they form a homogeneous mix.",
            "3) Bake for 15 minutes at 350°F."
        ],
        "subrecipes": {}
    },
    "Cookie Dough": {
        "ingredients": {
            "butter": 396,
            "sugar": 344,
            "brown sugar": 386,
            "pasteurized egg whites": 92,
            "pasteurized egg yolks": 90,
            "vanilla extract": 16,
            "flour": 646,
            "salt": 6
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Dulce de Leche": {
        "ingredients": {
            "milk": 24775,
            "cream": 7500,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 500,
            "dulce de leche heladero": 90
        },
        "instructions": []
    },
    "Fresh Mint": {
        "ingredients": {
            "milk": 31140,
            "cream": 6500,
            "sugar": 8500,
            "guar": 110,
            "dry milk": 3000,
            "yolks": 750,
            "mint": 1250,
            "blanched mint": 500
        },
        "instructions": [
            "Day 1: Prepare Mint-Infused Milk",
            "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
            "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
            "Day 2: Prepare Blanched Mint Purée",
            "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
            "4) Bring 2 gallons of fresh water to a boil.",
            "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
            "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
            "7) Drain the mint and blend until very fine and smooth.",
            "Final Steps:",
            "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
            "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
        ],
        "subrecipes": {}
    },
    "Graham Cracker Crust": {
        "ingredients": {
            "graham cracker crumble": 338,
            "butter": 310,
            "sugar": 352
        },
        "instructions": [
            "1) Process graham crackers on the Robocoupe.",
            "2) Mix ingredients on the mixer.",
            "3) Press ingredients down on a flat pan.",
            "4) Bake for 15 minutes at 325°F."
        ],
        "subrecipes": {}
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F.",
            "4) Add the baking soda and stir.",
            "5) Pour the rising honeycomb on previously greased trays and let cool."
        ],
        "subrecipes": {}
    },
    "Lemon Bar": {
        "ingredients": {
            "crust": 566,
            "filling": 1362
        },
        "instructions": [
            "1) Bake the crust at 350°F for 15 minutes.",
            "2) Pour filling onto baked crust and bake at 350°F for 20 minutes."
        ],
        "subrecipes": {
            "crust": {
                "ingredients": {
                    "butter": 225,
                    "flour": 240,
                    "sugar": 100,
                    "salt": 1
                },
                "instructions": [
                    "1) Process all crust ingredients in a food processor until smooth.",
                    "2) Press into a greased pan and bake for 15 minutes at 350°F."
                ]
            },
            "filling": {
                "ingredients": {
                    "eggs (each)": 12,
                    "lemon juice": 360,
                    "sugar": 900,
                    "flour": 90
                },
                "instructions": [
                    "1) Beat all filling ingredients in a bowl until fully dissolved.",
                    "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
                ]
            }
        }
    },
    "Lemon Sorbet": {
        "ingredients": {
            "water": 5442,
            "lemon": 3500,
            "pectin": 87,
            "guar gum": 12,
            "sugar": 2625
        },
        "instructions": [],
        "subrecipes": {}
    },
    "Peach Preserves": {
        "ingredients": {
            "peaches": 1350,
            "sugar": 1250,
            "lemon": 82
        },
        "instructions": [
            "1) Combine cored peaches and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Pear Sorbet": {
        "ingredients": {
            "water": 5500,
            "pectin": 100,
            "sugar": 3500,
            "pear": 10600,
            "lemon": 300
        },
        "instructions": [
            "1) Quarter the pears and remove their seeds.",
            "2) Fill a pot with the quartered pears and weigh.",
            "3) Add water to completely cover the pears.",
            "4) Weigh the water + pears in the pot.",
            "5) Cook until pears are soft and translucent.",
            "6) Re-weigh cooked pear+water mix.",
            "7) Add enough water to make up the difference between step 4 and 6.",
            "8) Process all the ingredients in a blender until smooth."
        ],
        "subrecipes": {}
    },
    "Pistachio": {
        "ingredients": {
            "milk": 32640,
            "cream": 750,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2750,
            "yolks": 1000,
            "pistachio paste": 4500
        },
        "instructions": [
            "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
            "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
        ],
        "subrecipes": {
            "pistachio paste": {
                "ingredients": {
                    "roasted pistachios": 2967,
                    "pistachio oil": 1532
                },
                "instructions": [
                    "1) Roast the pistachios if raw.",
                    "2) Blend pistachios with pistachio oil until smooth and creamy."
                ]
            }
        }
    },
    "Strawberry Preserves": {
        "ingredients": {
            "strawberries": 1250,
            "sugar": 1150,
            "pectin": 11,
            "lemon": 89
        },
        "instructions": [
            "1) Combine strawberries and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Toffee": {
        "ingredients": {
            "butter": 863,
            "sugar": 779,
            "honey": 17,
            "salt": 4
        },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F."
        ],
        "subrecipes": {}
    },
    "vanilla": {
        "ingredients": {
            "milk": 28510,
            "cream": 10000,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2500,
            "yolks": 500,
            "vanilla extract": 100,
            "vanilla seeds": 90
        },
        "instructions": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
        ]
    }
}
# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Ingredient Inventory Section ---
def ingredient_inventory_section():
    st.subheader("📦 Ingredient Inventory Control")

    bulk_units = {
        "milk": "gallons",
        "cream": "half gallons",
        "sugar": "50 lb bags",
        "dry milk": "50 lb bags",
        "flour": "50 lb bags",
        "brown sugar": "50 lb bags",
        "butter": "cases"
    }

    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())

    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
    if st.button("Save Exclusion List"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    ingredient_inventory = {}
    min_thresholds = {}

    st.markdown("#### Enter Inventory and Minimum Thresholds")
    for ing in sorted(all_ingredients):
        if ing in exclude_list:
            continue
        unit = bulk_units.get(ing, "grams")
        col1, col2 = st.columns(2)
        with col1:
            qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
        with col2:
            threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
        ingredient_inventory[ing] = {"amount": qty, "unit": unit}
        min_thresholds[ing] = threshold

    if st.button("Save Ingredient Inventory"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
        st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

    if os.path.exists(THRESHOLD_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)
        with open(THRESHOLD_FILE) as f:
            thresholds = json.load(f)
        needs_order = {
            ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
            for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
        }
        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order)
        else:
            st.success("✅ All ingredients above minimum thresholds.")

# --- Routing ---
if page == "Ingredient Inventory":
    ingredient_inventory_section()
elif page == "Flavor Inventory":
    st.write("Flavor inventory page placeholder (implement or call your function here)")
elif page == "Batching System":
    st.write("Batching system page placeholder (implement or call your function here)")

# # --- Utility Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Recipe Adjuster Section ---
# # ... (no changes here for brevity) ...

# # --- Ingredient Inventory Section ---
# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
#     if st.button("Save Exclusion List"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in sorted(all_ingredients):
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
#         st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#         if needs_order:
#             st.error("⚠️ Order Needed:")
#             st.dataframe(needs_order)
#         else:
#             st.success("✅ All ingredients above minimum thresholds.")

# import streamlit as st

# # --- Sidebar navigation ---
# page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory"])


# # --- Recipes ---
# recipes = {
    
#     "Creme Brulee": {
#         "ingredients": {
#             "milk": 20300,
#             "cream": 6828,
#             "sugar": 4400,
#             "guar": 72,
#             "dry milk": 2800,
#             "yolks": 2400,
#             "caramel sauce": 3200
#         },
#         "instructions": [
#             "1) Weigh and mix all base ingredients except caramel sauce.",
#             "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
#             "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
#             "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
#             "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
#         ],
#         "subrecipes": {
#             "caramel sauce": {
#                 "ingredients": {
#                     "sugar": 3200,
#                     "water": 500,
#                     "honey": 50
#                 },
#                 "instructions": [
#                     "1) Combine sugar, water, and honey.",
#                     "2) Cook on medium-high heat until sugar dissolves.",
#                     "3) Raise heat and cook until mixture reaches 220°F."
#                 ]
#             }
#         }
#     },
#     "Crumble": {
#         "ingredients": {
#             "flour": 223,
#             "sugar": 388,
#             "cinnamon": 8,
#             "butter": 272
#             },
#         "instructions": [
            
#             "1) Melt the butter.",
#             "2) Briefly mix ingredients on the mixer, and remove them before they form a homogeneous mix.",
#             "3) Bake for 15 minmmutes at 350 F."
#             ""
            
#         ],
#         "subrecipes": {}
#     }, 
#     "Cookie Dough": {
#         "ingredients": {
#             "butter": 396,
#             "sugar": 344,
#             "brown sugar": 386,
#             "pasteurized egg whites": 92,
#             "pasteurized egg yolks": 90,
#             "vanilla extract": 16,
#             "flour": 646,
#             "salt": 6
#             },
#         "instructions": [
            
            
            
#         ],
#         "subrecipes": {},
#     },"Dulce de Leche": {
#         "ingredients": {
#             "milk": 24775,
#             "cream": 7500,
#             "sugar": 2550,
#             "guar": 75,
#             "dry milk": 1000,
#             "yolks": 500,
#             "dulce de leche heladero": 90
#         },
#         "instructions": [
            
#         ]
#     },
#     "Fresh Mint": {
#         "ingredients": {
#             "milk": 31140,
#             "cream": 6500,
#             "sugar": 8500,
#             "guar": 110,
#             "dry milk": 3000,
#             "yolks": 750,
#             "mint": 1250,
#             "blanched mint": 500
#         },
#         "instructions": [
#             "Day 1: Prepare Mint-Infused Milk",
#             "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
#             "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
#             "",
#             "Day 2: Prepare Blanched Mint Purée",
#             "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
#             "4) Bring 2 gallons of fresh water to a boil.",
#             "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
#             "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
#             "7) Drain the mint and blend until very fine and smooth.",
#             "",
#             "Final Steps:",
#             "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
#             "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
#         ],
#         "subrecipes": {}
#     },
#     "Graham Cracker Crust": {
#         "ingredients": {
#             "graham cracker crumble": 338,
#             "butter": 310,
#             "sugar": 352
#             },
#         "instructions": [
            
#             "1) Process graham crackers on the Robocoupe.",
#             "2) Mix ingredients on the mixer.",
#             "3) Press ingredients down on a flat pan.",
#             "4) Bake for 15 minmmutes at 325 F."
#             ""
            
#         ],
#         "subrecipes": {}
#     },
#     "Honeycomb": {
#         "ingredients": {
#             "sugar": 3000,
#             "honey": 50,
#             "water": 1450,
#             "baking soda": 250,
#             },
#         "instructions": [
#             "1) Cook on medium heat, stirring constantly until sugar dissolves.",
#             "2) Once sugar is completely dissolved, stop stirring.",
#             "3) Continue cooking on high until 300 F.",
#             "4) Add the baking soda and stir.",
#             "5) Pour the rising honeycomb on previously greased trays and let cool."
#             ""
            
#         ],
#         "subrecipes": {}
#     },
#     "Lemon Bar": {
#     "ingredients": {
#         "crust": 566,  # butter + flour + sugar + salt
#         "filling": 1362  # estimated weight
#     },
#     "instructions": [
#         "1) Bake the crust at 350°F for 15 minutes.",
#         "2) Pour filling onto baked crust and bake at 350°F for 20 minutes."
#     ],
#     "subrecipes": {
#         "crust": {
#             "ingredients": {
#                 "butter": 225,
#                 "flour": 240,
#                 "sugar": 100,
#                 "salt": 1
#             },
#             "instructions": [
#                 "1) Process all crust ingredients in a food processor until smooth.",
#                 "2) Press into a greased pan and bake for 15 minutes at 350°F."
#             ]
#         },
#         "filling": {
#             "ingredients": {
#                 "eggs (each)": 12,
#                 "lemon juice": 360,
#                 "sugar": 900,
#                 "flour": 90
#             },
#             "instructions": [
#                 "1) Beat all filling ingredients in a bowl until fully dissolved.",
#                 "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
#             ]
#         }
#     }
# }
# ,
#     "Lemon Sorbet": {
#         "ingredients": {
#             "water": 5442,
#             "lemon": 3500,
#             "pectin": 87,
#             "guar gum": 12,
#             "sugar": 2625
#             },
#         "instructions": [          
#         ],
#         "subrecipes": {}
#     },
#     "Peach Preserves": {
#         "ingredients": {
#             "peaches": 1350,
#             "sugar": 1250,
#             "lemon": 82
#             },
#         "instructions": [
            
#             "1) combine cored peaches and sugar and let stand for 3 hours.",
#             "2) bring to boil, stirring occasionally.",
#             "3) cook until it reaches 220 F and syrup is thick."
#             ""
            
#         ],
#         "subrecipes": {}
#     },
#     "Pear Sorbet": {
#         "ingredients": {
#             "water": 5500,
#             "pectin": 100,
#             "sugar": 3500,
#             "pear": 10600,
#             "lemon": 300
#             },
#         "instructions": [
            
#             "1) Quarter the pears and remove their seeds.",
#             "2) Fill a put with the quwartered pears and weigh.",
#             "3) Add water to fill completely cover the pears.",
#             "4) weigh the water + pears on the pot.",
#             "5) Cook until pears are soft and translucent.",
#             "6) Re-weigh cooked pear+water mix.",
#             "7) Add enough water to make up for the difference between weighs on spet 4) and 6).",
#             "8) Process all the ingredients on a blender until smooth."
#             ""
            
#         ],
#         "subrecipes": {}
#     },



#     "Pistachio": {
#         "ingredients": {
#             "milk": 32640,
#             "cream": 750,
#             "sugar": 8250,
#             "guar": 110,
#             "dry milk": 2750,
#             "yolks": 1000,
#             "pistachio paste": 4500
#         },
#         "instructions": [
#             "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
#             "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
#         ],
#         "subrecipes": {
#             "pistachio paste": {
#                 "ingredients": {
#                     "roasted pistachios": 2967,
#                     "pistachio oil": 1532
#                 },
#                 "instructions": [
#                     "1) Roast the pistachios if raw.",
#                     "2) Blend pistachios with pistachio oil until smooth and creamy."
#                 ]
#             }
#         }
#     },
#     "Strawberry Preserves": {
#         "ingredients": {
#             "strawberries": 1250,
#             "sugar": 1150,
#             "pectin": 11,
#             "lemon": 89
#             },
#         "instructions": [
            
#             "1) combine strawberries and sugar and let stand for 3 hours.",
#             "2) bring to boil, stirring occasionally.",
#             "3) cook until it reaches 220 F and syrup is thick."
#             ""
            
#         ],
#         "subrecipes": {}
#     },
#     "Toffee": {
#         "ingredients": {
#             "butter": 863,
#             "sugar": 779,
#             "honey": 17,
#             "salt": 4,
#             },
#         "instructions": [
            
#             "1) Cook on medium heat, stirring constantly until sugar dissolves.",
#             "2) Once sugar is completely dissolved, stop stirring.",
#             "3) Continue cooking on high until 300 F."
#             ""
            
#         ],
#         "subrecipes": {}
#     },
#     "vanilla": {
#         "ingredients": {
#             "milk": 28510,
#             "cream": 10000,
#             "sugar": 8250,
#             "guar": 110,
#             "dry milk": 2500,
#             "yolks": 500,
#             "vanilla extract": 100,
#             "vanilla seeds": 90
#         },
#         "instructions": [
#             "1) Combine all ingredients.",
#             "2) Pasteurize the mix.",
#             "3) Chill, batch freeze, and pack."
#         ]
#     }
# }

# # --- Scaling Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}

#     scaled = {
#         "ingredients": adjusted_main,
#         "instructions": recipe.get("instructions", [])
#     }

#     if "subrecipes" in recipe:
#         scaled["subrecipes"] = {}
#         for name, sub in recipe["subrecipes"].items():
#             scaled_sub = {
#                 "ingredients": {k: round(v * scale_factor) for k, v in sub["ingredients"].items()},
#                 "instructions": sub.get("instructions", [])
#             }
#             scaled["subrecipes"][name] = scaled_sub

#     return scaled, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- Streamlit App ---
# st.title("Ice Cream Recipe Adjuster")

# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# st.subheader("Choose how you want to scale the recipe:")
# scale_mode = st.selectbox("Scaling method", ["Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans", "Available ingredient amounts"])

# target_weight = None
# scaled_recipe = None

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)", "")
#     if w.strip():
#         try:
#             target_weight = float(w)
#         except ValueError:
#             st.error("Enter a valid number for total weight")

# elif scale_mode == "1.5 gallon tubs":
#     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#     target_weight = tubs * 4275

# elif scale_mode == "5 liter pans":
#     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#     target_weight = pans * 3750

# elif scale_mode == "Mix of tubs and pans":
#     tubs = st.number_input("Tubs", min_value=0, step=1)
#     pans = st.number_input("Pans", min_value=0, step=1)
#     target_weight = tubs * 4275 + pans * 3750

# if target_weight:
#     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)

# if scale_mode == "Available ingredient amounts":
#     st.subheader("Enter available ingredient amounts (g):")
#     available_inputs = {}
#     for ing in recipe["ingredients"]:
#         val = st.text_input(f"{ing}", "")
#         if val.strip():
#             try:
#                 available_inputs[ing] = float(val)
#             except ValueError:
#                 st.error(f"Invalid input for {ing}")

#     if st.button("Adjust Recipe Based on Ingredients"):
#         adjusted, limit_scale = adjust_recipe_with_constraints(recipe, available_inputs)
#         st.session_state.adjusted_recipe = adjusted
#         st.session_state.adjusted_total = round(sum(adjusted.values()))
#         st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
#         st.subheader(f"Final Adjusted Recipe:")
#         for ing, amt in adjusted.items():
#             st.write(f"{ing}: {amt} g")

# if scaled_recipe:
#     st.markdown("---")
#     st.success(f"Scaled recipe to {round(target_weight)} g")
#     st.subheader(f"Scaled {selected} Recipe")

#     # --- Main Ingredients ---
#     st.subheader("Main Ingredients")
#     for ing, amt in scaled_recipe["ingredients"].items():
#         st.write(f"• {ing}: {amt} g")

#     # --- Subrecipes ---
#     if "subrecipes" in scaled_recipe:
#         for subname, sub in scaled_recipe["subrecipes"].items():
#             st.subheader(f"Subrecipe: {subname}")
#             for ing, amt in sub.get("ingredients", {}).items():
#                 st.write(f"• {ing}: {amt} g")

#     # --- Instructions ---
#     if scaled_recipe.get("instructions"):
#         st.subheader("Instructions")
#         for step in scaled_recipe["instructions"]:
#             st.markdown(f"- {step}")
# # --- Step-by-Step Ingredient Mode ---
# st.markdown("---")
# st.subheader("🧪 Step-by-Step Weighing")

# # Initialize step index safely
# if "step_index" not in st.session_state:
#     st.session_state.step_index = 0

# if st.button("Start Step-by-Step Mode"):
#     st.session_state.step_index = 0

# if scaled_recipe:
#     # Flatten ingredients and subrecipes
#     all_ingredients = list(scaled_recipe["ingredients"].items())

#     if "subrecipes" in scaled_recipe:
#         for subname, sub in scaled_recipe["subrecipes"].items():
#             all_ingredients.append((f"[{subname}]", None))  # Section header
#             all_ingredients.extend(list(sub["ingredients"].items()))

#     step = st.session_state.step_index

#     if step < len(all_ingredients):
#         label, amount = all_ingredients[step]

#         if amount is None:
#             st.markdown(f"### {label}")  # e.g., [crust]
#         else:
#             st.markdown(f"### {label}: {round(amount)} grams")

#         if st.button("Next"):
#             st.session_state.step_index += 1
#     else:
#         st.success("✅ All ingredients completed!")
#         if st.button("Restart"):
#             st.session_state.step_index = 0




# import os
# import json
# from datetime import datetime

# # --- Constants ---
# LINEUP_FILE = "weekly_lineup.json"
# INVENTORY_FILE = "inventory.json"

# # --- Load & Save ---
# def load_inventory_data():
#     if os.path.exists(LINEUP_FILE):
#         with open(LINEUP_FILE) as f:
#             lineup = json.load(f)
#     else:
#         lineup = []

#     if os.path.exists(INVENTORY_FILE):
#         with open(INVENTORY_FILE) as f:
#             inventory = json.load(f)
#     else:
#         inventory = {}

#     return lineup, inventory

# def save_inventory_data(lineup, inventory):
#     with open(LINEUP_FILE, "w") as f:
#         json.dump(lineup, f)
#     with open(INVENTORY_FILE, "w") as f:
#         json.dump(inventory, f)

# # --- Flavor Inventory UI ---
# def flavor_inventory_section():
#     st.subheader("🍦 Flavor & Topping Inventory Control")

#     lineup, inventory = load_inventory_data()

#     st.markdown("#### 1. Set Weekly Flavor Lineup")
#     lineup_input = st.text_area("Flavors (comma-separated)", value=", ".join(lineup), key="lineup_input")
#     # if st.button("Update Lineup"):
#     #     lineup = [flavor.strip() for flavor in lineup_input.split(",") if flavor.strip()]
#     #     save_inventory_data(lineup, inventory)
#     #     st.success("Lineup updated.")
#     if st.button("Update Lineup"):
#         lineup = [flavor.strip() for flavor in lineup_input.split(",") if flavor.strip()]
    
#         # Remove inventory entries not in the new lineup
#         inventory = {flavor: data for flavor, data in inventory.items() if flavor in lineup}
    
#         save_inventory_data(lineup, inventory)
#         st.success("Lineup updated and inventory cleaned.")


#     st.markdown("#### 2. Update Inventory ")
#     if not lineup:
#         st.warning("Please set the weekly lineup first.")
#         return

#     flavor = st.selectbox("Select a flavor to update", lineup, key="flavor_select")
#     quarts = st.number_input("Enter quarts available", min_value=0, step=1, key="quarts_input")

#     if st.button("Submit Inventory"):
#         inventory[flavor] = {
#             "quarts": quarts,
#             "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
#         }
#         save_inventory_data(lineup, inventory)
#         st.success(f"Inventory updated for {flavor}")

#     st.markdown("#### 3. Current Inventory")
#     if inventory:
#         sorted_inventory = sorted(inventory.items(), key=lambda x: x[1]['quarts'], reverse=True)
#         table = {
#             "Flavor": [k for k, _ in sorted_inventory],
#             "Quarts": [v["quarts"] for _, v in sorted_inventory],
#             "Last Updated": [v["last_updated"] for _, v in sorted_inventory],
#         }
#         st.dataframe(table)
#     else:
#         st.info("No inventory records yet.")
# # Add this at the bottom of your main file
# page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory"])

# if page == "Batching System":
#     # your existing batching code
#     pass  # Replace with your batching app logic
# elif page == "Flavor Inventory":
#     flavor_inventory_section()


# # --- Routing ---
# if page == "Batching System":
#     st.title("Ice Cream Recipe Adjuster")
#     recipe_adjuster_section()  # call your recipe adjuster function

# elif page == "Flavor Inventory":
#     flavor_inventory_section()


# def recipe_adjuster_section():
#     # all your existing batching code goes here
#     # e.g., dropdowns, weight inputs, scaling logic, display results
#     # Example:
#     st.markdown("### Select a recipe and scale it")
#     # ... your full recipe scaling UI logic ...










































