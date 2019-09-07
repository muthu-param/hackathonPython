from django_cron import CronJobBase, Schedule

from datetime import datetime, timedelta


class generateNotification (CronJobBase):
    RUN_EVERY_MINS = 0.01  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'notification'    # a unique code

    def do(self):

        print '*** cron for alert user ***  -- '+str(datetime.now())
        try:
            # For Start alert
            from_date = datetime.now()
            last_time = from_date.replace(hour=18, minute=59, second=59)

            bookings = Booking.objects.filter(
                startTime__range=[from_date, last_time]).values()
                
            return success_response(list(bookings))
        except Exception as e:
            fail['msg'] = str(e)
            return failure_response(fail)
