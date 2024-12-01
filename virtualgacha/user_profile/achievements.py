from inventory.models import Inventory
from adventure.models import AdventureUser, Adventure, AdventurePet
from daily_rewards.models import UserReward
from django.utils import timezone
from datetime import timedelta

achievements = {
    'General Achievements': [
        {
            "name": "Officially a Pet Collector",
            "description": "Own your first pet.",
            "badge": '<svg fill="#000000" height="64px" width="64px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-147 -147 784.00 784.00" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"><rect x="-147" y="-147" width="784.00" height="784.00" rx="0" fill="#ffffff" strokewidth="0"></rect></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <g> <path d="M345,70c11.028,0,20-8.972,20-20V10c0-5.522-4.477-10-10-10H135c-5.523,0-10,4.478-10,10v40c0,11.028,8.972,20,20,20h10 v220.635c-19.372,21.94-30,49.961-30,79.365c0,66.168,53.832,120,120,120s120-53.832,120-120c0-29.405-10.628-57.425-30-79.364 V70H345z M345,370c0,55.141-44.86,100-100,100s-100-44.859-100-100c0-25.634,9.685-50.009,27.29-68.655 C191.27,281.132,217.092,270,245,270s53.73,11.132,72.71,31.345c0.006,0.007,0.013,0.014,0.019,0.021 C335.315,319.991,345,344.366,345,370z M215,200V70h20v150h20V70h20v130h20V70h20v202.438C294.836,257.854,270.65,250,245,250 c-25.654,0-49.843,7.856-70,22.434V70h20v130H215z M145,50V20h200v30H145z"></path> <path d="M245,285c-46.869,0-85,38.131-85,85c0,46.869,38.131,85,85,85s85-38.131,85-85C330,323.131,291.869,285,245,285z M245,435c-35.841,0-65-29.159-65-65s29.159-65,65-65s65,29.159,65,65S280.841,435,245,435z"></path> <path d="M255,345c0-5.522-4.477-10-10-10h-20v20h10v30h-10v20h40v-20h-10V345z"></path> </g> </g> </g> </g></svg>',
            "condition": lambda user: Inventory.objects.filter(owner_id=user).exists(),
            #okie
        }, {
            "name": "Adventure Rookie",
            "description": "Send a pet on an adventure.",
            "badge": '<svg height="64px" width="64px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-153.6 -153.6 819.20 819.20" xml:space="preserve" fill="#ED0685"><g id="SVGRepo_bgCarrier" stroke-width="0"><rect x="-153.6" y="-153.6" width="819.20" height="819.20" rx="81.92" fill="#ffffff" strokewidth="0"></rect></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <polygon style="fill:#222077;" points="401.664,427.752 194.048,427.752 194.048,162.616 101.392,162.616 101.392,283.592 0,283.592 0,251.592 69.392,251.592 69.392,130.616 226.048,130.616 226.048,395.752 369.664,395.752 369.664,242.28 401.664,242.28 "></polygon> <polygon style="fill:#ED0685;" points="386.512,84.248 416.144,179.88 512,179.88 434.448,238.984 464.064,334.648 386.512,275.512 308.944,334.648 338.576,238.984 261.024,179.88 356.88,179.88 "></polygon> </g></svg>',
            "condition": lambda user: AdventureUser.objects.filter(user_id=user).exists(),
            #okie
        }, {
            "name": "Rookie Collector",
            "description": "Own 5 pets.",
            "badge": '<svg fill="#1A1D45" height="64px" width="64px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-153.6 -153.6 819.20 819.20" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0" transform="translate(0,0), scale(1)"><rect x="-153.6" y="-153.6" width="819.20" height="819.20" rx="81.92" fill="#ffffff" strokewidth="0"></rect></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#CCCCCC" stroke-width="4.095976"></g><g id="SVGRepo_iconCarrier"> <g> <g> <g> <path d="M377.411,412.052c-11.768,0-21.34,9.573-21.34,21.34v31.631c0,11.767,9.572,21.339,21.34,21.339 c11.767,0,21.339-9.572,21.339-21.339v-31.631C398.75,421.625,389.177,412.052,377.411,412.052z M382.55,465.022 c0,2.834-2.306,5.139-5.139,5.139c-2.834,0-5.14-2.306-5.14-5.139v-31.631c0-2.834,2.306-5.14,5.14-5.14 c2.833,0,5.139,2.306,5.139,5.14V465.022z"></path> <path d="M403.073,384.359h-6.144c0.981-0.942,1.9-1.964,2.748-3.058c4.539-5.861,6.524-13.139,5.59-20.494 c-1.575-12.377-11.13-21.834-22.831-23.853l-62.159-10.865l60.956-7.747c7.354-0.935,13.904-4.678,18.443-10.539 c4.539-5.861,6.524-13.139,5.59-20.494c-1.554-12.22-10.976-21.772-22.757-23.831l0.002-0.009l-62.236-10.878l60.956-7.747 c7.355-0.934,13.905-4.677,18.444-10.538c4.539-5.861,6.524-13.139,5.59-20.493c-1.719-13.521-13.067-23.762-26.585-24.215 l-59.385-10.379l61.937-7.872c7.355-0.935,13.904-4.677,18.443-10.539c4.539-5.861,6.524-13.139,5.59-20.494 c-1.758-13.828-13.583-24.257-27.507-24.257c-0.286,0-0.572,0.018-0.86,0.027l-58.582-10.24l62.915-7.996 c7.354-0.935,13.904-4.678,18.443-10.538c4.539-5.861,6.524-13.139,5.59-20.493c-1.554-12.224-10.976-21.776-22.756-23.833 l0.001-0.008L139.047,0.423c-7.313-1.28-14.668,0.367-20.733,4.628c-6.065,4.261-10.109,10.63-11.385,17.933 c-1.278,7.303,0.367,14.666,4.628,20.732c4.262,6.066,10.631,10.11,17.934,11.387l62.237,10.878l-60.957,7.747 c-7.355,0.934-13.904,4.678-18.443,10.538c-4.54,5.861-6.525,13.141-5.591,20.494c1.557,12.257,11.03,21.825,22.857,23.846 l-0.103,0.586l60.277,10.536l-58.998,7.498c-15.183,1.93-25.964,15.851-24.034,31.031c1.556,12.241,11.003,21.801,22.807,23.84 l-0.052,0.297l61.256,10.706l-59.976,7.623c-7.355,0.934-13.904,4.676-18.443,10.538c-4.54,5.862-6.525,13.141-5.591,20.493 c1.553,12.223,10.976,21.775,22.757,23.832l-0.002,0.009l62.235,10.878l-60.956,7.747c-15.182,1.93-25.964,15.851-24.034,31.032 c1.553,12.223,10.975,21.775,22.756,23.832l-0.001,0.009l62.235,10.878l-60.955,7.747c-9.92,1.26-18.217,7.764-22.021,16.651 c-10.578,0.097-19.154,8.723-19.154,19.323v88.978c0,10.66,8.671,19.331,19.331,19.331h294.147 c10.66,0,19.331-8.671,19.331-19.331v-88.978C422.405,393.031,413.733,384.359,403.073,384.359z M132.278,39.144 c-3.04-0.531-5.693-2.215-7.466-4.74c-1.774-2.525-2.458-5.59-1.927-8.63s2.215-5.692,4.74-7.465 c2.525-1.773,5.587-2.458,8.631-1.927l187.655,32.8l-77.705,9.876L132.278,39.144z M134.243,112.816 c-5.788,0-10.705-4.342-11.436-10.099c-0.389-3.062,0.436-6.092,2.326-8.532c1.89-2.44,4.617-3.998,7.678-4.388l243.469-30.942 c0.492-0.063,0.993-0.095,1.483-0.095c0.665,0,1.319,0.064,1.955,0.174l0.004,0.001c4.901,0.851,8.825,4.831,9.473,9.925 c0.389,3.061-0.436,6.091-2.326,8.531c-1.89,2.44-4.617,3.998-7.678,4.388l-243.469,30.942 C135.231,112.784,134.733,112.816,134.243,112.816z M186.13,122.645l78.505-9.977l-0.041,0.233l57.355,10.025l-77.706,9.877 L186.13,122.645z M134.243,186.314c-5.788,0-10.705-4.343-11.436-10.1c-0.804-6.32,3.685-12.115,10.005-12.918l111.049-14.114 l0.756,0.132l0.041-0.233l131.386-16.698l3.677,0.643l0.102-0.578c4.855,0.889,8.728,4.852,9.371,9.91 c0.389,3.061-0.436,6.091-2.326,8.531c-1.89,2.441-4.617,3.999-7.678,4.388l-243.469,30.942 C135.228,186.283,134.731,186.314,134.243,186.314z M187.111,196.018l77.708-9.877l58.112,10.158l-77.706,9.877L187.111,196.018z M122.807,249.712c-0.389-3.062,0.436-6.091,2.326-8.531c1.89-2.44,4.617-3.998,7.678-4.388l243.466-30.942 c0.314-0.04,0.631-0.045,0.945-0.06l2.499,0.436l0.051-0.288c4.88,0.87,8.776,4.842,9.422,9.918 c0.389,3.062-0.436,6.091-2.326,8.53c-1.89,2.44-4.617,3.998-7.678,4.388l-243.459,30.942 C129.328,260.526,123.599,255.955,122.807,249.712z M188.09,269.392l77.707-9.877l58.113,10.158l-77.706,9.877L188.09,269.392z M134.243,333.309c-5.788,0-10.705-4.342-11.436-10.099c-0.804-6.32,3.685-12.116,10.005-12.919l243.464-30.942 c0.492-0.063,0.99-0.094,1.48-0.094c5.79,0,10.707,4.342,11.44,10.099c0.389,3.062-0.436,6.091-2.326,8.531 c-1.89,2.441-4.617,3.998-7.678,4.388l-243.47,30.942C135.231,333.277,134.733,333.309,134.243,333.309z M188.09,342.889 l77.706-9.877l58.113,10.158l-77.707,9.877L188.09,342.889z M132.811,383.788l243.463-30.943c1.176-0.15,2.333-0.114,3.443,0.08 l0.004,0.001c4.858,0.852,8.818,4.783,9.473,9.924c0.389,3.062-0.436,6.091-2.326,8.531c-1.89,2.44-4.617,3.998-7.678,4.388 l-67.591,8.59H130.44C131.198,384.093,131.99,383.893,132.811,383.788z M403.073,495.799H108.925 c-1.697,0-3.131-1.434-3.131-3.131v-88.978c0-1.697,1.434-3.131,3.131-3.131h294.147c1.697,0,3.131,1.434,3.131,3.131v88.978 h0.001C406.204,494.365,404.77,495.799,403.073,495.799z"></path> <path d="M309.909,411.142H202.091c-8.801,0-15.962,7.161-15.962,15.962v42.152c0,8.801,7.161,15.962,15.962,15.962h107.818 c8.801,0,15.962-7.161,15.962-15.962v-42.152C325.871,418.302,318.71,411.142,309.909,411.142z M309.671,469.016H202.329v-41.674 h107.342V469.016z"></path> <path d="M227.921,456.28h56.159c4.474,0,8.1-3.627,8.1-8.1c0-4.473-3.626-8.1-8.1-8.1h-56.159c-4.474,0-8.1,3.627-8.1,8.1 C219.821,452.653,223.447,456.28,227.921,456.28z"></path> </g> </g> </g> </g></svg>',
            "condition": lambda user: Inventory.objects.filter(owner_id=user).count() >= 5,
            #okie
        }, {
            "name": "Showcase Star",
            "description": "Showcase a pet for the first time.",
            "badge": '<svg width="64px" height="64px" viewBox="-153.6 -153.6 819.20 819.20" id="Layer_1" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"><rect x="-153.6" y="-153.6" width="819.20" height="819.20" rx="81.92" fill="#ffffff" strokewidth="0"></rect></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#0A557F;} .st1{fill:#4CC3F2;} .st2{fill:#CFF1FF;} </style> <g> <rect class="st0" height="67.3" width="15" x="410.5" y="152.7"></rect> <rect class="st0" height="15" width="15" x="410.5" y="235.1"></rect> <rect class="st0" height="67.3" width="15" x="86.5" y="371.8"></rect> <rect class="st0" height="15" width="15" x="86.5" y="454.1"></rect> <path class="st1" d="M411.4,299.3l-105.7-13.1L256,186.5l-49.7,99.8l-105.7,13.1l79.2,87.8l-19,94l95.2-44.3l95.2,44.3l-19-94 L411.4,299.3z M256,401.2l-50.7,23.6l9.5-47.2l-48.5-53.7l61.2-7.6l28.5-57.1l28.5,57.1l61.2,7.6l-48.5,53.7l9.5,47.2L256,401.2z"></path> <path class="st0" d="M376.1,312.5l-81.8-10.1L256,225.5l-38.3,76.9l-81.8,10.1l62.7,69.5l-13.9,68.9l71.3-33.2l71.3,33.2L313.4,382 L376.1,312.5z M256,401.2l-50.7,23.6l9.5-47.2l-48.5-53.7l61.2-7.6l28.5-57.1l28.5,57.1l61.2,7.6l-48.5,53.7l9.5,47.2L256,401.2z"></path> <polygon class="st2" points="185.7,94.9 185.7,34.7 170.7,34.7 170.7,94.9 105.7,94.9 105.7,19.7 250.7,19.7 250.7,79.8 265.7,79.8 265.7,19.7 410.6,19.7 410.6,94.9 345.6,94.9 345.6,34.7 330.6,34.7 330.6,94.9 "></polygon> <path class="st0" d="M441.8,288l-126.3-15.6l-51.1-102.7l29.8-59.8h131.5V4.7H90.7v105.2h127.2l29.8,59.8l-51.1,102.7L70.2,288 l93.5,103.6l-23.4,115.7L256,453.4l115.7,53.8l-23.4-115.7L441.8,288z M185.7,94.9V34.7h-15v60.2h-65V19.7h145v60.1h15V19.7h145 v75.2h-65V34.7h-15v60.2H185.7z M234.6,109.9h42.8L256,152.8L234.6,109.9z M351.2,481.2L256,436.9l-95.2,44.3l19-94l-79.2-87.8 l105.7-13.1l49.7-99.8l49.7,99.8l105.7,13.1l-79.2,87.8L351.2,481.2z"></path> </g> </g></svg>',
            "condition": lambda user: user.profile.showcased_pets.count() >= 1,
            #okie
        }
    ],

    'Adventure Achievements': [
        {
            'name': "First Journey",
            "description": "Complete your first adventure.",
            "badge": '',
            "condition": lambda user: AdventureUser.objects.filter(user_id=user, adventure_id__is_finished=True).exists(),
            #okie
        }, {
            'name': "Long-Haul Adventurer",
            'description': "Complete an adventure that lasts over 24 hours.",
            'badge': '',
            "condition": lambda user: Adventure.objects.filter(adventureuser__user_id=user, date_finish__isnull=False, date_finish__gte=timezone.now() - timezone.timedelta(hours=24)).exists(),
        }, {
            'name': "True Adventurer",
            'description': "Send a pet on an adventure for a week.",
            'badge': '',
            "condition": lambda user: AdventurePet.objects.filter(adventure_id__adventureuser__user_id=user, adventure_id__date_finish__isnull=False, adventure_id__date_finish__gte=timezone.now() - timezone.timedelta(days=7)).exists(),
        }
    ],

    'Rarity-based Achievements': [
        {
            'name': "Common Companion",
            'description': "Own 10 Common pets.",
            'badge': '',
            "condition": lambda user: Inventory.objects.filter(owner_id=user, pet_id__rarity=0).count() >= 10,
            #okie
        }, {
            'name': "Rare Treasurer",
            'description': "Own 5 Rare pets.",
            'badge': '',
            "condition": lambda user: Inventory.objects.filter(owner_id=user, pet_id__rarity=2).count() >= 5,
            #okie
        }, {
            'name': "Mythical Collector",
            'description': "Own 3 Mythical pets.",
            'badge': '',
            "condition": lambda user: Inventory.objects.filter(owner_id=user, pet_id__rarity=3).count() >= 3,
            #okie
        }, {
            'name': "Legendary Hoarder",
            'description': "Own 2 Legendary pets.",
            'badge': '',
            "condition": lambda user: Inventory.objects.filter(owner_id=user, pet_id__rarity=4).count() >= 2,
            #okie
        },
    ],

    'Daily Log-in Achievements': [
        {
            'name': "Dedicated Player",
            'description': "Claim rewards every day for 3 days.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }, {
            'name': "Streak Achiever",
            'description': "Claim rewards for a week.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }, {
            'name': "Persistence Pays",
            'description': "Claim rewards for 15 consecutive days.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }, {
            'name': "Hardcore Collector",
            'description': "Claim rewards for a month.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }, {
            'name': "Ultimate Streak",
            'description': "Claim rewards for 2 months.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }, {
            'name': "Adventurer’s Commitment",
            'description': "Log in daily for a month while sending a pet on adventures.",
            'badge': '',
            "condition": lambda user: UserReward.objects.filter(user=user, claimed=True, claim_date__gte=timezone.now() - timedelta(days=3)).count() == 3,
        }
    ]


}