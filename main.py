from engine.macros import calculate_macros
from engine.meal_generator import generate_day, generate_week
from engine.analysis import analyze_meal


# ==========================
# USER INPUT
# ==========================
age = int(input("Age: "))
weight = float(input("Weight (kg): "))
height = float(input("Height (cm): "))

activity = input(
    "Activity (sedentary/light/moderate/active): "
).strip().lower()

goal = input(
    "Goal (lose_weight / maintain / gain_muscle): "
).strip().lower()

meals_per_day = int(input("Meals per day (2-5): "))


# ==========================
# INPUT VALIDATION
# ==========================
valid_goals = ["lose_weight", "maintain", "gain_muscle"]
valid_activity = ["sedentary", "light", "moderate", "active"]

if goal not in valid_goals:
    print("⚠ Invalid goal entered → switched to maintain")
    goal = "maintain"

if activity not in valid_activity:
    print("⚠ Invalid activity entered → switched to moderate")
    activity = "moderate"

if meals_per_day < 2:
    meals_per_day = 2
elif meals_per_day > 5:
    meals_per_day = 5


# ==========================
# PROFILE CLASS
# ==========================
class Profile:
    def __init__(self, age, weight, height, activity, goal, meals_per_day):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.goal = goal
        self.meals_per_day = meals_per_day


profile = Profile(
    age,
    weight,
    height,
    activity,
    goal,
    meals_per_day
)


# ==========================
# MACROS
# ==========================
target = calculate_macros(
    weight,
    goal,
    activity
)

print("\n" + "=" * 55)
print("🎯 TARGET MACROS")
print("=" * 55)

print(f"Goal     : {goal}")
print(f"Calories : {target['calories']}")
print(f"Protein  : {target['protein']} g")
print(f"Carbs    : {target['carbs']} g")
print(f"Fat      : {target['fat']} g")


# ==========================
# GENERATE PLANS
# ==========================
day_plan = generate_day(profile)
week_plan = generate_week(profile)


# ==========================
# DAILY PLAN
# ==========================
print("\n" + "=" * 55)
print("📅 DAILY PLAN")
print("=" * 55)

for meal_name, items in day_plan.items():

    print(f"\n🍽 {meal_name.upper()}")
    print("-" * 35)

    for item in items:
        print(
            f"- {item['food']} | "
            f"{item['calories']} cal | "
            f"P:{item['protein']} "
            f"C:{item['carbs']} "
            f"F:{item['fat']}"
        )


# ==========================
# WEEKLY PLAN
# ==========================
print("\n" + "=" * 55)
print("📆 WEEKLY PLAN")
print("=" * 55)

for day_name, meals in week_plan.items():

    print(f"\n🗓 {day_name}")
    print("-" * 40)

    for meal_name, items in meals.items():

        print(f"\n🍽 {meal_name.upper()}")
        print("-" * 25)

        for item in items:
            print(
                f"- {item['food']} | "
                f"{item['calories']} cal"
            )


# ==========================
# MEAL ANALYSIS
# ==========================
print("\n" + "=" * 55)
print("🧠 MEAL ANALYSIS")
print("=" * 55)

dish_label = input("Enter dish name: ").strip().lower()

# sample realistic meal values
meal_total = {
    "calories": round(target["calories"] * 0.60),
    "protein": round(target["protein"] * 0.80),
    "carbs": round(target["carbs"] * 0.70),
    "fat": round(target["fat"] * 0.50),
    "sodium_mg": 800,
    "added_sugars": 5
}

base_plan = {
    "diet": goal,
    "calories": target["calories"],
    "why": "Calculated from user goal + activity"
}

analysis = analyze_meal(
    profile,
    base_plan,
    meal_total,
    dish_label
)


# ==========================
# ANALYSIS RESULT
# ==========================
print("\n" + "=" * 55)
print("📊 RESULT")
print("=" * 55)

print(f"Dish: {dish_label}")
print(f"Suggested diet: {analysis['diet']}")
print(f"Daily calories target: {analysis['daily_calories_target']}")
print(f"Meal calories limit : {analysis['meal_calories_limit']}")

print("\nUpdates:")
for u in analysis["updates"]:
    print("-", u)

print("\nWhy:")
for w in analysis["why"]:
    print("-", w)


# ==========================
# FINAL CHECK
# ==========================
if meal_total["calories"] <= analysis["meal_calories_limit"]:
    print("\n✔ Meal fits your plan")
else:
    print("\n❌ Meal exceeds your plan")