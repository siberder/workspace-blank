class FoodDiary:
    def __init__(self):
        self.entries = []
        self.goals = {
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbohydrates': 0
        }

    def add_entry(self, calories, protein=0, fat=0, carbohydrates=0):
        entry = {
            'calories': calories,
            'protein': protein,
            'fat': fat,
            'carbohydrates': carbohydrates
        }
        self.entries.append(entry)

    def edit_entry(self, index, calories=None, protein=None, fat=None, carbohydrates=None):
        if 0 <= index < len(self.entries):
            if calories is not None:
                self.entries[index]['calories'] = calories
            if protein is not None:
                self.entries[index]['protein'] = protein
            if fat is not None:
                self.entries[index]['fat'] = fat
            if carbohydrates is not None:
                self.entries[index]['carbohydrates'] = carbohydrates

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)

    def calculate_daily_calories(self):
        return sum(entry['calories'] for entry in self.entries)

    def set_goal(self, calories, protein, fat, carbohydrates):
        self.goals = {
            'calories': calories,
            'protein': protein,
            'fat': fat,
            'carbohydrates': carbohydrates
        }

    def track_goal(self):
        total_calories = self.calculate_daily_calories()
        total_protein = sum(entry['protein'] for entry in self.entries)
        total_fat = sum(entry['fat'] for entry in self.entries)
        total_carbohydrates = sum(entry['carbohydrates'] for entry in self.entries)
        return {
            'calories': total_calories,
            'protein': total_protein,
            'fat': total_fat,
            'carbohydrates': total_carbohydrates
        }

    def view_previous_days(self, days):
        from datetime import datetime, timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        previous_entries = []
        for entry in self.entries:
            entry_date = datetime.strptime(entry['date'], '%Y-%m-%d')
            if start_date <= entry_date <= end_date:
                previous_entries.append(entry)

        return previous_entries
