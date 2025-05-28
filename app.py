from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def load_menu():
    df = pd.read_excel('menu.xlsx')
    df.columns = df.columns.str.strip().str.lower()
    df = df.fillna('')
    return df

def get_current_meal():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day = now.strftime('%A').lower()
    
    if hour < 9 or (hour == 9 and minute <= 30):
        meal = 'breakfast'
    elif hour < 14 or (hour == 14 and minute == 0):
        meal = 'lunch'
    else:
        meal = 'dinner'
    
    return day, meal

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_menu()
    message = None

    if request.method == 'POST':
        day = request.form['day'].strip().lower()
        meal = request.form['meal'].strip().lower()
    else:
        day, meal = get_current_meal()

    try:
        menu_item = df[df['day'].str.lower() == day][meal].values[0]
    except IndexError:
        menu_item = "Menu not available."

    return render_template('index.html', day=day.capitalize(), meal=meal.capitalize(), menu=menu_item)

if __name__ == '__main__':
    app.run(debug=True)
