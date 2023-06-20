def register_api(app_register, view, url):
    """
    Register a route in the API
    :param app_register: The app where te route is going to be registered
    :param view: The controller to register
    :param url: The url for the controller
    :return: None
    """
    item = view.as_view(f"{url}")
    app_register.add_url_rule(f"/api/{url}", view_func=item)
