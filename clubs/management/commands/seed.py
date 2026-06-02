"""
Seed command: python manage.py seed
Creates sample data for demo purposes.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from presences.models import Utilisateur
from clubs.models import Club, ClubCategory, Membership, Announcement
from events.models import Event, EventRegistration
from notifications.models import Notification
import datetime


CATEGORIES = [
    {'name': 'Technologie & IA',     'slug': 'technologie', 'icon': 'fa-microchip',     'color': '#6366F1', 'order': 1},
    {'name': 'Sports',               'slug': 'sports',      'icon': 'fa-futbol',        'color': '#10B981', 'order': 2},
    {'name': 'Arts & Culture',       'slug': 'arts',        'icon': 'fa-palette',       'color': '#F59E0B', 'order': 3},
    {'name': 'Sciences',             'slug': 'sciences',    'icon': 'fa-flask',         'color': '#3B82F6', 'order': 4},
    {'name': 'Entrepreneuriat',      'slug': 'business',    'icon': 'fa-briefcase',     'color': '#8B5CF6', 'order': 5},
    {'name': 'Littérature',          'slug': 'litterature', 'icon': 'fa-book-open',     'color': '#EF4444', 'order': 6},
    {'name': 'Musique',              'slug': 'musique',     'icon': 'fa-music',         'color': '#EC4899', 'order': 7},
    {'name': 'Environnement',        'slug': 'environnement','icon':'fa-leaf',           'color': '#14B8A6', 'order': 8},
]

CLUBS_DATA = [
    {
        'name': 'Club IA & Robotique',
        'short_description': 'Explorons ensemble l\'intelligence artificielle et la robotique.',
        'description': '''Le Club IA & Robotique d'EMSI est un espace d'exploration et d'innovation dédié aux étudiants passionnés par les technologies de demain. Nous organisons des workshops, des hackathons et des compétitions de robotique. Notre mission est de créer une communauté apprenante où chaque membre peut développer ses compétences en machine learning, deep learning, computer vision et programmation de robots.

Rejoignez-nous pour participer à des projets réels, collaborer avec des professionnels du secteur et représenter EMSI lors de compétitions nationales et internationales.''',
        'category_slug': 'technologie',
        'is_featured': True,
        'tags': 'intelligence artificielle, robotique, machine learning, python, arduino',
        'contact_email': 'club-ia@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'EMSI Entrepreneurs',
        'short_description': 'Transformez vos idées en startups qui changent le monde.',
        'description': '''EMSI Entrepreneurs est le hub de l\'entrepreneuriat étudiant. Nous accompagnons les étudiants qui souhaitent créer leur propre entreprise, de l\'idéation au MVP. Nous organisons des pitchs, des visites de startups, des rencontres avec des investisseurs et des ateliers de business model canvas.

Que vous ayez une idée ou que vous cherchiez une équipe, EMSI Entrepreneurs est l\'endroit idéal pour concrétiser vos ambitions entrepreneuriales.''',
        'category_slug': 'business',
        'is_featured': True,
        'tags': 'startup, entrepreneuriat, innovation, business, investissement',
        'contact_email': 'entrepreneurs@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'Photo & Design Club',
        'short_description': 'Capturer, créer et inspirer à travers l\'art visuel.',
        'description': '''Le Photo & Design Club rassemble les passionnés de photographie, de design graphique et d\'arts visuels. Nous organisons des sorties photo, des expositions, des workshops Photoshop/Illustrator et des concours créatifs.

Notre club est ouvert à tous les niveaux, des débutants aux experts. Venez partager votre passion pour l\'art visuel et développer votre œil artistique dans une ambiance conviviale et créative.''',
        'category_slug': 'arts',
        'is_featured': True,
        'tags': 'photographie, design, graphisme, créativité, illustration',
        'contact_email': 'photo@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'Club de Développement Web',
        'short_description': 'Du code au déploiement, maîtrisez le web moderne.',
        'description': '''Le Club Dev Web d'EMSI est votre communauté pour apprendre et pratiquer les technologies web les plus récentes. React, Vue, Django, Node.js, Docker... Nous couvrons tout le stack moderne.

Chaque semaine, nous organisons des coding sessions, des code reviews et des mini-projets en équipe. Participez à nos hackathons mensuels et construisez votre portfolio avec de vrais projets.''',
        'category_slug': 'technologie',
        'is_featured': False,
        'tags': 'web, javascript, python, react, django, fullstack',
        'contact_email': 'devweb@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'Club Football EMSI',
        'short_description': 'Le football comme vecteur de cohésion et de dépassement.',
        'description': '''Le Club Football EMSI réunit les amoureux du ballon rond. Nous organisons des entraînements réguliers, des matchs inter-filières et des tournois inter-établissements. Rejoignez-nous pour partager la passion du football dans un esprit de fair-play et de camaraderie.''',
        'category_slug': 'sports',
        'is_featured': False,
        'tags': 'football, sport, équipe, tournoi, compétition',
        'contact_email': 'football@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'Green Campus',
        'short_description': 'Ensemble pour un campus plus vert et un avenir durable.',
        'description': '''Green Campus est le club environnemental d'EMSI. Nous sensibilisons la communauté étudiante aux enjeux écologiques et organisons des actions concrètes : collectes de déchets, jardinage urbain, conférences sur le développement durable et initiatives de réduction de l\'empreinte carbone.''',
        'category_slug': 'environnement',
        'is_featured': True,
        'tags': 'environnement, écologie, développement durable, recyclage',
        'contact_email': 'green@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'Club Cybersécurité',
        'short_description': 'Protégeons le monde numérique, une vulnérabilité à la fois.',
        'description': '''Le Club Cybersécurité d\'EMSI est dédié à la sécurité informatique. CTF, pentesting éthique, reverse engineering, cryptographie... Nous explorons tous les aspects de la cybersécurité dans un cadre légal et éthique. Participez à des compétitions CTF nationales et internationales sous la bannière EMSI.''',
        'category_slug': 'technologie',
        'is_featured': False,
        'tags': 'cybersécurité, CTF, hacking éthique, réseau, cryptographie',
        'contact_email': 'cyber@emsi.ma',
        'status': 'approved',
    },
    {
        'name': 'EMSI Music Band',
        'short_description': 'La musique qui unit les âmes et fait vibrer le campus.',
        'description': '''EMSI Music Band rassemble les étudiants musiciens et mélomanes. Instruments, chant, composition, production musicale... Nous créons ensemble et nous performons lors des événements du campus. Rejoignez-nous que vous soyez débutant ou musicien confirmé.''',
        'category_slug': 'musique',
        'is_featured': False,
        'tags': 'musique, guitare, chant, performance, composition',
        'contact_email': 'music@emsi.ma',
        'status': 'approved',
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with sample data for ClubHub'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n*** Seeding ClubHub database...\n'))

        # Users
        admin = self._get_or_create_user(
            'admin_clubhub', 'admin@emsi.ma', 'Admin123!',
            'Platform', 'Admin', 'admin', 'EMSI Casablanca'
        )
        manager1 = self._get_or_create_user(
            'sara.alami', 'sara.alami@emsi.ma', 'Sara123!',
            'Sara', 'Alami', 'club_manager', 'EMSI Casablanca'
        )
        manager2 = self._get_or_create_user(
            'karim.fassi', 'karim.fassi@emsi.ma', 'Karim123!',
            'Karim', 'Fassi', 'club_manager', 'EMSI Casablanca'
        )
        manager3 = self._get_or_create_user(
            'leila.benjelloun', 'leila.b@emsi.ma', 'Leila123!',
            'Leïla', 'Benjelloun', 'club_manager', 'EMSI Casablanca'
        )
        students = []
        student_data = [
            ('ali.benali', 'ali.benali@emsi.ma', 'Ali', 'Benali'),
            ('fatima.zohra', 'fatima.z@emsi.ma', 'Fatima', 'Zohra'),
            ('youssef.elidrissi', 'youssef.e@emsi.ma', 'Youssef', 'El Idrissi'),
            ('nadia.cherkaoui', 'nadia.c@emsi.ma', 'Nadia', 'Cherkaoui'),
            ('omar.benkirane', 'omar.b@emsi.ma', 'Omar', 'Benkirane'),
            ('ines.tahiri', 'ines.t@emsi.ma', 'Inès', 'Tahiri'),
            ('mehdi.bakkali', 'mehdi.b@emsi.ma', 'Mehdi', 'Bakkali'),
            ('zineb.lahlou', 'zineb.l@emsi.ma', 'Zineb', 'Lahlou'),
        ]
        for username, email, fn, ln in student_data:
            s = self._get_or_create_user(username, email, 'Student123!', fn, ln, 'etudiant', 'EMSI Casablanca')
            students.append(s)

        self.stdout.write(f'  [OK] {1 + 3 + len(students)} users created/verified')

        # Categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, _ = ClubCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'display_order': cat_data['order'],
                }
            )
            cat_map[cat_data['slug']] = cat
        self.stdout.write(f'  [OK] {len(cat_map)} categories created/verified')

        # Clubs
        managers = [manager1, manager2, manager3, admin, manager1, manager2, manager3, manager1]
        clubs = []
        for i, club_data in enumerate(CLUBS_DATA):
            manager = managers[i % len(managers)]
            club, created = Club.objects.get_or_create(
                name=club_data['name'],
                defaults={
                    'slug': slugify(club_data['name']),
                    'short_description': club_data['short_description'],
                    'description': club_data['description'],
                    'category': cat_map.get(club_data['category_slug']),
                    'created_by': manager,
                    'status': club_data['status'],
                    'is_featured': club_data['is_featured'],
                    'tags': club_data['tags'],
                    'contact_email': club_data['contact_email'],
                    'is_public': True,
                }
            )
            if created:
                Membership.objects.get_or_create(
                    user=manager, club=club,
                    defaults={'role': 'owner', 'status': 'approved', 'joined_at': timezone.now()}
                )
            clubs.append(club)

        self.stdout.write(f'  [OK] {len(clubs)} clubs created/verified')

        # Memberships for students
        membership_count = 0
        for student in students:
            for club in clubs[:5]:
                m, created = Membership.objects.get_or_create(
                    user=student, club=club,
                    defaults={'role': 'member', 'status': 'approved', 'joined_at': timezone.now()}
                )
                if created:
                    membership_count += 1

        # Pending requests
        for student in students[5:]:
            for club in clubs[5:]:
                Membership.objects.get_or_create(
                    user=student, club=club,
                    defaults={'role': 'member', 'status': 'pending', 'join_message': 'Bonjour, je suis très intéressé par les activités de votre club !'}
                )
        self.stdout.write(f'  [OK] {membership_count} memberships created')

        # Events
        today = timezone.now().date()
        events_data = [
            {
                'club': clubs[0],
                'title': 'Workshop Machine Learning avec Python',
                'description': 'Apprenez les bases du machine learning avec scikit-learn et TensorFlow. De la théorie à la pratique, nous couvrirons la régression, la classification et les réseaux de neurones. Apportez votre ordinateur portable !',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=7),
                'start_time': datetime.time(14, 0),
                'end_time': datetime.time(18, 0),
                'location': 'Amphi A — EMSI Casablanca',
                'capacity': 40,
                'status': 'published',
                'is_featured': True,
                'tags': 'machine learning, python, tensorflow, workshop',
                'created_by': manager1,
            },
            {
                'club': clubs[1],
                'title': 'Pitch Night : Présentez votre startup',
                'description': 'Rejoignez-nous pour la soirée pitch la plus excitante de l\'année ! Des étudiants-entrepreneurs présenteront leurs projets devant un jury de professionnels. Networking et échanges au programme.',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=14),
                'start_time': datetime.time(18, 30),
                'end_time': datetime.time(21, 0),
                'location': 'Espace Innovation EMSI — Salle B201',
                'capacity': 80,
                'status': 'published',
                'is_featured': True,
                'tags': 'startup, pitch, entrepreneuriat, investissement',
                'created_by': manager2,
            },
            {
                'club': clubs[2],
                'title': 'Exposition Photo : "Visages du Campus"',
                'description': 'Venez découvrir l\'exposition photographique annuelle du Photo & Design Club. Cette année, le thème est "Visages du Campus" — des portraits saisissants de la vie universitaire à EMSI.',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=21),
                'start_time': datetime.time(10, 0),
                'end_time': datetime.time(17, 0),
                'location': 'Hall principal EMSI',
                'capacity': 0,
                'status': 'published',
                'is_featured': False,
                'tags': 'photographie, exposition, art, créativité',
                'created_by': manager3,
            },
            {
                'club': clubs[6],
                'title': 'CTF Challenge — HackEMSI 2025',
                'description': 'Participez au premier Capture The Flag organisé par EMSI ! Des challenges de cybersécurité de différents niveaux : web, forensics, crypto, pwn et reverse. Des prix pour les 3 premiers équipes.',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=30),
                'start_time': datetime.time(9, 0),
                'end_time': datetime.time(20, 0),
                'location': 'Salle Info — EMSI Casablanca',
                'capacity': 60,
                'status': 'published',
                'is_featured': True,
                'tags': 'CTF, cybersécurité, hacking, compétition',
                'created_by': manager1,
            },
            {
                'club': clubs[5],
                'title': 'Journée de nettoyage du campus',
                'description': 'Ensemble, faisons de notre campus un espace plus propre et plus vert ! Rejoignez Green Campus pour une journée d\'action écologique. Gants et sacs fournis. Goûter bio offert !',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=10),
                'start_time': datetime.time(9, 0),
                'end_time': datetime.time(13, 0),
                'location': 'Campus EMSI — Point de RDV : Entrée principale',
                'capacity': 100,
                'status': 'published',
                'is_featured': False,
                'tags': 'écologie, nettoyage, environnement, campus',
                'created_by': manager2,
            },
            {
                'club': clubs[3],
                'title': 'Hackathon Web 24h — Web3Challenge',
                'description': '24 heures pour concevoir, développer et déployer une application web complète. Travaillez en équipes de 2 à 4 personnes. Technologies libres. Mentors disponibles tout au long de l\'événement.',
                'event_type': 'in_person',
                'date': today + datetime.timedelta(days=45),
                'start_time': datetime.time(10, 0),
                'end_time': datetime.time(10, 0),
                'location': 'Labo Informatique L3 — EMSI',
                'capacity': 50,
                'status': 'published',
                'is_featured': False,
                'tags': 'hackathon, web, développement, compétition',
                'created_by': manager3,
            },
        ]

        event_objects = []
        for ev_data in events_data:
            ev, created = Event.objects.get_or_create(
                title=ev_data['title'],
                defaults={
                    **{k: v for k, v in ev_data.items() if k != 'title'},
                }
            )
            event_objects.append(ev)

        # Register some students for events
        for student in students[:6]:
            for event in event_objects[:4]:
                EventRegistration.objects.get_or_create(
                    user=student, event=event,
                    defaults={'status': 'registered'}
                )
        self.stdout.write(f'  [OK] {len(event_objects)} events created/verified')

        # Announcements
        for club in clubs[:4]:
            ann, created = Announcement.objects.get_or_create(
                club=club,
                title=f'Bienvenue dans {club.name} !',
                defaults={
                    'content': f'Nous sommes ravis de vous accueillir dans le {club.name}. Restez connectés pour les dernières nouvelles, événements et activités du club. N\'hésitez pas à contacter les responsables pour toute question.',
                    'author': club.created_by,
                    'is_pinned': True,
                }
            )
        self.stdout.write(f'  [OK] Announcements created')

        self.stdout.write(self.style.SUCCESS('\n[DONE] Database seeded successfully!\n'))
        self.stdout.write('Credentials:')
        self.stdout.write('  Admin:    admin@emsi.ma / Admin123!')
        self.stdout.write('  Manager:  sara.alami@emsi.ma / Sara123!')
        self.stdout.write('  Student:  ali.benali@emsi.ma / Student123!\n')

    def _get_or_create_user(self, username, email, password, fn, ln, role, uni=''):
        user, created = Utilisateur.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': fn,
                'last_name': ln,
                'role': role,
                'university': uni,
                'is_active': True,
            }
        )
        if created:
            user.set_password(password)
            user.save()
        return user
