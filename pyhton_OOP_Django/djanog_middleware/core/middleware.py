from datetime import datetime
from pathlib import Path
from user_agents import parse

class RequestLogMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        method = request.method
        path = request.path
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent_str = request.headers.get('User-agent', '')

        user_agent = parse(user_agent_str)
        browser = (
            f"{user_agent.browser.family} "
            f"{user_agent.browser.version_string}"
        )

        operating_system = (
            f"{user_agent.os.family} "
            f"{user_agent.os.version_string}"
        )

        if user_agent.is_mobile:
            device_type = "Mobile"

        elif user_agent.is_tablet:
            device_type = "Tablet"

        elif user_agent.is_pc:
            device_type = "Desktop"

        elif user_agent.is_bot:
            device_type = "Bot"

        else:
            device_type = "Unknown"

        response = self.get_response(request)
        status = response.status_code

        log_message = (
            f"Time: {request_time}\n"
            f"Method: {method}\n"
            f"Path: {path}\n"
            f"IP: {ip_address}\n"
            f"User Agent:\n"
            f"            Browser: {browser}\n"
            f"            OS: {operating_system}\n"
            f"Device: {device_type} \n"
            f"Status: {status} |\n\n"
        )

        log_path = Path(__file__).resolve().parent / "request_logs.txt"

        with open(log_path, 'a') as log_file:
            log_file.write(log_message)

        
        return response
