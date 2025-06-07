# import requests

# url = 'https://graph.facebook.com/v18.0/328726203668222/messages'

# headers = {
#     'Authorization': 'Bearer EAAyUBzhth2oBO5uZC8l8v5108GflLq3kf9hLPCcgCXAjfAqJDfEDRP5bQj6V6hi7xj7AfOQVLppYEAPKpvyzH8ZCcoKxrqcHX7Iyh2f0Roxobl3jwQMTCRMXwyCajLUX5D103b1Q94Le9h3hKqmsDt9KtoKkZAgEjiEEGV8PjGb4lOqpGYQeruDjlHuGCxbSD7BxeZBPjTIINoPkGCEZD',
#     'Content-Type': 'application/json',
# }

# data = {
#   'messaging_product': 'whatsapp',
#   'recipient_type': 'individual',
#   'to': '917018651659',
#   'type': 'document',
#   'document': {
#     'link': '/home/aman/Downloads/22000207_PerformanceReport.pdf',
#     "caption": "Here is your reciept"
#   }
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)


import requests
import json

url = 'https://graph.facebook.com/v18.0/328726203668222/messages'
headers = {
    'Authorization': 'Bearer EAAyUBzhth2oBO5uZC8l8v5108GflLq3kf9hLPCcgCXAjfAqJDfEDRP5bQj6V6hi7xj7AfOQVLppYEAPKpvyzH8ZCcoKxrqcHX7Iyh2f0Roxobl3jwQMTCRMXwyCajLUX5D103b1Q94Le9h3hKqmsDt9KtoKkZAgEjiEEGV8PjGb4lOqpGYQeruDjlHuGCxbSD7BxeZBPjTIINoPkGCEZD',
    'Content-Type': 'application/json'
}
payload = {
    'messaging_product': 'whatsapp',
    'recipient_type': 'individual',
    'to': '917018651659',
    'type': 'text',
    'text': {
        'preview_url': False,
        'body': 'Hello'
    }
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)