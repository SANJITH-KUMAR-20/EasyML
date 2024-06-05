# import requests

# dataset = None
# def upload_csv() -> None:

#     """
#     Unit test for upload route

#     Args : None
#     Returns : None
#     """
#     url = 'http://127.0.0.1:8000/upload_csv'
#     files = {'file': open('path/to/your/file.csv', 'rb')}
#     data = {'name': 'dummy', 'type': 'csv'}
#     response = requests.post(url, files=files, data=data)
#     if response.status_code == 200:
#         print("Sucess")
#     else:
#         print("Upload failed with status code:", response.status_code)


# def drop_colum() -> None:

#     """
#     Unit test for drop column
#     Args : None
#     Returns: None

#     """
#     url = 'http://127.0.0.1:8000/drop_columns'

#     payload = {
#         "dataset_name": "dummy",
#         "task": "Drop",
#         "columns": ["Pclass"]
#     }

#     response = requests.post(url, json=payload)
#     print(dataset[payload["dataset_name"]].get_state().head())

#     if response.status_code == 200:
#         print("Sucess")
#     else:
#         print("Upload failed with status code:", response.status_code)
        