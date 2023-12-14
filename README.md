# notabug-parser
Парсер пользователей NotABug, написаный с помощью Scrapy<br>
Данные сохраняются в json файл
```json
{
    "avatar": "<avatar>", 
    "username": "<name>", 
    "link": null, 
    "location": null, 
    "organizations": [], 
    "repositories": [], 
    "joined": "Joined on Mar 02, 2015", 
    "followers": 3, 
    "following": 0
}
``````

## Запуск
- Устанавливаем зависимости:
    
    pip install -r requirements.txt

- Заходим в корневой раздел проекта:

    cd notabug

- Запускаем паука (парсер):

    scrapy crawl notabug -o accounts.json
