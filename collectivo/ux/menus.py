"""
Management of menus.

Objects:
    Menu (class): A menu.
    MenuItem (class): A menu item.
    menus (dict): A dictionary of all registered menus.
    main_menu (Menu): The main menu for collectivo users.
"""

from dataclasses import dataclass


@dataclass
class MenuItem:
    """An item of a menu.

    Menu items can contain further items as sub_items.

    Arguments:
        display (str): HTML Snippet to be displayed within the menu tile.
        path (str): Link to be used when the item is clicked.
        use_static (bool): Interpret path as relative path in static files.
        action (str):
            Action to be performed when item is clicked.
            Options:
                'microfrontend': Load microfrontend from given path.
                'iframe': Load given path as an iframe.
        target (str):
            Location in which the action should be performed.
            Options:
                'default': Default location of the user interface.
    """

    display: str
    path: str
    use_static: bool = True
    action: str = 'microfrontend'
    target: str = 'default'
    # subitems: list['MenuItem'] = None


# Global object to store menus
# name(str): menu(Menu)
menus = {}


class Menu:
    """
    A menu consisting of multiple items.

    Arguments:
        name (str): Name of the menu.
    """

    def __init__(self, name: str):
        """Initialize menu."""
        if name in menus:
            AttributeError(f"Menu with name '{name}' defined twice.")
        self.name = name
        self.items = []
        menus[name] = self

    def add_item(self, menu_item):
        """Add a new item to the menu."""
        self.items.append(menu_item)
        # TODO Sorting system self.items.sort()

    def __repr__(self) -> str:
        """Return string representation of this class."""
        return f'Menu ({self.name}, {len(self.items)} items)'


# Initialize main menu
main_menu = Menu('main_menu')
main_menu.add_item(MenuItem(
    display='Test item',
    path='test/path'
))
