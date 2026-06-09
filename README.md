# Cabinet Site

Django‑проект для сайта производства шкафов автоматики.

## Что внутри
- публичные страницы: главная, референс‑лист, контакты
- личный кабинет клиентов с доступом к проектам и файлам
- админка для управления проектами, пользователями и доступами
- SEO: `robots.txt`, `sitemap.xml`, мета‑теги, заготовка под `yandex-verification`
- минималистичный UI с анимациями появления

## Как запустить
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Переменные окружения
Смотри `.env.example`.

## Как устроен доступ
В админке:
1. создаёшь пользователя клиента;
2. прикрепляешь его к проекту через `ProjectAccess`;
3. загружаешь схемы и исходники как `ProjectFile`.

Пользователь после входа видит только те проекты и файлы, на которые ему выдан доступ.

- `YANDEX_MAP_EMBED_URL` — ссылка на iframe-виджет Яндекс.Карт для страницы контактов.
