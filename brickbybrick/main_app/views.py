from django.shortcuts import render
from .models import Set

# Create your views here.
# sets = [
#     {'name': 'The Lord of the Rings: Rivendell', 'id': '10316-1', 'pieces': 6164, 'minifigs': 21, 'image': 'https://images.brickset.com/sets/images/10316-1.jpg?202302060243'},
#     {'name': 'Millennium Falcon', 'id': '75192', 'pieces': 7541, 'minifigs': 7, 'image': 'https://images.brickset.com/sets/images/75192-1.jpg?201708310401'},
#     {'name': 'Imperial Star Destroyer', 'id': '75252', 'pieces': 4784, 'minifigs': 2, 'image': 'https://images.brickset.com/sets/images/75252-1.jpg?201909050158'},
#     {'name': 'Tantive IV', 'id': '75244', 'pieces': 1767, 'minifigs': 6, 'image': 'https://images.brickset.com/sets/images/75244-1.jpg?201904120858'},
#     {'name': 'Death Star', 'id': '10188', 'pieces': 3886, 'minifigs': 24, 'image': 'https://images.brickset.com/sets/images/10188-1.jpg?200807260532'},
#     {'name': 'X-Wing Starfighter', 'id': '9493-1','pieces': 559, 'minifigs': 4, 'image': 'https://images.brickset.com/sets/large/9493-1.jpg?201110150700'},
    
# ]
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sets_index(request):
    sets = Set.objects.all()
    return render(request, 'sets/index.html', {'sets': sets})
    