def create_view_reserver(data):
    return (f"<b>{data['name']}</b>\n"
            f"{data["description"]}\n\n"
            f"<b>Регион</b>: {data["region"]["name"]}\n"
            f"<b>Город</b>: {data["city"]["name"]}\n"
            f"<b>Статус</b>: {data["state"]["name"]}\n"
            f"<b>Кол кластеров</b>: {data["count_cluster"]}\n"
            f"<b>Размер</b>: {data["size"]} га.\n"
            f"<b>Размер охраняемой зоны</b>: {data["guarded_size"]} га.\n"
            f"<b>Телефон</b>: +7{data["phone"]}\n"
            f"<b>Email</b>: {data["mail"]}\n"
            f"<a href='{data['link']}'>Ссылка на сайт</a>")


def create_weather_reserver(data):
        message = "Погода на ближайшую неделю\n\n"
        for i in data["info_to_week"]:
                message += (f"<b>Дата: {i["time"]}</b>\n"
                            f"Облачность: {i["info"]["cloudiness"]}\n"
                            f"Влажность: {i["info"]["humidity"]}%\n"
                            f"Температура: {i["info"]["avgTemperature"]} t\n"
                            f"Тип Осадков: {i["info"]["precType"]}\n"
                            f"Сила Осадков: {i["info"]["precStrength"]}\n"
                            f"Скорость ветра: {i["info"]["windSpeed"]} м/с\n\n")
        return message