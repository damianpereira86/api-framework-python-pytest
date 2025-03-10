from enum import Enum


class Method(Enum):
    Get = "get"
    Post = "post"
    Put = "put"
    Patch = "patch"
    Delete = "delete"
    Head = "head"
    Options = "options"
