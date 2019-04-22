from app.core.services import page_data_service


def get_page_data():
    (data, err) = page_data_service.get_page_data_service()
    if err is not None:
        return None, err
    return data, None
