import requests
import os

"""
voice input -> до скольки работает библиотека -> 



"""

class A2FHandlers:
    
    def __init__(self, host_url: str):
        self._host_url = host_url.rstrip('/')  # Удаляем слэш в конце, если есть

    def get_instances(self):  # Добавлено self
        response = requests.get(self._host_url + '/A2F/Player/GetInstances')
        
        if response.status_code == 200:
            return response.json()  # Возвращаем JSON-ответ
        else:
            print(f"Запрос не удался. Код ошибки: {response.status_code}")
            return None  # Или можно вернуть ошибку

    def set_root_path(self, dir_path: str = None, a2f_player: str = None):
        if dir_path is None:
            dir_path = os.path.join(os.getcwd(), 'audiofiles')

        full_url = self._host_url + '/A2F/Player/SetRootPath'  # Полный URL
        payload = {
            'dir_path': dir_path,  # Параметры для POST-запроса
            'a2f_player': a2f_player
        }
        headers = {'accept': 'application/json'}  # Заголовки запроса

        response = requests.post(full_url, json=payload, headers=headers)  # Отправка POST-запроса

        if response.status_code == 200:
            return response.json()  # Возвращаем JSON-ответ
        else:
            print(f"Запрос не удался. Код ошибки: {response.status_code}, Сообщение: {response.text}")
            return None  # Обработка ошибки

    def set_track(self, a2f_player: str, file_name: str):
        """Отправляет трек на указанный A2F плеер"""
        full_url = self._host_url + '/A2F/Player/SetTrack'  # Полный URL
        payload = {
            'a2f_player': a2f_player,
            'file_name': file_name
        }
        headers = {'accept': 'application/json'}  # Заголовки запроса

        try:
            response = requests.post(full_url, json=payload, headers=headers)  # Отправка POST-запроса

            if response.status_code == 200:
                return response.json()  # Возвращаем JSON-ответ
            else:
                print(f"Запрос не удался. Код ошибки: {response.status_code}, Сообщение: {response.text}")
                return None  # Обработка ошибки
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None  # Обработка исключений

    def play(self, a2f_player: str):
        full_url = self._host_url + '/A2F/Player/Play'  # Полный URL
        payload = {
            'a2f_player': a2f_player,
        }
        headers = {'accept': 'application/json'}  # Заголовки запроса

        try:
            response = requests.post(full_url, json=payload, headers=headers)  # Отправка POST-запроса

            if response.status_code == 200:
                return response.json()  # Возвращаем JSON-ответ
            else:
                print(f"Запрос не удался. Код ошибки: {response.status_code}, Сообщение: {response.text}")
                return None  # Обработка ошибки
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None  # Обработка исключений

    def remove_keys(self, a2f_instance: str):
        # Получаем ключи
        get_keys_url = self._host_url + '/A2F/A2E/GetKeys'  # Полный URL для получения ключей
        payload = {
            'a2f_instance': a2f_instance,
            'as_timestamps': False  # Константа
        }
        headers = {'accept': 'application/json'}  # Заголовки запроса

        try:
            # Запрос на получение ключей
            response = requests.post(get_keys_url, json=payload, headers=headers)

            if response.status_code != 200:
                print(f"Запрос на получение ключей не удался. Код ошибки: {response.status_code}, Сообщение: {response.text}")
                return None

            keys_response = response.json()
            if keys_response.get("status") != "OK":
                print("Не удалось получить ключи.")
                return None

            # Извлекаем ключи из ответа
            keys = keys_response.get("result", [])

            # Удаляем ключи
            remove_keys_url = self._host_url + '/A2F/A2E/RemoveKeys'  # Полный URL для удаления ключей
            payload = {
                'a2f_instance': a2f_instance,
                'keys': keys,  # Используем полученные ключи
                'as_timestamps': False  # Константа
            }

            response = requests.post(remove_keys_url, json=payload, headers=headers)  # Отправка POST-запроса для удаления ключей

            if response.status_code == 200:
                return response.json()  # Возвращаем JSON-ответ
            else:
                print(f"Запрос на удаление ключей не удался. Код ошибки: {response.status_code}, Сообщение: {response.text}")
                return None  # Обработка ошибки
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None  # Обработка исключений

if __name__ == '__main__':
    a2f_player_path = "/World/audio2face/Player"
    a2fHandler = A2FHandlers(host_url="http://localhost:8011/")
    a2fHandler.set_root_path(a2f_player=a2f_player_path)
    
    result = a2fHandler.play(a2f_player=a2f_player_path)
