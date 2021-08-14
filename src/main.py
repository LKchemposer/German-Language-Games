from mvc_menu import Menu, MenuView, MenuController


def main():
    menu = MenuController(MenuView(), Menu())
    menu.run()
    menu.end()


if __name__ == '__main__':
    main()
