from functions import (
    add_book,
    display_books,
    display_menu,
    find_books,
    remove_book,
    update_status,
)

from models import Library


def main() -> None:
    # Инициализация библиотеки.
    library = Library()

    # Главный цикл
    while True:
        display_menu()

        choice = input("Выберите номер действия : ")

        # Обработка выбора действия пользователя

        if choice == "1":
            add_book(library)

        elif choice == "2":
            remove_book(library)

        elif choice == "3":
            find_books(library)

        elif choice == "4":
            display_books(library)

        elif choice == "5":
            update_status(library)
            
        elif choice == "6":
            break
        else:
            print("Неправильный выбор. Попробуйте снова.")

        if input("\nПродолжить работу (*/нет): ") == "нет":
            break


if __name__ == "__main__":
    main()
