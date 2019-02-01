# coding: utf-8
"""
:mod:`boardgamegeek.things` - Generic objects
=============================================

.. module:: boardgamegeek.things
   :platform: Unix, Windows
   :synopsis: Generic objects

.. moduleauthor:: Cosmin Luță <q4break@gmail.com>

"""
from __future__ import unicode_literals

from ..exceptions import BGGError
from ..utils import DictObject, fix_url


class Thing(DictObject):
    """
    A thing, an object with a name and an id. Base class for various objects in the library.
    """
    def __init__(self, data):
        for i in ["id", "name"]:
            if i not in data:
                raise BGGError("missing '{}' when trying to create a Thing".format(i))

        try:
            self._id = int(data["id"])
        except:
            raise BGGError("id ({}) is not an int when trying to create a Thing".format(data["id"]))

        self._name = data["name"]

        super(Thing, self).__init__(data)

    @property
    def name(self):
        """
        :return: name
        :rtype: str
        """
        return self._name

    @property
    def id(self):
        """
        :return: id
        :rtype: integer
        """
        return self._id

    def __repr__(self):
        return "Thing (id: {})".format(self.id)


class BaseItem(Thing):
    """
    The base item which represents all collectible "things" across the BGG network: boardgames,
    boardgame expansions, boardgame accessories, RPG items, RPG issues, and video games in both
    their primary form (via the "thing" API) and abbreviated form (via the "collection" API).
    """
    def __init__(self, data):
        if "stats" not in data:
            raise BGGError("'stats' not in dictionary")

        self._thumbnail = fix_url(data["thumbnail"]) if "thumbnail" in data else None
        self._image = fix_url(data["image"]) if "image" in data else None
        self._stats = BoardGameStats(data["stats"])

        super(BaseItem, self).__init__(data)

    @property
    def thumbnail(self):
        """
        :return: thumbnail URL
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._thumbnail

    @property
    def image(self):
        """
        :return: image URL
        :rtype: str
        :return: ``None`` if n/a
        """
        return self._image

    # TODO: create properties to access the stats

    @property
    def users_rated(self):
        """
        :return: how many users rated the game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._stats.users_rated

    @property
    def rating_average(self):
        """
        :return: average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_average

    @property
    def rating_bayes_average(self):
        """
        :return: bayes average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_bayes_average

    @property
    def rating_stddev(self):
        """
        :return: standard deviation
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_stddev

    @property
    def rating_median(self):
        """
        :return:
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_median

    @property
    def ranks(self):
        #TODO: document this change. It's not returning list of dicts anymore, but BoardGameRank objects
        """
        :return: rankings of this game
        :rtype: list of dicts, keys: ``friendlyname`` (the friendly name of the rank, e.g. "Board Game Rank"), ``name``
                (name of the rank, e.g "boardgame"), ``value`` (the rank)
        :return: ``None`` if n/a
        """
        return self._stats.ranks


class BoardGameStats(DictObject):
    """
    Statistics about a board game
    """
    def __init__(self, data):
        self._ranks = []

        for rank in data.get("ranks", []):
            if rank.get("name") == "boardgame":
                try:
                    self._bgg_rank = int(rank["value"])
                except (KeyError, TypeError):
                    self._bgg_rank = None
            self._ranks.append(BoardGameRank(rank))

        super(BoardGameStats, self).__init__(data)

    @property
    def bgg_rank(self):
        return self._bgg_rank

    @property
    def ranks(self):
        return self._ranks

    @property
    def users_rated(self):
        """
        :return: how many users rated the game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("usersrated")

    @property
    def rating_average(self):
        """
        :return: average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("average")

    @property
    def rating_bayes_average(self):
        """
        :return: bayes average rating
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("bayesaverage")

    @property
    def rating_stddev(self):
        """
        :return: standard deviation
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("stddev")

    @property
    def rating_median(self):
        """
        :return:
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("median")

    @property
    def users_owned(self):
        """
        :return: number of users owning this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("owned")

    @property
    def users_trading(self):
        """
        :return: number of users trading this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("trading")

    @property
    def users_wanting(self):
        """
        :return: number of users wanting this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("wanting")

    @property
    def users_wishing(self):
        """
        :return: number of users wishing for this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("wishing")

    @property
    def users_commented(self):
        """
        :return: number of user comments
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("numcomments")

    @property
    def rating_num_weights(self):
        """
        :return:
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("numweights")

    @property
    def rating_average_weight(self):
        """
        :return: average weight
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("averageweight")


class BoardGameComment(DictObject):

    @property
    def commenter(self):
        return self._data["username"]

    @property
    def comment(self):
        return self._data["comment"]

    @property
    def rating(self):
        return self._data["rating"]

    def _format(self, log):
        log.info(u"comment by {} (rating: {}): {}".format(self.commenter, self.rating, self.comment))


class BoardGameRank(Thing):
    @property
    def type(self):
        return self._data.get("type")

    @property
    def friendly_name(self):
        return self._data.get("friendlyname")

    @property
    def value(self):
        return self._data.get("value")

    @property
    def rating_bayes_average(self):
        return self._data.get("bayesaverage")
