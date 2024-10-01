import requests

class A2FHandlers:
    
    def __init__(self, host_url: str):  # Добавлено self
        self._host_url = host_url.rstrip('/')  # Удаляем слэш в конце, если есть


    def get_instances(self):  # Добавлено self
        response = requests.get(self._host_url + '/A2F/Player/GetInstances')
        
        # Проверка статуса ответа
        if response.status_code == 200:
            return response.json()  # Возвращаем JSON-ответ
        else:
            print(f"Запрос не удался. Код ошибки: {response.status_code}")
            return None  # Или можно вернуть ошибку

    def set_root_path(self, dir_path: str = None, a2f_player: str = None):
        # Устанавливаем dir_path по умолчанию на путь к audiofiles в текущем каталоге
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



if __name__ == '__main__':
    a2fHandler = A2FHandlers(host_url="http://192.168.8.104:8011")
    result = a2fHandler.play(a2f_player="/World/LazyGraph/Player")
    print(result)