import os
import django
from django.db.models import Count

from main_app.models import Astronaut, Mission

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


def get_astronauts(search_string: str | None) -> str:
    if not search_string:
        return ""

    astronauts = Astronaut.objects.filter(name__icontains=search_string)

    lines = [
        f"Astronaut: {a.name}, phone number: {a.phone_number}, "
        f"status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    ]

    return "\n".join(lines)



def get_top_astronaut() -> str:
    top_astronaut = (
        Astronaut.objects
        .annotate(mission_count=Count('missions'))
        .order_by('-mission_count', 'phone_number')
        .first()
    )

    if not top_astronaut:
        return "No astronauts available."

    return (
        f"Top Astronaut: {top_astronaut.name} "
        f"with {top_astronaut.mission_count} missions."
    )

def get_top_commander():
    top_commander: Astronaut = (Astronaut.objects
                                .annotate(c=Count('commander_missions'))
                                .order_by('-c', 'phone_number')
                                .first())
    if not top_commander:
        return 'No data'

    return f'Top commander: {top_commander.name} with {top_commander.c} missions.'


def get_last_completed_mission() -> str:
    lcm = (
        Mission.objects
        .filter(status='Completed')
        .order_by('-launch_date')
        .first()
    )

    if not lcm:
        return "No completed missions."

    astronauts = list(lcm.astronauts.all())

    total_spacewalks = sum(a.spacewalks for a in astronauts)

    if lcm.commander and lcm.commander not in astronauts:
        total_spacewalks += lcm.commander.spacewalks

    commander_name = lcm.commander.name if lcm.commander else "TBA"
    astronaut_names = ", ".join(a.name for a in astronauts)

    return (
        f"The last completed mission is: {lcm.name}. "
        f"Commander: {commander_name}. "
        f"Astronauts: {astronaut_names}. "
        f"Spacecraft: {lcm.spacecraft.name}. "
        f"Total spacewalks: {total_spacewalks}."
    )
