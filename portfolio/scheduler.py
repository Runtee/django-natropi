from decimal import Decimal
import schedule
import time
import threading
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Portfolio

User = get_user_model()

def distribute_weekly_profit(investment_id):
    try:
        investment = Portfolio.objects.get(id=investment_id)
        user = investment.user  # Get the user object

        print(f"Distributing weekly profit for investment ID: {investment_id}")
        print(f"Initial user balances - Main: {user.main}, Trade: {user.trade}")

        if investment.status == '1' and investment.days_passed % 7 == 0 and investment.days_passed < investment.get_horizon_days():
            weekly_profit = investment.calculate_weekly_profit()
            print(f"Calculated weekly profit: {weekly_profit}")

            user.main += weekly_profit
            print(f"Updated main balance: {user.main}")

            user.trade += weekly_profit
            print(f"Updated trade balance: {user.trade}")

            try:
                user.save()
                print("User balances saved")
            except Exception as e:
                print(f"Error saving user balances: {str(e)}")

            # Refresh the user object to ensure it's updated
            user.refresh_from_db()
            print(f"Refreshed user balances - Main: {user.main}, Trade: {user.trade}")

            investment.send_weekly_profit_email(weekly_profit)
            investment.days_passed += 7
            try:
                investment.save()
                print("Investment days_passed updated and saved")
            except Exception as e:
                print(f"Error saving investment: {str(e)}")

            print("Distributed weekly profit and updated investment days_passed")
        else:
            print("Conditions not met for distributing weekly profit")
    except Portfolio.DoesNotExist:
        print(f"Portfolio with ID {investment_id} does not exist")
    except Exception as e:
        print(f"Error in distributing weekly profit: {str(e)}")

def complete_investment(investment_id):
    try:
        investment = Portfolio.objects.get(id=investment_id)
        user = investment.user  # Get the user object

        if investment.status == '1' and investment.days_passed >= investment.get_horizon_days():
            total_profit = (Decimal(investment.amount) * Decimal(investment.portfolioadd.short_term)) / 100
            total_weekly_profit = (investment.days_passed // 7) * investment.calculate_weekly_profit()
            remaining_profit = total_profit - total_weekly_profit
            
            user.main += remaining_profit
            user.portfolio += Decimal(investment.amount)
            user.trade -= total_weekly_profit
            if user.trade < 0:
                user.trade = 0
            user.save()
            investment.send_completion_email(total_profit)
            investment.status = '2'  # Indicate completion
            investment.save()
            print('Completed investment')
    except Portfolio.DoesNotExist:
        pass
    except Exception as e:
        print(f"Error in completing investment: {str(e)}")

def schedule_weekly_profit(investment):
    if investment.status == '1':
        # Check every minute for testing
        schedule.every().week.do(distribute_weekly_profit, investment.id)

def schedule_investment_completion(investment):
    if investment.status == '1':
        # Check every minute for testing
        schedule.every().day.at("00:00").do(complete_investment, investment.id)

def schedule_investments():
    investments = Portfolio.objects.filter(status='1')
    for investment in investments:
        schedule_weekly_profit(investment)
        schedule_investment_completion(investment)

def run_scheduler():
    schedule_investments()
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler_thread():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
