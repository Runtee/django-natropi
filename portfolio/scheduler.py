# myapp/scheduler.py
import schedule
import time
import threading
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import Portfolio  # Replace 'myapp' with your app name

def distribute_weekly_profit(investment_id):
    try:
        investment = Portfolio.objects.get(id=investment_id)
        weekly_profit = investment.calculate_weekly_profit()
        investment.user.main += weekly_profit
        investment.user.trade += weekly_profit
        investment.user.save()
        investment.send_weekly_profit_email(weekly_profit)
    except Portfolio.DoesNotExist:
        pass

def complete_investment(investment_id):
    try:
        investment = Portfolio.objects.get(id=investment_id)
        total_profit = (investment.amount * investment.portfolioadd.short_term) / 100
        remaining_profit = total_profit - (investment.get_horizon_weeks() - investment.get_remaining_weeks()) * investment.calculate_weekly_profit()

        investment.user.main += remaining_profit
        investment.user.portfolio += investment.amount
        investment.user.trade -= total_profit
        investment.user.save()
        investment.send_completion_email(remaining_profit)
    except Portfolio.DoesNotExist:
        pass

def schedule_weekly_profit(investment):
    weeks = investment.get_horizon_weeks()
    for week in range(1, weeks + 1):
        schedule.every(week).weeks.do(distribute_weekly_profit, investment.id)

def schedule_investment_completion(investment):
    horizon_weeks = investment.get_horizon_weeks()
    schedule.every(horizon_weeks).weeks.do(complete_investment, investment.id)

def schedule_investments():
    now = timezone.now()
    investments = Portfolio.objects.filter(status='1')  # Adjust the filter as needed
    for investment in investments:
        weeks_since_investment = (now - investment.created_at).days // 7
        horizon_weeks = investment.get_horizon_weeks()
        if weeks_since_investment < horizon_weeks:
            # Schedule remaining weekly profits
            for week in range(weeks_since_investment + 1, horizon_weeks + 1):
                schedule.every(week).weeks.do(distribute_weekly_profit, investment.id)
        else:
            # If the horizon has passed, complete the investment
            complete_investment(investment.id)

def run_scheduler():
    schedule.every().day.at("00:00").do(schedule_investments)  # Run scheduling every day at midnight

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler_thread():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
