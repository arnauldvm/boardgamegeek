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

from copy import copy
import datetime

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


class FullItem(DictObject):
    """
    The properties which exist on the "full" version of the main collectible objects
    but which _don't_ exist on the abbreviated forms returned by the "collection" API.
    """
    def __init__(self, data):
        self._data = data

        self._comments = []
        for comment in data.get("comments", []):
            self.add_comment(comment)

        self._expansions = []                      # list of Thing for the expansions
        self._expansions_set = set()               # set for making sure things are unique
        for exp in data.get("expansions", []):
            try:
                if exp["id"] not in self._expansions_set:
                    self._expansions_set.add(exp["id"])
                    self._expansions.append(Thing(exp))
            except KeyError:
                raise BGGError("invalid expansion data")

        self._expands = []                         # list of Thing which this item expands
        self._expands_set = set()                  # set for keeping things unique
        for exp in data.get("expands", []):        # for all the items this game expands, create a Thing
            try:
                if exp["id"] not in self._expands_set:
                    self._expands_set.add(exp["id"])
                    self._expands.append(Thing(exp))
            except KeyError:
                raise BGGError("invalid expanded game data")

        self._videos = []
        self._videos_ids = set()
        for video in data.get("videos", []):
            try:
                if video["id"] not in self._videos_ids:
                    self._videos.append(BoardGameVideo(video))
                    self._videos_ids.add(video["id"])
            except KeyError:
                raise BGGError("invalid video data")

    def add_comment(self, data):
        self._comments.append(BoardGameComment(data))

    def add_expanded_game(self, data):
        """
        Add a game expanded by this one

        :param dict data: expanded game's data
        :raises: :py:exc:`boardgamegeek.exceptions.BoardGameGeekError` if data is invalid
        """
        try:
            if data["id"] not in self._expands_set:
                self._data["expands"].append(data)
                self._expands_set.add(data["id"])
                self._expands.append(Thing(data))
        except KeyError:
            raise BGGError("invalid expanded game data")

    def add_expansion(self, data):
        """
        Add an expansion of this game

        :param dict data: expansion data
        :raises: :py:exc:`boardgamegeek.exceptions.BoardGameGeekError` if data is invalid
        """
        try:
            if data["id"] not in self._expansions_set:
                self._data["expansions"].append(data)
                self._expansions_set.add(data["id"])
                self._expansions.append(Thing(data))
        except KeyError:
            raise BGGError("invalid expansion data")

    @property
    def alternative_names(self):
        """
        :return: alternative names
        :rtype: list of str
        """
        return self._data.get("alternative_names", [])

    @property
    def description(self):
        """
        :return: description
        :rtype: str
        """
        return self._data.get("description", "")

    @property
    def comments(self):
        return self._comments

    @property
    def expansions(self):
        """
        :return: expansions
        :rtype: list of :py:class:`boardgamegeek.things.Thing`
        """
        return self._expansions

    @property
    def expands(self):
        """
        :return: games this item expands
        :rtype: list of :py:class:`boardgamegeek.things.Thing`
        """
        return self._expands

    @property
    def publishers(self):
        """
        :return: publishers
        :rtype: list of str
        """
        return self._data.get("publishers", [])

    @property
    def expansion(self):
        """
        :return: True if this item is an expansion
        :rtype: bool
        """
        return self._data.get("expansion", False)

    @property
    def users_owned(self):
        """
        :return: number of users owning this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._stats.users_owned

    @property
    def users_trading(self):
        """
        :return: number of users trading this game
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._stats.users_trading

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
        return self._stats.rating_num_weights

    @property
    def rating_average_weight(self):
        """
        :return: average weight
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._stats.rating_average_weight

    @property
    def videos(self):
        """
        :return: videos of this game
        :rtype: list of :py:class:`boardgamegeek.game.BoardGameVideo`
        """
        return self._videos

    @property
    def versions(self):
        """
        :return: versions of this game
        :rtype: list of :py:class:`boardgamegeek.game.BoardGameVersion`
        """
        return self._versions


class BoardGameVideo(Thing):
    """
    Object containing information about a board game video
    """
    def __init__(self, data):
        kw = copy(data)

        if "post_date" in kw:
            date = kw["post_date"]
            if type(date) != datetime.datetime:
                try:
                    kw["post_date"] = datetime.datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S")
                except:
                    kw["post_date"] = None

        kw["uploader_id"] = int(kw["uploader_id"])

        super(BoardGameVideo, self).__init__(kw)

    def _format(self, log):
        log.info("video id          : {}".format(self.id))
        log.info("video title       : {}".format(self.name))
        log.info("video category    : {}".format(self.category))
        log.info("video link        : {}".format(self.link))
        log.info("video language    : {}".format(self.language))
        log.info("video uploader    : {}".format(self.uploader))
        log.info("video uploader id : {}".format(self.uploader_id))
        log.info("video posted at   : {}".format(self.post_date))

    @property
    def category(self):
        """
        :return: the category of this video
        :return: ``None`` if n/a
        :rtype: string
        """
        return self._data.get("category")

    @property
    def link(self):
        """
        :return: the link to this video
        :return: ``None`` if n/a
        :rtype: string
        """
        return self._data.get("link")

    @property
    def language(self):
        """
        :return: the language of this video
        :return: ``None`` if n/a
        :rtype: string
        """
        return self._data.get("language")

    @property
    def uploader(self):
        """
        :return: the name of the user which uploaded this video
        :return: ``None`` if n/a
        :rtype: string
        """
        return self._data.get("uploader")

    @property
    def uploader_id(self):
        """
        :return: id of the uploader
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("uploader_id")

    @property
    def post_date(self):
        """
        :return: date when this video was uploaded
        :rtype: datetime.datetime
        :return: ``None`` if n/a
        """
        return self._data.get("post_date")
