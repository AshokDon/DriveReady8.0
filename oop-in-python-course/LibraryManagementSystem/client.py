from member import Member
from novel_book import NovelBook


def main():
    goku = Member("Asha", "asha@email.com")

    novel = NovelBook(
        "N-1",
        "Dune",
        "Frank Herbert",
        "Sci-Fi"
    )

    novel.display_book_details()

    print("Available?", novel.is_available())
    print("Lend:", novel.lend(goku))
    print("Available?", novel.is_available())
    print("Lend again:", novel.lend(goku))


if __name__ == "__main__":
    main()
