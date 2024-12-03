from constants import AVAILABLE_STATUSES, MENU_OPTIONS
from models import Library


def display_menu() -> None:
    """Отображает список команд библиотеки."""
    print("\nСписок команд библиотеки:")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    print("\n")


def remove_book(library: Library) -> None:
    """Обрабатывает удаление книги по ID."""
    book_id = check_if_int("Введите ID книги для удаления: ")
    library.remove_book(book_id)


def add_book(library: Library) -> None:
    """Обрабатывает добавление новой книги."""
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = check_if_int("Введите год издания: ")
    library.add_book(title, author, year)


def find_books(library: Library) -> None:
    """Обрабатывает поиск книг по ключевому слову."""
    while True:
        search_by = input("Искать по (название/автор/год): ").strip().lower()
        if search_by in ("название", "автор", "год"):
            break
        else:
            print("Ошибка: Пожалуйста, введите 'название', 'автор' или 'год'.")

    if search_by == "год":
        keyword = check_if_int("Введите год для поиска: ")
    elif search_by in ("название", "автор"):
        keyword = input("Введите ключевое слово для поиска: ")

    books = library.find_books(keyword, search_by)
    if books:
        for book in books:
            print(f"ID: {book.id}, Название: {book.title}, "
                  f"Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
    else:
        print("Книги не найдены.")


def display_books(library: Library) -> None:
    """Обрабатывает отображение всех книг."""
    library.display_books()


def update_status(library: Library) -> None:
    """Обрабатывает изменение статуса книги."""
    book_id = check_if_int("Введите ID книги для изменения статуса: ")

    while True:
        new_status = input(f"Введите новый статус {AVAILABLE_STATUSES}: ").strip()
        if new_status in AVAILABLE_STATUSES:
            break
        print(f"Статус '{new_status}' отсутствует. Список доступных статусов: {AVAILABLE_STATUSES}")
    library.update_status(book_id, new_status)


def check_if_int(prompt: str) -> int:
    """Запрашивает у пользователя ввод числа, пока не получит корректное значение."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: Пожалуйста, введите корректное целое число.")
