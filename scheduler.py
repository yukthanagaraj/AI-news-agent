

import schedule
import time

from agents.orchestrator_agent import run_pipeline

def safe_run():

    try:

        run_pipeline()

    except Exception as e:

        print(

            "Pipeline Error:",

            e

        )

schedule.every().day.at(

    "09:00"

).do(

    safe_run

)

print(

    "Scheduler Running... Waiting for 9 AM"

)

while True:

    schedule.run_pending()

    time.sleep(

        60

    )