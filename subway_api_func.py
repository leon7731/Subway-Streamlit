import requests

def Login(Email, Password, URL):
    """_summary_: Get JWT token from Subway API

    Args:
        Email (_type_): Email address of user
        Password (_type_): Password of user
        URL (_type_): URL of Subway API

    Returns:
        _type_: JWT token
    """
    
    params = {"username": Email,
              "password": Password}
    
    login_request = requests.post(URL, data=params)
    
    login_request_json = login_request.json()
    
    jwt_token = login_request_json['access_token']
    
    return jwt_token


def request_subway_info_total_items(JWT_Token, page = 1, per_page = 20, order = 'desc'):
    """_summary_: Get total items of subway info

    Args:
        JWT_Token (_type_): JWT token
        page (int, optional): Page number. Defaults to 1.
        per_page (int, optional): Number of items per page. Defaults to 20.
        order (str, optional): Order of items. Defaults to 'desc'.

    Returns:
        _type_: Total items of subway info
    """
    
    headers = {"Authorization": f"Bearer {JWT_Token}" }
    
    URL = f"http://50.19.149.26/subway/all?page={page}&perPage={per_page}&order=desc"
    
    subway_info_request = requests.get(URL, headers=headers)

    subway_info_json = subway_info_request.json()
    
    subway_info_total_items = subway_info_json['total_items']
    
    return subway_info_total_items


def request_subway_info_data(JWT_Token, page = 1, per_page = 20, order = 'desc'):
    """_summary_: Get subway info data

    Args:
        JWT_Token (_type_): JWT token
        page (int, optional): Page number. Defaults to 1.
        per_page (int, optional): Number of items per page. Defaults to 20.
        order (str, optional): Order of items. Defaults to 'desc'.

    Returns:
        _type_: Subway info data
    """
    
    headers = {"Authorization": f"Bearer {JWT_Token}" }
    
    URL = f"http://50.19.149.26/subway/all?page={page}&perPage={per_page}&order=desc"
    
    subway_info_request = requests.get(URL, headers=headers)

    subway_info_json = subway_info_request.json()
    
    return subway_info_json


def extract_subway_info_data(JWT_Token):
    """_summary_: Extract all subway info data

    Args:
        JWT_Token (_type_): JWT token

    Returns:
        _type_: List of subway info data
    """
    # Request total items
    subway_info_total_items = request_subway_info_total_items(JWT_Token=JWT_Token, 
                                                              page=1, 
                                                              per_page=20, 
                                                              order='desc')

    # print(f"Total Items: {subway_info_total_items}")

    # Initialize a list to store all subway data
    all_subway_data = []

    # Calculate total pages needed
    total_pages = subway_info_total_items // 20 + 1

    for page in range(1, total_pages + 1):  # Ensure last page is included
        # Request subway info data for each page
        subway_info_data = request_subway_info_data(JWT_Token=JWT_Token, 
                                                    page=page, 
                                                    per_page=20, 
                                                    order='desc')

        # Process and store data from each page
        for item in subway_info_data.get('data', []):
            subway_info = {
                'name': item.get('name'), 
                'address': item.get('address'), 
                'operating_hours': item.get('operating_hours'), 
                'waze_link': item.get('waze_link'),
                'google_maps_link': item.get('google_maps_link'),
                'latitude': item.get('google_geocoded_latitude'),
                'longitude': item.get('google_geocoded_longitude')
            }
            all_subway_data.append(subway_info)

        # print(f"Page: {page}\n")

    return all_subway_data