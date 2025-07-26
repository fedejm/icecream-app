import streamlit as st

# --- Recipes ---
recipes = {
    "vanilla": {
        "milk": 28510,
        "cream": 10000,
        "sugar": 8250,
        "guar": 110,
        "dry_milk": 2500,
        "yolks": 500,
        "vanilla_extract": 100,
        "vanilla_seeds": 90
    },
    "chocolate": {
        "milk": 25000,
        "cream": 9000,
        "sugar": 7500,
        "cocoa": 3000,
        "guar": 120,
        "dry_milk": 2600
    }
}

# --- Scaling Function ---
def adjust_recipe_with_constraints(recipe, available_ingredients):
    ratios = []
    for ing, amt in available_ingredients.items():
        if ing in recipe and recipe[ing] != 0:
            ratios.append(amt / recipe[ing])
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
    return adjusted, scale_factor

# --- Streamlit App ---
st.title("Ice Cream Recipe Adjuster")

# Select recipe
selected = st.selectbox("Choose a recipe", list(recipes.keys()))
recipe = recipes[selected]

st.subheader("Enter available amounts (in grams)")
st.write("Leave blank if you have the full amount for an ingredient.")

# Collect available inputs
available_inputs = {}
for ing in recipe:
    val = st.text_input(f"{ing}", "")
    if val.strip():
        try:
            available_inputs[ing] = float(val)
        except ValueError:
            st.error(f"Invalid input for {ing}")

# Button to adjust
if st.button("Adjust Recipe"):
    adjusted, scale = adjust_recipe_with_constraints(recipe, available_inputs)
    st.success(f"Scale factor: {scale:.2f}")
    st.subheader("Adjusted Recipe:")
    for ing, amt in adjusted.items():
        st.write(f"{ing}: {amt} g")

st.subheader("Choose how you want to scale the recipe:")

scale_mode = st.selectbox(
    "Scaling method",
    ("Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans")
)

target_weight = None

if scale_mode == "Total weight (grams)":
    w = st.text_input("Enter target total weight (g)", "")
    if w.strip():
        try:
            target_weight = float(w)
        except ValueError:
            st.error("Enter a valid number for total weight")

elif scale_mode == "1.5 gallon tubs":
    tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
    target_weight = tubs * 4275  # approx 0.75 g/mL × 5.7L

elif scale_mode == "5 liter pans":
    pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
    target_weight = pans * 3750

elif scale_mode == "Mix of tubs and pans":
    tubs = st.number_input("Tubs", min_value=0, step=1)
    pans = st.number_input("Pans", min_value=0, step=1)
    target_weight = tubs * 4275 + pans * 3750

# Scale recipe if a target weight is set
scaled_recipe = recipe
scale_factor = 1

if target_weight:
    scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
    st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")
#updated 072525
