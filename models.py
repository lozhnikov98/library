import json
import os

from typing import List

from constants import AVAILABLE_STATUSES


class Book:
    """Модель книги."""

    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """Преобразует объект книги в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создает объект книги из словаря."""
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    """Модель библиотеки."""

    def __init__(self, data_file: str = None):
        self.data_file = data_file or os.path.join(os.path.dirname(__file__), "", "library.json")
        self.books: List[Book] = []
        self._initialize_library()

    def _initialize_library(self) -> None:
        """Инициализирует библиотеку, проверяя наличие файла и загружая книги."""
        if not os.path.exists(self.data_file):
            self._create_empty_library_file()
        self.load_books()

    def _create_empty_library_file(self) -> None:
        """Создает пустой JSON файл библиотеки."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    def load_books(self) -> None:
        """Загружает книги из JSON файла."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    books_data = json.load(file)
                    self.books = [Book.from_dict(book) for book in books_data]
            except json.JSONDecodeError:
                print("Ошибка: Файл данных поврежден или содержит недопустимый JSON.")
                self.books = []
            except Exception as e:
                print(f"Произошла ошибка при загрузке данных: {e}")
                self.books = []

    def save_books(self) -> None:
        """Сохраняет книги в JSON файл."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки по ID."""
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, keyword: str, search_by: str) -> List[Book]:
        """Ищет книги по заданному критерию."""
        if search_by == "название":
            return [book for book in self.books if keyword.lower() in book.title.lower()]
        elif search_by == "автор":
            return [book for book in self.books if keyword.lower() in book.author.lower()]
        elif search_by == "год":
            return [book for book in self.books if book.year == keyword]
        else:
            return []

    def display_books(self) -> None:
        """Отображает все книги в библиотеке."""
        if self.books:
            for book in self.books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
                      f"Год: {book.year}, Статус: {book.status}")
        else:
            print("Библиотека пуста.")

    def update_status(self, book_id: int, new_status: str) -> None:
        """Изменяет статус книги по ID."""
        book_to_update = next((book for book in self.books if book.id == book_id), None)
        if book_to_update:
            if new_status in AVAILABLE_STATUSES:
                book_to_update.status = new_status
                self.save_books()
            else:
                print(f"Неправильный статус. Доступные статусы: {AVAILABLE_STATUSES}.")
        else:
            print(f"Книга с ID {book_id} не найдена.")
