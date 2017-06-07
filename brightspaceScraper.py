payload = {
    "userName": "dy780090",
    "password": "#20l17D80a47",
}
















from lxml import html
import requests

sessionRequests = requests.session()

loginUrl = "https://dal.brightspace.com/d2l/login"
result = sessionRequests.get(loginUrl)

result = sessionRequests.post(
    loginUrl,
    data = payload,
    headers = dict(referer=loginUrl)
)

tree = html.fromstring(result.text)


print('aa')
