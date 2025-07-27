

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
        "vanilla extract": 100,
        "vanilla seeds": 90
    },
    
    "Dulce de Leche": {
        "milk": 24775,
        "cream": 7500,
        "sugar": 2550,
        "guar": 75,
        "dry milk": 1000,
        "yolks": 500,
        "deulce de leche heladero": 90
    },
    "Creme Brulee": {
        "milk": 20300,
        "cream": 6828,
        "sugar": 4400,
        "guar": 72,
        "dry milk": 2800,
        "yolks": 2400,
        "caramel sauce": 3200
    }
    }
# --- Scaling Functions ---
def get_total_weight(recipe):
    return sum(recipe.values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
    return adjusted, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    ratios = []
    for ing, amt in available_ingredients.items():
        if ing in recipe and recipe[ing] != 0:
            ratios.append(amt / recipe[ing])
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
    return adjusted, scale_factor

# --- UI ---
st.title("Ice Cream Recipe Adjuster")

# Select recipe
selected = st.selectbox("Choose a recipe", list(recipes.keys()))
recipe = recipes[selected]

# --- Scaling Method ---
st.subheader("Choose how you want to scale the recipe:")
scale_mode = st.selectbox(
    "Scaling method",
    (
        "Total weight (grams)",
        "1.5 gallon tubs",
        "5 liter pans",
        "Mix of tubs and pans",
        "Available ingredient amounts"
    )
)

target_weight = None
show_ingredient_inputs = False

if scale_mode == "Total weight (grams)":
    w = st.text_input("Enter target total weight (g)", "")
    if w.strip():
        try:
            target_weight = float(w)
        except ValueError:
            st.error("Enter a valid number for total weight")

elif scale_mode == "1.5 gallon tubs":
    tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
    target_weight = tubs * 4275

elif scale_mode == "5 liter pans":
    pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
    target_weight = pans * 3750

elif scale_mode == "Mix of tubs and pans":
    tubs = st.number_input("Tubs", min_value=0, step=1)
    pans = st.number_input("Pans", min_value=0, step=1)
    target_weight = tubs * 4275 + pans * 3750

elif scale_mode == "Available ingredient amounts":
    show_ingredient_inputs = True

# --- Scale recipe if target weight is defined ---
scaled_recipe = recipe
scale_factor = 1

if target_weight:
    scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
    st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")
    st.subheader(f"Scaled {selected} Recipe:")
    st.session_state.adjusted_recipe = scaled_recipe
    st.session_state.adjusted_total = round(sum(scaled_recipe.values()))
    st.session_state.processing_mode = False
    st.session_state.current_step = 0

    for ing, amt in scaled_recipe.items():
        st.write(f"{ing}: {amt} g")

    st.button("Process Recipe", on_click=lambda: st.session_state.update({
        "processing_mode": True,
        "current_step": 0
    }))


# --- Available Ingredient Input Mode ---
if show_ingredient_inputs:
    st.subheader("Enter available ingredient amounts (in grams)")
    st.write("Leave blank if you have the full amount for an ingredient.")

    available_inputs = {}
    for ing in recipe:
        val = st.text_input(f"{ing}", "")
        if val.strip():
            try:
                available_inputs[ing] = float(val)
            except ValueError:
                st.error(f"Invalid input for {ing}")

    if st.button("Adjust Recipe Based on Ingredients"):
        adjusted, limit_scale = adjust_recipe_with_constraints(recipe, available_inputs)
        st.session_state.adjusted_recipe = adjusted
        st.session_state.adjusted_total = round(sum(adjusted.values()))
        st.session_state.processing_mode = False
        st.session_state.current_step = 0

        st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
        st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
        for ing, amt in st.session_state.adjusted_recipe.items():
            st.write(f"{ing}: {amt} g")

        st.button("Process Recipe", on_click=lambda: st.session_state.update({
            "processing_mode": True,
            "current_step": 0
        }))
# --- Step-by-step processing screen ---
if st.session_state.get("processing_mode", False):
    adjusted = st.session_state.get("adjusted_recipe", None)
    if not adjusted:
        st.error("No adjusted recipe found. Please scale or adjust a recipe first.")
    else:
        step = st.session_state.get("current_step", 0)
        ingredients = list(adjusted.items())

        if step < len(ingredients):
            ing, amt = ingredients[step]
            st.header(f"Step {step + 1} of {len(ingredients)}")
            st.subheader(f"🧪 {ing}: {amt} g")

            if st.button("Next"):
                st.session_state.current_step += 1
        else:
            st.success("✅ All ingredients processed!")
            if st.button("Reset"):
                st.session_state.processing_mode = False
                st.session_state.current_step = 0

# # --- Step-by-step processing screen ---
# if st.session_state.get("processing_mode", False):
#     adjusted = st.session_state.get("adjusted_recipe", {})
#     step = st.session_state.get("current_step", 0)
#     ingredients = list(adjusted.items())

#     if step < len(ingredients):
#         ing, amt = ingredients[step]
#         st.header(f"Step {step + 1} of {len(ingredients)}")
#         st.subheader(f"🧪 {ing}: {amt} g")

#         if st.button("Next"):
#             st.session_state.current_step += 1
#     else:
#         st.success("✅ All ingredients processed!")
#         if st.button("Reset"):
#             st.session_state.processing_mode = False
#             st.session_state.current_step = 0



# # --- Scaling Function ---
# def get_total_weight(recipe):
#     return sum(recipe.values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
#     return adjusted, scale_factor


# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in recipe and recipe[ing] != 0:
#             ratios.append(amt / recipe[ing])
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
#     return adjusted, scale_factor

# # --- Streamlit App ---
# st.title("Ice Cream Recipe Adjuster")

# # Select recipe
# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# st.subheader("Enter available amounts (in grams)")
# st.write("Leave blank if you have the full amount for an ingredient.")

# # Collect available inputs
# available_inputs = {}
# for ing in recipe:
#     val = st.text_input(f"{ing}", "")
#     if val.strip():
#         try:
#             available_inputs[ing] = float(val)
#         except ValueError:
#             st.error(f"Invalid input for {ing}")

# # # Button to adjust
# #  if st.button("Adjust Recipe"):
# #     adjusted, scale = adjust_recipe_with_constraints(recipe, available_inputs)
# #     st.success(f"Scale factor: {scale:.2f}")
# #     st.subheader("Adjusted Recipe:")
# #     for ing, amt in adjusted.items():
# #         st.write(f"{ing}: {amt} g")

# # --- Final Adjusted Output ---
# if st.button("Adjust Recipe Based on Ingredients"):
#     adjusted, limit_scale = adjust_recipe_with_constraints(scaled_recipe, available_inputs)
#     st.session_state.adjusted_recipe = adjusted
#     st.session_state.adjusted_total = round(sum(adjusted.values()))
#     st.session_state.processing_mode = False
#     st.session_state.current_step = 0

#     st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
#     st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
#     for ing, amt in st.session_state.adjusted_recipe.items():
#         st.write(f"{ing}: {amt} g")

#     st.button("Process Recipe", on_click=lambda: st.session_state.update({
#         "processing_mode": True,
#         "current_step": 0
#     }))

# # --- Step-by-step processing screen ---
# if st.session_state.get("processing_mode", False):
#     adjusted = st.session_state.get("adjusted_recipe", {})
#     step = st.session_state.get("current_step", 0)
#     ingredients = list(adjusted.items())

#     if step < len(ingredients):
#         ing, amt = ingredients[step]
#         st.header(f"Step {step + 1} of {len(ingredients)}")
#         st.subheader(f"🧪 {ing}: {amt} g")

#         if st.button("Next"):
#             st.session_state.current_step += 1
#     else:
#         st.success("✅ All ingredients processed!")
#         if st.button("Reset"):
#             st.session_state.processing_mode = False
#             st.session_state.current_step = 0


# st.subheader("Choose how you want to scale the recipe:")

# scale_mode = st.selectbox(
#     "Scaling method",
#     ("Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans")
# )

# target_weight = None

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)", "")
#     if w.strip():
#         try:
#             target_weight = float(w)
#         except ValueError:
#             st.error("Enter a valid number for total weight")

# elif scale_mode == "1.5 gallon tubs":
#     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#     target_weight = tubs * 4275  # approx 0.75 g/mL × 5.7L

# elif scale_mode == "5 liter pans":
#     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#     target_weight = pans * 3750

# elif scale_mode == "Mix of tubs and pans":
#     tubs = st.number_input("Tubs", min_value=0, step=1)
#     pans = st.number_input("Pans", min_value=0, step=1)
#     target_weight = tubs * 4275 + pans * 3750

# # Scale recipe if a target weight is set
# scaled_recipe = recipe
# scale_factor = 1

# if target_weight:
#     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
#     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")


# --- Scaling Functions ---
# def get_total_weight(recipe):
#     return sum(recipe.values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
#     return adjusted, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in recipe and recipe[ing] != 0:
#             ratios.append(amt / recipe[ing])
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
#     return adjusted, scale_factor

# # --- UI ---
# st.title("Ice Cream Recipe Adjuster")

# # Select recipe
# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# # --- Scaling Input ---
# st.subheader("Choose how you want to scale the recipe:")
# scale_mode = st.selectbox(
#     "Scaling method",
#     ("Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans")
# )

# target_weight = None

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

# # --- Scale recipe if target weight is defined ---
# scaled_recipe = recipe
# scale_factor = 1

# if target_weight:
#     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
#     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")

# # --- Ingredient availability input ---
# st.subheader("Enter available ingredient amounts (in grams)")
# st.write("Leave blank if you have the full amount for an ingredient.")

# available_inputs = {}
# for ing in scaled_recipe:
#     val = st.text_input(f"{ing}", "")
#     if val.strip():
#         try:
#             available_inputs[ing] = float(val)
#         except ValueError:
#             st.error(f"Invalid input for {ing}")

# # --- Final Adjusted Output ---
# if st.button("Adjust Recipe Based on Ingredients"):
#     adjusted, limit_scale = adjust_recipe_with_constraints(scaled_recipe, available_inputs)
#     st.session_state.adjusted_recipe = adjusted
#     st.session_state.adjusted_total = round(sum(adjusted.values()))
#     st.session_state.processing_mode = False
#     st.session_state.current_step = 0

#     st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
#     st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
#     for ing, amt in st.session_state.adjusted_recipe.items():
#         st.write(f"{ing}: {amt} g")

#     st.button("Process Recipe", on_click=lambda: st.session_state.update({
#         "processing_mode": True,
#         "current_step": 0
#     }))

# # --- Step-by-step processing screen ---
# if st.session_state.get("processing_mode", False):
#     adjusted = st.session_state.get("adjusted_recipe", {})
#     step = st.session_state.get("current_step", 0)
#     ingredients = list(adjusted.items())

#     if step < len(ingredients):
#         ing, amt = ingredients[step]
#         st.header(f"Step {step + 1} of {len(ingredients)}")
#         st.subheader(f"🧪 {ing}: {amt} g")

#         if st.button("Next"):
#             st.session_state.current_step += 1
#     else:
#         st.success("✅ All ingredients processed!")
#         if st.button("Reset"):
#             st.session_state.processing_mode = False
#             st.session_state.current_step = 0



#updated 072525
