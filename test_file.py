import pytest
from main import BooksCollector

# Класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector.
# Обязательно указывать префикс Test, чтобы pytest распознал его как тестовый набор.
class TestBooksCollector:

    # Тест для метода add_new_book: проверяем добавление двух книг.
    # Обязательно указывать префикс test_.
    # Далее идет название метода, который тестируем (add_new_book),
    # затем краткое описание того, что именно тестируем (add_two_books - добавление двух книг).
    def test_add_new_book_add_two_books(self):
        # Создаем экземпляр (объект) класса BooksCollector.
        # Это гарантирует, что каждый тест начинается с "чистого листа" и не зависит от предыдущих тестов.
        collector = BooksCollector()

        # Добавляем две книги с помощью метода add_new_book.
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # Проверяем, что в словаре books_genre теперь содержится именно две книги.
        # Метод get_books_genre() возвращает текущее состояние словаря, а len() - его размер.
        assert len(collector.get_books_genre()) == 2

    # Тест для метода add_new_book: проверяем невозможность добавления книги с недопустимой длиной названия.
    def test_add_new_book_invalid_name_length(self):
        collector = BooksCollector()
        # Создаем строку, которая длиннее максимально допустимых 40 символов.
        long_name = 'a' * 41
        collector.add_new_book(long_name)
        # Ожидаем, что книга с таким названием не будет добавлена, и размер словаря останется 0.
        assert len(collector.get_books_genre()) == 0

    # Тест для метода add_new_book: проверяем, что одну и ту же книгу можно добавить только один раз.
    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        # Добавляем книгу с одинаковым названием дважды.
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 1')
        # Ожидаем, что в словаре будет только одна запись для "Книга 1".
        assert len(collector.get_books_genre()) == 1

    # Тест для метода add_new_book: проверяем, что книга добавляется без жанра.
    def test_add_new_book_no_genre_initially(self):
        collector = BooksCollector()
        book_name = 'Новая книга без жанра'
        collector.add_new_book(book_name)
        # Проверяем, что добавленная книга имеет пустой жанр (не назначенный).
        assert collector.get_book_genre(book_name) == ''

    # Параметризованный тест для метода set_book_genre.
    # pytest.mark.parametrize позволяет запускать один и тот же тест несколько раз с разными данными.
    # Аргументы: 'book_name', 'genre', 'expected_genre' - это названия переменных,
    # которые будут переданы в тест для каждого набора данных.
    @pytest.mark.parametrize("book_name, genre, expected_genre", [
        ('Книга 1', 'Фантастика', 'Фантастика'),    # Успешное присвоение существующего жанра
        ('Книга 2', 'Ужасы', 'Ужасы'),
        ('Книга 3', 'Детективы', 'Детективы'),
        ('Книга 4', 'Мультфильмы', 'Мультфильмы'),
        ('Книга 5', 'Комедии', 'Комедии'),
        ('Книга 6', 'Неизвестный жанр', ''),        # Попытка присвоить несуществующий жанр (должно остаться пустым)
        ('Книга 7', 'Фантастика', 'Фантастика'),    # Еще один успешный случай
    ])
    def test_set_book_genre(self, book_name, genre, expected_genre):
        collector = BooksCollector()
        # Сначала добавляем книгу, чтобы её можно было назначить жанр.
        collector.add_new_book(book_name)
        # Устанавливаем жанр книги.
        collector.set_book_genre(book_name, genre)
        # Проверяем, что жанр книги соответствует ожидаемому.
        # Метод get_book_genre() возвращает жанр по названию книги.
        assert collector.get_book_genre(book_name) == expected_genre

    # Тест для метода get_book_genre: проверяем, что метод возвращает None для книги, которой нет в словаре.
    def test_get_book_genre_nonexistent(self):
        collector = BooksCollector()
        # Пытаемся получить жанр для несуществующей книги.
        # Ожидаем, что метод вернет None.
        assert collector.get_book_genre('Несуществующая книга') is None

    # Параметризованный тест для метода get_books_with_specific_genre.
    # Проверяем, как метод возвращает списки книг для разных жанров.
    @pytest.mark.parametrize("genre, expected_books", [
        ('Фантастика', ['Книга Ф1', 'Книга Ф2']), # Ожидаем две книги жанра "Фантастика"
        ('Ужасы', ['Книга У1']),                  # Ожидаем одну книгу жанра "Ужасы"
        ('Детективы', []),                        # Ожидаем пустой список для "Детективы" (книги нет)
        ('Мультфильмы', ['Книга М1']),            # Ожидаем одну книгу жанра "Мультфильмы"
        ('Комедии', ['Книга К1']),                # Ожидаем одну книгу жанра "Комедии"
        ('Неизвестный жанр', []),                 # Ожидаем пустой список для несуществующего жанра
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        # Заполняем словарь books_genre тестовыми данными.
        collector.add_new_book('Книга Ф1')
        collector.set_book_genre('Книга Ф1', 'Фантастика')
        collector.add_new_book('Книга Ф2')
        collector.set_book_genre('Книга Ф2', 'Фантастика')
        collector.add_new_book('Книга У1')
        collector.set_book_genre('Книга У1', 'Ужасы')
        collector.add_new_book('Книга Д1')
        collector.set_book_genre('Книга Д1', 'Детективы')  # Эта книга не будет найдена в тесте 'Детективы', так как ожидаемый список пуст
        collector.add_new_book('Книга М1')
        collector.set_book_genre('Книга М1', 'Мультфильмы')
        collector.add_new_book('Книга К1')
        collector.set_book_genre('Книга К1', 'Комедии')
        collector.add_new_book('Книга без жанра')           # Книга без жанра

        # Получаем список книг для заданного жанра.
        actual_books = collector.get_books_with_specific_genre(genre)
        # Сравниваем полученный список с ожидаемым.
        assert actual_books == expected_books

    # Тест для метода get_books_genre.
    def test_get_books_genre(self):
        collector = BooksCollector()
        # Добавляем несколько книг.
        collector.add_new_book('Книга А')
        collector.add_new_book('Книга Б')
        collector.set_book_genre('Книга А', 'Фантастика')

        # Получаем словарь всех книг.
        books_dict = collector.get_books_genre()
        # Проверяем, что словарь содержит добавленные книги и их жанры.
        assert len(books_dict) == 2
        assert books_dict.get('Книга А') == 'Фантастика'
        assert books_dict.get('Книга Б') == ''                          # Проверяем, что "Книга Б" имеет пустой жанр

    # Тест для метода get_books_for_children.
    # Проверяем, что книги с возрастным рейтингом не попадают в список детских книг.
    def test_get_books_for_children_without_age_rating(self):
        collector = BooksCollector()
        # Добавляем книги разных жанров.
        collector.add_new_book('Детская книга 1')
        collector.set_book_genre('Детская книга 1', 'Мультфильмы')      # Мультфильмы - без возрастного рейтинга
        collector.add_new_book('Детская книга 2')
        collector.set_book_genre('Детская книга 2', 'Комедии')          # Комедии - без возрастного рейтинга

        collector.add_new_book('Книга для взрослых 1')
        collector.set_book_genre('Книга для взрослых 1', 'Ужасы')       # Ужасы - с возрастным рейтингом
        collector.add_new_book('Книга для взрослых 2')
        collector.set_book_genre('Книга для взрослых 2', 'Детективы')   # Детективы - с возрастным рейтингом

        # Получаем список книг для детей.
        books_for_children = collector.get_books_for_children()
        # Ожидаем, что в списке будут только книги без возрастного рейтинга.
        assert len(books_for_children) == 2
        assert 'Детская книга 1' in books_for_children
        assert 'Детская книга 2' in books_for_children
        assert 'Книга для взрослых 1' not in books_for_children
        assert 'Книга для взрослых 2' not in books_for_children

    # Тест для метода add_book_in_favorites.
    # Проверяем добавление книги в избранное.
    @pytest.mark.parametrize("book_name", ['Книга для избранного 1', 'Книга для избранного 2'])
    def test_add_book_in_favorites_success(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        # Проверяем, что книга добавлена в список избранного.
        assert book_name in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1

    # Тест для метода add_book_in_favorites: проверяем, что книгу, которой нет в books_genre, нельзя добавить в избранное.
    def test_add_book_in_favorites_nonexistent_book(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Книга, которой нет')
        # Ожидаем, что список избранного останется пустым.
        assert len(collector.get_list_of_favorites_books()) == 0

    # Тест для метода add_book_in_favorites: проверяем, что одну и ту же книгу нельзя добавить в избранное повторно.
    def test_add_book_in_favorites_duplicate(self):
        collector = BooksCollector()
        book_name = 'Уникальная книга'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)      # Повторное добавление
        # Ожидаем, что в списке избранного будет только одна копия книги.
        assert len(collector.get_list_of_favorites_books()) == 1

    # Тест для метода delete_book_from_favorites.
    def test_delete_book_from_favorites_success(self):
        collector = BooksCollector()
        book_to_delete = 'Книга для удаления'
        # Добавляем книгу в избранное.
        collector.add_new_book(book_to_delete)
        collector.add_book_in_favorites(book_to_delete)
        # Удаляем книгу из избранного.
        collector.delete_book_from_favorites(book_to_delete)
        # Проверяем, что книга удалена из списка избранного.
        assert book_to_delete not in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 0

    # Тест для метода delete_book_from_favorites: проверяем, что попытка удалить несуществующую книгу не вызывает ошибок.
    def test_delete_book_from_favorites_nonexistent_book(self):
        collector = BooksCollector()
        # Пытаемся удалить книгу, которой нет ни в books_genre, ни в favorites.
        collector.delete_book_from_favorites('Книга, которой нет в избранном')
        # Список избранного должен остаться пустым.
        assert len(collector.get_list_of_favorites_books()) == 0

    # Тест для метода get_list_of_favorites_books.
    def test_get_list_of_favorites_books_empty_initially(self):
        collector = BooksCollector()
        # Ожидаем, что при создании объекта список избранного пуст.
        assert collector.get_list_of_favorites_books() == []

    # Дополнительный тест: Проверяем, что книга, удаленная из избранного, может быть добавлена снова.
    def test_add_and_delete_and_add_again_to_favorites(self):
        collector = BooksCollector()
        book_name = 'Перезагрузка избранного'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        assert len(collector.get_list_of_favorites_books()) == 1
        assert book_name in collector.get_list_of_favorites_books()

