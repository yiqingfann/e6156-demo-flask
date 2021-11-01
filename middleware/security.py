import json
import re

path_not_secure = {
    "^/$": {"GET"},
    # /users
    # /users/
    "^/users/?$": {"GET"},
    # /users/<user_id>
    # /users/<user_id>/
    "^/users/[0-9]+/?$": {"GET"}
}

path_not_restrict = {

}

admin_accounts = {

}

def check_security(request, google, blueprint):
    path = request.path

    for reg in path_not_secure:
        if re.match(reg, path):
            return True
    if not google.authorized:
        return False
    user_info_endpoint = "/oauth2/v2/userinfo"
    google_data = google.get(user_info_endpoint).json()
    print(json.dumps(google_data, indent=2))
    session = blueprint.session
    token = session.token
    print("Token = ", json.dumps(token, indent=2))
    return True
