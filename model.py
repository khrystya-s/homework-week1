"""
model.py - Модель даних (M у MVC)
Містить класи даних та всю бізнес-логіку:
зберігання, завантаження, CRUD, аналітика, розрахунок ІМТ і норми калорій.
"""

import json
import os
import datetime


class FoodItem:
    # Модель одного продукту або страви

    def __init__(self, name: str, calories: float, proteins: float,
                 fats: float, carbs: float, category: str = "Загальне",
                 fiber: float = 0.0):
        self.name     = name
        self.calories = float(calories)
        self.proteins = float(proteins)
        self.fats     = float(fats)
        self.carbs    = float(carbs)
        self.category = category
        self.fiber    = float(fiber)

    def to_dict(self) -> dict:
        return {
            "name": self.name, "calories": self.calories,
            "proteins": self.proteins, "fats": self.fats,
            "carbs": self.carbs, "category": self.category,
            "fiber": self.fiber,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FoodItem":
        return cls(d["name"], d["calories"], d["proteins"],
                   d["fats"], d["carbs"], d.get("category", "Загальне"),
                   d.get("fiber", 0.0))


class MealEntry:

    def __init__(
        self,
        food_name,
        grams,
        calories,
        proteins=0,
        fats=0,
        carbs=0,
        fiber=0,
        date=None
    ):

        self.food_name = food_name
        self.grams = grams
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
        self.fiber = fiber

        self.date = (
            date
            if date
            else datetime.date.today().isoformat()
        )

    def to_dict(self):
        return {
            "food_name": self.food_name,
            "grams": self.grams,
            "calories": self.calories,
            "proteins": self.proteins,
            "fats": self.fats,
            "carbs": self.carbs,
            "fiber": self.fiber,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["food_name"],
            data["grams"],
            data["calories"],
            data.get("proteins", 0),
            data.get("fats", 0),
            data.get("carbs", 0),
            data.get("fiber", 0),
            data.get("date")
        )

ACTIVITY_PRESETS = [
    ("Ходьба",         4.0),
    ("Біг",           10.0),
    ("Велосипед",      7.5),
    ("Плавання",       8.0),
    ("Йога",           3.0),
    ("Силове тренування", 6.0),
    ("Танці",          5.0),
    ("Інше",           5.0),
]

class ActivityEntry:
    # Запис фізичної активності

    def __init__(self, activity: str, minutes: float, calories_burned: float, date=None):
        self.activity        = activity
        self.minutes         = float(minutes)
        self.calories_burned = float(calories_burned)
        self.date = date if date else datetime.date.today().isoformat()

    def to_dict(self):
        return {
            "activity":        self.activity,
            "minutes":         self.minutes,
            "calories_burned": self.calories_burned,
            "date":            self.date,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["activity"], d["minutes"], d["calories_burned"], d.get("date"))


class WeightEntry:
    def __init__(self, weight, date=None, note=""):
        self.weight = float(weight)
        self.note = note

        self.date = (
            date
            if date
            else datetime.date.today().isoformat()
        )

    def to_dict(self):
        return {
            "weight": self.weight,
            "date": self.date,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["weight"],
            data.get("date"),
            data.get("note", "")
        )
# Розрахунки ІМТ

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    # Індекс маси тіла
    h = height_cm / 100.0
    return round(weight_kg / (h * h), 1)

def bmi_category(bmi: float) -> str:
    # Ключі для перекладу ІМТ
    if bmi < 18.5: return "bmi_underweight"
    if bmi < 25.0: return "bmi_normal"
    if bmi < 30.0: return "bmi_overweight"
    return "bmi_obese"

def bmi_color(bmi: float) -> str:
    # Колір для візуалізації ІМТ
    if bmi < 18.5: return "#42A5F5"
    if bmi < 25.0: return "#66BB6A"
    if bmi < 30.0: return "#FFA726"
    return "#EF5350"

def calculate_bmr(weight_kg: float, height_cm: float,
                  age: int, sex: str) -> float:
    """
    Базовий обмін речовин (BMR) за формулою Міффліна–Сан Жеора.
    sex: 'male' або 'female'
    """
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == "male" else base - 161

ACTIVITY_LEVELS = {
    "activity_sedentary": 1.2,
    "activity_light": 1.375,
    "activity_moderate": 1.55,
    "activity_high": 1.725,
    "activity_extreme": 1.9,
}

GOAL_ADJUSTMENTS = {
    "goal_loss_fast": -500,
    "goal_loss_soft": -250,
    "goal_maintain": 0,
    "goal_gain_soft": 250,
    "goal_gain_fast": 500,
}

def calculate_tdee(bmr: float, activity_key: str) -> float:
    return round(bmr * ACTIVITY_LEVELS.get(activity_key, 1.2))


# Центральна модель
class AppModel:
    DATA_FILE = "data.json"

    def __init__(self):
        self.food_items:    list[FoodItem]      = []
        self.meal_log:      list[MealEntry]     = []
        self.weight_log:    list[WeightEntry]   = []
        self.activity_log:  list[ActivityEntry] = []
        self.daily_goal:    float = 2000.0
        self.water_goal:    float = 2000.0
        self.water_log:     dict[str, float]    = {}
        self.language:      str = "uk"
        self.theme_name:    str = "Класична"
        self.load()

    # Збереження / завантаження

    def save(self):
        data = {
            "food_items":   [f.to_dict() for f in self.food_items],
            "meal_log":     [m.to_dict() for m in self.meal_log],
            "weight_log":   [w.to_dict() for w in self.weight_log],
            "activity_log": [a.to_dict() for a in self.activity_log],
            "daily_goal":   self.daily_goal,
            "water_goal":   self.water_goal,
            "water_log":    self.water_log,
            "language":     self.language,
            "theme_name":   self.theme_name,
        }
        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, encoding="utf-8") as f:
                    data = json.load(f)
                self.food_items = [FoodItem.from_dict(d)  for d in data.get("food_items", [])]
                self.meal_log   = [MealEntry.from_dict(d) for d in data.get("meal_log",   [])]
                self.weight_log = [
                    WeightEntry.from_dict(d)
                    for d in data.get("weight_log", [])
                ]
                self.activity_log = [ActivityEntry.from_dict(d) for d in data.get("activity_log", [])]
                self.daily_goal = data.get("daily_goal", 2000.0)
                self.water_goal = data.get("water_goal", 2000.0)
                self.water_log  = data.get("water_log", {})
                self.language   = data.get("language", "uk")
                self.theme_name = data.get("theme_name", "Класична")
            except (json.JSONDecodeError, KeyError):
                self._load_defaults()
        else:
            self._load_defaults()

    def _load_defaults(self):
        self.food_items = [
            FoodItem("Гречка варена",        110,  4.2,  1.1, 21.3, "Крупи"),
            FoodItem("Курятина (грудка)",    165, 31.0,  3.6,  0.0, "М'ясо"),
            FoodItem("Яйце куряче",          155, 13.0, 11.0,  1.1, "М'ясо"),
            FoodItem("Хліб житній",          215,  5.6,  1.2, 42.0, "Хліб"),
            FoodItem("Молоко 2.5%",           52,  2.8,  2.5,  4.7, "Молочне"),
            FoodItem("Яблуко",                52,  0.3,  0.2, 14.0, "Фрукти"),
            FoodItem("Банан",                 89,  1.1,  0.3, 22.8, "Фрукти"),
            FoodItem("Рис варений",          130,  2.7,  0.3, 28.2, "Крупи"),
            FoodItem("Сир кисломолочний 5%", 121, 17.0,  5.0,  1.8, "Молочне"),
            FoodItem("Вівсянка на воді",      88,  3.0,  1.7, 15.0, "Крупи"),
        ]
        self.save()

    # CRUD: продукти

    def add_food(self, item: FoodItem):
        self.food_items.append(item); self.save()

    def edit_food(self, index: int, item: FoodItem):
        self.food_items[index] = item; self.save()

    def delete_food(self, index: int):
        del self.food_items[index]; self.save()

    def get_food_by_name(self, name: str) -> FoodItem | None:
        return next((f for f in self.food_items if f.name == name), None)

    def entries_by_date(self, date_str: str) -> list[MealEntry]:
        return [
            e for e in self.meal_log
            if e.date == date_str
        ]
    # CRUD: журнал

    def add_activity(self, entry: "ActivityEntry"):
        self.activity_log.append(entry); self.save()

    def delete_activity(self, entry: "ActivityEntry"):
        if entry in self.activity_log:
            self.activity_log.remove(entry); self.save()

    def today_activities(self) -> list:
        today = datetime.date.today().isoformat()
        return [a for a in self.activity_log if a.date == today]

    def activities_by_date(self, date_str: str) -> list:
        return [a for a in self.activity_log if a.date == date_str]

    def burned_by_date(self, date_str: str) -> float:
        return sum(a.calories_burned for a in self.activities_by_date(date_str))

    def add_meal(self, entry: MealEntry):
        self.meal_log.append(entry); self.save()

    def delete_meal(self,  meal_entry):
        if meal_entry in self.meal_log:
            self.meal_log.remove(meal_entry)
            self.save()

    # CRUD: вага

    def add_weight(self, entry: WeightEntry):
        self.weight_log.append(entry)

        self.weight_log.sort(
            key=lambda x: x.date,
            reverse=True
        )

        self.save()

    def delete_weight(self, index: int):
        del self.weight_log[index]
        self.save()

    def latest_weight(self):
        if not self.weight_log:
            return None

        return self.weight_log[0].weight

    def weight_change(self):
        if len(self.weight_log) < 2:
            return 0

        return round(
            self.weight_log[0].weight - self.weight_log[1].weight,
            1
        )
    # Базові запити

    def today_entries(self) -> list[MealEntry]:
        today = datetime.date.today().isoformat()
        return [e for e in self.meal_log if e.date == today]

    def recalc_water_from_meals(self, date_str: str):
        # Перерахувати water_log для дати на основі записів напоїв у meal_log
        total = sum(
            e.grams
            for e in self.meal_log
            if e.date == date_str
            and self.get_food_by_name(e.food_name) is not None
            and getattr(self.get_food_by_name(e.food_name), "category", "") == "Напої"
        )
        self.water_log[date_str] = total
        self.save()

    def today_water(self) -> float:
        # Скільки мл випито сьогодні
        today = datetime.date.today().isoformat()
        return self.water_log.get(today, 0.0)

    def water_for_date(self, date_str: str) -> float:
        # Скільки мл випито для вказаної дати
        return self.water_log.get(date_str, 0.0)

    def add_water(self, ml: float):
        # Додати мл до сьогоднішнього лічильника
        today = datetime.date.today().isoformat()
        self.water_log[today] = self.water_log.get(today, 0.0) + ml
        self.save()

    def reset_water(self):
        # Скинути воду за сьогодні
        today = datetime.date.today().isoformat()
        self.water_log[today] = 0.0
        self.save()

    def categories(self) -> list[str]:
        return ["__all__"] + sorted({f.category for f in self.food_items})

    # Аналітичні запити

    def top_foods(self, n: int = 5) -> list[tuple[str, int]]:
        """ТОП-N продуктів за кількістю вживань."""
        from collections import Counter
        counts = Counter(e.food_name for e in self.meal_log)
        return counts.most_common(n)

    def calories_vs_burned_by_date(self, days: int = 7) -> list[tuple[str, float, float, float]]:
        # За кожен з останніх N днів: (дата, спожито, спалено, дефіцит/профіцит)
        today = datetime.date.today()
        result = []
        for i in range(days - 1, -1, -1):
            d = (today - datetime.timedelta(days=i)).isoformat()
            consumed = sum(e.calories for e in self.meal_log if e.date == d)
            burned   = sum(e.calories_burned for e in self.activity_log if e.date == d)
            balance  = consumed - burned - self.daily_goal
            result.append((d, round(consumed, 1), round(burned, 1), round(balance, 1)))
        return result

    def activity_heatmap(self, weeks: int = 12) -> list[tuple[str, str]]:
        """
        Останні weeks*7 днів. Для кожного дня повертає (date_str, status):
        'diary'    - є записи їжі, але норма не перевищена
        'over'     - норма калорій перевищена
        'activity' - є активність, але немає їжі
        'both'     - є і їжа, і активність
        'empty'    - нічого немає
        """
        today = datetime.date.today()
        total_days = weeks * 7
        result = []
        for i in range(total_days - 1, -1, -1):
            d = (today - datetime.timedelta(days=i)).isoformat()
            has_food     = any(e.date == d for e in self.meal_log)
            has_activity = any(e.date == d for e in self.activity_log)
            calories     = sum(e.calories for e in self.meal_log if e.date == d)
            over_limit   = has_food and calories > self.daily_goal
            if over_limit:
                status = "over"
            elif has_food and has_activity:
                status = "both"
            elif has_food:
                status = "diary"
            elif has_activity:
                status = "activity"
            else:
                status = "empty"
            result.append((d, status))
        return result

    def calories_by_date(self, days: int = 7) -> list[tuple[str, float]]:
        # Калорії за кожен з останніх N днів (від старішого до новішого)
        today = datetime.date.today()
        result = []
        for i in range(days - 1, -1, -1):
            d = (today - datetime.timedelta(days=i)).isoformat()
            total = sum(e.calories for e in self.meal_log if e.date == d)
            result.append((d, total))
        return result

    def today_macros(self) -> dict[str, float]:
        # Сумарні БЖВ + клітковина (г) за сьогодні
        return self.macros_by_date(datetime.date.today().isoformat())

    def macros_by_date(self, date_str: str) -> dict[str, float]:
        # Сумарні БЖВ + клітковина (г) за вказану дату
        totals = {"proteins": 0.0, "fats": 0.0, "carbs": 0.0, "fiber": 0.0}
        for entry in self.entries_by_date(date_str):
            food = self.get_food_by_name(entry.food_name)
            if food:
                k = entry.grams / 100.0
                totals["proteins"] += food.proteins * k
                totals["fats"]     += food.fats     * k
                totals["carbs"]    += food.carbs     * k
                totals["fiber"]    += food.fiber     * k
        return {k: round(v, 1) for k, v in totals.items()}

    def calories_for_date(self, date_str: str) -> float:
        # Сума калорій за вказану дату
        return round(sum(e.calories for e in self.entries_by_date(date_str)), 1)

    def weekly_avg_calories(self) -> float:
        # Середнє добове споживання за останні 7 днів (без нульових)
        vals = [c for _, c in self.calories_by_date(7) if c > 0]
        return round(sum(vals) / len(vals), 1) if vals else 0.0

    def activity_by_date(self, days: int = 7) -> list[tuple[str, float, float]]:
        # Активність за кожен з останніх N днів: (дата, хвилини, ккал спалено)
        today = datetime.date.today()
        result = []
        for i in range(days - 1, -1, -1):
            d = (today - datetime.timedelta(days=i)).isoformat()
            minutes = sum(e.minutes for e in self.activity_log if e.date == d)
            burned  = sum(e.calories_burned for e in self.activity_log if e.date == d)
            result.append((d, round(minutes, 1), round(burned, 1)))
        return result

    def calculate_macro_goals(self):
        """
        Автоматичний розрахунок БЖВ і клітковини
        від добової норми калорій.
        """

        calories = self.daily_goal

        # співвідношення макронутрієнтів
        protein_ratio = 0.25
        fat_ratio = 0.30
        carbs_ratio = 0.45

        # розрахунок грамів
        proteins = (calories * protein_ratio) / 4
        fats = (calories * fat_ratio) / 9
        carbs = (calories * carbs_ratio) / 4

        # клітковина:
        # приблизно 14 г на кожні 1000 ккал
        fiber = (calories / 1000) * 14

        return {
            "proteins": round(proteins, 1),
            "fats": round(fats, 1),
            "carbs": round(carbs, 1),
            "fiber": round(fiber, 1),
        }