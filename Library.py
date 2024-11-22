import json
import os


class Book:
    """
    Класс для представления книги с ее характеристиками.

    id (int): уникальный идентификатор, генерируется автоматически;
    title (str): название книги
    author (str): автор книги
    year (int): год издания
    status (str): статус книги: “в наличии”, “выдана”
    """

    def __init__(self, title: str, author: str, year: int, status: str = "В наличии"):
        """
        Инициализация объекта книги.

        :param title(str): название книги
        :param author(str): автор книги
        :param year(int): год издания
        :param status(str): статус книги: “в наличии”, “выдана”
        """
        self.id = Book.get_next_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    @staticmethod
    def get_next_id() -> int:
        """
        Генерирует уникальный id.

        :return: (int) следующий уникальный id
        """
        if not os.path.exists('books.json'):
            return 1
        with open('books.json', 'r', encoding='utf-8') as file:
            books = json.load(file)
            if books:
                return max(book['id'] for book in books) + 1
        return 1

def load_books() -> list:
    """
     Загружает данные книг из файла books.json
    """
    if not os.path.exists('books.json'):
        return []
    with open('books.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def save_books(books: list) -> None:
    """
    Сохраняет данные книг в books.json
    :param books: список книг
    """
    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def add_book(title: str, author: str, year: int) -> None:
    """
    Добавляет новую книгу.

    :param title(str): название книги
    :param author(str): автор книги
    :param year(int): год издания
    """

    books = load_books()
    new_book = Book(title, author, year)
    books.append(new_book.__dict__)
    save_books(books)
    print(f'\nВы добавили книгу "{title}" в библиотеку')


def delete_book(book_id: int) -> None:
    """
    Удаляет книгу по id.
    :param book_id: id книги, которую нужно удалить
    """
    books = load_books()
    update_books = [book for book in books if book['id'] != book_id]
    if len(update_books) == len(books):
        print(f'Книга с ID {book_id} не найдена.')
    else:
        save_books(update_books)
        print(f'Книга с ID {book_id} удалена успешно.')



def search_book(query: str) -> list:
    """
    Ищет книги по названию, году издания или автору.
    :param query: данные для поиска (название, год, автор)
    """
    books = load_books()
    results = [book for book in books if query.lower() in book['title'].lower() or
               query.lower() in book['author'].lower() or
               query == str(book['year'])]

    if results:
        for book in results:
            print(f' \tID книги: {book["id"]}\n \tНазвание книги: {book["title"]}\n'
                  f' \tАвтор: {book["author"]}\n \tГод издания: {book["year"]}\n '
                  f' \tСтатус: {book["status"]}\n')
    else:
        print('Книги не найдены.')


def display_books() -> None:
    """
    Отображает список книг.
    """

    books = load_books()
    if books:
        print("Список книг в библиотеке: ")
        for book in books:
            print(f' \tID книги: {book["id"]}\n \tНазвание книги: {book["title"]}\n'
                  f' \tАвтор: {book["author"]}\n \tГод издания: {book["year"]}\n '
                  f' \tСтатус: {book["status"]}\n')
    else:
        print("В библиотеке пока нет книг")


def update_status(book_id: int, new_status: str) -> None:
    """
    Изменяет статус книги по id
    :param book_id(int): id книги
    :param new_status(str): новый статус для книги ("в наличии", "выдана")
    """
    books = load_books()
    for book in books:
        if book['id'] == book_id:
            if new_status in ["в наличии", "выдана"]:
                book['status'] = new_status
                save_books(books)
                print(f'Статус книги с ID {book_id} обновлен на "{new_status}".')
                return
            else:
                print('Ошибка: статус должен быть "в наличии" или "выдана".')
                return
    print(f'Книга с ID {book_id} не найдена.')


def main():
    """
    Главная функция для запуска консольного приложения по управлению библиотекой
    """
    print('\nВас приветствует система управления библиотекой.')
    while True:
        print('\nДоступные действия: ')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книгу')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('6. Выход')
        choice = input('\nВведите номер действия: ')
        '\n'

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            add_book(title=title, author=author, year=year)

        elif choice == '2':
            try:
                book_id = int(input("Введите id книги, которую хотите удалить: "))
                delete_book(book_id)
            except ValueError:
                print("Ошибка: введите корректный ID.")

        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            search_book(query)

        elif choice == '4':
            display_books()

        elif choice == '5':
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                update_status(book_id, new_status)
            except ValueError:
                print("Ошибка: введите корректный числовой ID.")

        elif choice == '6':
            print("Работа с библиотекой звершена. \nХорошего Вам дня.")
            break

        else:
            print('*Такого действия пока нет, попробуйте другое*')


if __name__ == '__main__':
    main()
