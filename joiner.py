#dont skid lol
import random, httpx, json
from colorama import Fore,Style
with open('config.json') as fp:
    config = json.load(fp)
capapi = config["whichapitosolvewith"]
class TokenJoiner:
    def __init__(self, capKey, invitecode, token):
        self.capKey = capKey
        self.invitecode = invitecode
        with open("Proxies.txt") as fp:
            proxies = fp.read().splitlines()
        self.client = httpx.Client(cookies={"locale": "en-US"}, headers={"Pragma": "no-cache", "Accept": "*/*", "Host": "ptb.discord.com", "Accept-Language": "en-US", "Cache-Control": "no-cache", "Accept-Encoding": "br, gzip, deflate", "Referer": "https://ptb.discord.com/", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "X-Track": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi11cyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzEzXzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMy4xLjIgU2FmYXJpLzYwNS4xLjE1IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMuMS4yIiwib3NfdmVyc2lvbiI6IjEwLjEzLjYiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTEzNTQ5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="}, proxies=f"http://{random.choice(proxies)}")
        superproperties = self.client.headers["X-Track"]
        self.client.headers["X-Fingerprint"] = self.client.get("https://discord.com/api/v10/experiments", timeout=30).json()["fingerprint"]
        del self.client.headers["X-Track"]
        self.client.headers["X-Super-Properties"] = superproperties
        self.client.headers["Authorization"] = token
        self.client.headers["Origin"] = "https://ptb.discord.com"
    def joinServer(self):
        joinreq = self.client.post(f"https://ptb.discord.com/api/v10/invites/{self.invitecode}", json={})
        if "captcha_key" not in joinreq.json():
            if "message" in joinreq.json() and joinreq["message"] == "The user is banned from this guild.":
                print(f"{self.client.headers['Authorization']} Is Banned From discord.gg/{self.invitecode}")
                return "NotJoined", joinreq.json()
            print(
                f"{Fore.GREEN}{self.client.headers['Authorization']} Successfully Joined discord.gg/{self.invitecode} {Style.RESET_ALL}")
            return "Joined", joinreq.json()
        joinreq=self.client.post(f"https://ptb.discord.com/api/v10/invites/{self.invitecode}", json={"captcha_key": self.getCap()})
        if joinreq.status_code == 200:
            print(
                f"{Fore.GREEN}{self.client.headers['Authorization']} Successfully Joined discord.gg/{self.invitecode} {Style.RESET_ALL}")
            return "Joined", joinreq.json()
        else:
            print(
                f"{Fore.RED}{self.client.headers['Authorization']} Failed To Join discord.gg/{self.invitecode} {Style.RESET_ALL}")
            return "NotJoined", joinreq.json()
    def getCap(self):
        solvedCaptcha = None
        captchaKey = self.capKey
        taskId = ""
        taskId = httpx.post(f"https://api.{capapi}/createTask", json={"clientKey": captchaKey, "task": {"type": "HCaptchaTaskProxyless", "websiteURL": "https://ptb.discord.com/","websiteKey": "4c672d35-0701-42b2-88c3-78380b0db560", "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}}, timeout=30).json()
        if taskId.get("errorId") > 0:
                print(f"{Fore.RED}{Style.BRIGHT}[-] createTask - {taskId.get('errorDescription')}!{Style.RESET_ALL}")
                return None
        taskId = taskId.get("taskId")
        while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.{capapi}/getTaskResult", json={"clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
                    if captchaData.get("status") == "ready":
                        solvedCaptcha = captchaData.get("solution").get("gRecaptchaResponse")
                        print(f"{Fore.GREEN}{Style.BRIGHT}[>] Got Captcha {solvedCaptcha[0:60]}{Style.RESET_ALL}")
                        return solvedCaptcha
