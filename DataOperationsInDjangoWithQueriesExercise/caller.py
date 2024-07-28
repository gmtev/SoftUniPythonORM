import os
import django
from django.db.models import F

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Character, Car, Task, HotelRoom


def create_pet(name, species):
    pet = Pet.objects.create(name=name, species=species)

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk=artifact.pk).update(name=new_name)
    # since there is no reason to filter for only one given object and because of the "Judge" system
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    # could be done with adding a __str__ in the class itself; it isn't mentioned in the exercise, so I'm not doing
    # that in order to not mess with Judge
    return '\n'.join(f"{location.name} has a population of {location.population}!" for location in locations)


def new_capital():
    # could be slightly optimised with Location.objects.filter(id=1).update(is_capital=True), though if the first record
    # is deleted then it wouldn't work due to the id no longer being "1"
    first = Location.objects.first()
    first.is_capital = True
    first.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        percentage = sum(int(digit) for digit in str(car.year)) / 100
        discount = float(car.price) * percentage
        car.price_with_discount = float(car.price) - discount
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(str(task) for task in unfinished_tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True
    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text, task_title):
    encoded = ''.join(chr(ord(symbol)-3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=encoded)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_deluxe_rooms = [str(room) for room in deluxe_rooms if room.id % 2 == 0]
    return '\n'.join(even_deluxe_rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_capacity = None
    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_capacity is not None:
            room.capacity += previous_capacity
        else:
            room.capacity += room.id
        previous_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()


def update_characters():
    Character.objects.filter(class_name="Mage").update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name="Warrior").update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character, second_character):
    fusion_name = first_character.name + second_character.name
    class_name = 'Fusion'
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = (first_character.hit_points + second_character.hit_points)
    if first_character.class_name in ['Assassin','Warrior']:
        inventory = "Dragon Scale Armor, Excalibur"
    else:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"

    Character.objects.create(
        name=fusion_name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory)
    first_character.delete()
    second_character.delete()


def grant_dexterity():
    Character.objects.update(dexterity=30)


def grant_intelligence():
    Character.objects.update(intelligence=40)


def grant_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()