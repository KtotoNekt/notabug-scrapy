# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
# from dataclasses import dataclass, field


class AccountItem(Item):
    username = Field()
    avatar = Field()
    link = Field()
    location = Field()
    organizations = Field(serializer=list)
    repositories = Field(serializer=list)
    followers = Field()
    following = Field()
    joined = Field()


class OrganizationItem(Item):
    icon = Field()
    link = Field()


class RepositoryItem(Item):
    title = Field()
    description = Field()
    last_updated = Field()
    url = Field()
    stars = Field()
    branches = Field()





# @dataclass
# class AccountItem:
#     username: str = field(default=None)
#     avatar: str = field(default=None)
#     link: str = field(default=None)
#     location: str = field(default=None)
#     organizations: list[OrganizationItem] = field(default_factory=[])
#     repositories: list[RepositoryItem] = field(default_factory=[])
#     followers: int = field(default=None)
#     following: int = field(default=None)
#     password: str = field(default=None)
#     joined: str = field(default=None)


# @dataclass
# class OrganizationItem:
#     icon: str = field(default=None)
#     link: str = field(default=None)


# @dataclass
# class RepositoryItem:
#     title: str = field(default=None)
#     description: str = field(default=None)
#     last_updated: str = field(default=None)
#     url: str = field(default=None)
#     stars: int = field(default=None)
#     branches: int = field(default=None)

