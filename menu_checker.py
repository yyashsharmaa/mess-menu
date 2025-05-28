import pandas as pd
import datetime

def load_menu():
    df = pd.read_excel('menu.xlsx')
    df.columns = df.columns.str.strip()
    df = df.melt(id_vars='Day', var_name='Meal', value_name='Items')

    meal_times = {
        'Breakfast': '12:00 AM - 9:30 AM',
        'Lunch': '9:31 AM - 2:00 PM',
        'Dinner': '2:01 PM - 11:59 PM'
    }
    df['Time'] = df['Meal'].map(meal_times)

    df['Day'] = df['Day'].str.strip().str.lower()
    df['Meal'] = df['Meal'].str.strip().str.lower()

    return df

def get_menu(day, meal):
    day = day.strip().lower()
    meal = meal.strip().lower()

    df = load_menu()
    result = df[(df['Day'] == day) & (df['Meal'] == meal)]

    if result.empty:
        return f"No menu found for {day.title()} {meal.title()}."
    else:
        items = result['Items'].values[0]
        time = result['Time'].values[0]
        return f"Menu for {day.title()} {meal.title()} ({time}):\n{items}"

def get_current_meal():
    now = datetime.datetime.now().time()

    if datetime.time(0, 0) <= now <= datetime.time(9, 30):
        return 'breakfast'
    elif datetime.time(9, 31) <= now <= datetime.time(14, 0):
        return 'lunch'
    else:
        return 'dinner'

if __name__ == "__main__":
    today = datetime.datetime.now().strftime('%A').lower()
    current_meal = get_current_meal()

    menu = get_menu(today, current_meal)
    print(menu)
