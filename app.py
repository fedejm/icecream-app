import streamlit as st
import os
import json

# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"

# --- Recipe Database ---
recipes = {
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
        ],
        "subrecipes": {}
    },
    "chocolate": {
        "ingredients": {
            "milk": 28000,
            "cream": 9000,
            "sugar": 8000,
            "cocoa powder": 1200,
            "chocolate": 1500
        },
        "instructions": [
            "1) Combine all ingredients.",
            "2) Heat while stirring.",
            "3) Pasteurize, chill, batch freeze, and pack."
        ],
        "subrecipes": {}
    },
    "strawberry": {
        "ingredients": {
            "milk": 28000,
            "cream": 9000,
            "sugar": 7000,
            "strawberries": 4000
        },
        "instructions": [
            "1) Blend strawberries.",
            "2) Combine with all other ingredients.",
            "3) Pasteurize, chill, batch freeze, and pack."
        ],
        "subrecipes": {}
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

# --- Sidebar Navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory"], key="sidebar_nav")

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

    steps = list(recipe["ingredients"].items())
    if st.session_state.step_i < len(steps):
        ing, amt = steps[st.session_state.step_i]
        st.markdown(f"**Weigh:** {amt} grams of {ing}")
        if st.button("Next Ingredient", key=f"next_{st.session_state.step_i}"):
            st.session_state.step_i += 1
    else:
        st.success("🎉 All ingredients completed!")

# --- Flavor Inventory Section ---
def flavor_inventory_section():
    st.subheader("📋 Flavor Inventory")

    current_lineup = []
    if os.path.exists(LINEUP_FILE):
        with open(LINEUP_FILE) as f:
            current_lineup = json.load(f)

    st.markdown("### 🧁 Weekly Flavor Lineup")
    all_recipe_names = list(recipes.keys())

    selected_flavors = st.multiselect(
        "Select flavors for this week's lineup:",
        all_recipe_names,
        default=current_lineup,
        key="weekly_flavor_picker"
    )

    if st.button("Save Weekly Lineup", key="save_weekly_lineup_btn"):
        with open(LINEUP_FILE, "w") as f:
            json.dump(selected_flavors, f, indent=2)
        st.success("✅ Weekly lineup saved!")

    if selected_flavors:
        st.markdown("### 📋 Selected Flavors and Their Ingredients")
        for flavor in selected_flavors:
            st.markdown(f"#### 🍨 {flavor}")
            for ing, amt in recipes[flavor]["ingredients"].items():
                st.write(f"- {amt} grams {ing}")
    else:
        st.info("No flavors selected yet.")

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

# --- Routing ---
with st.container():
    if page == "Batching System":
        batching_system_section()
    elif page == "Flavor Inventory":
        flavor_inventory_section()
    elif page == "Ingredient Inventory":
        ingredient_inventory_section()
